"""Aggregation engines."""

import contextlib
import logging
import os
import time
from abc import ABC, abstractmethod
from collections import namedtuple
from collections.abc import Generator
from typing import Union

import dask
import geopandas as gpd
import numpy as np
import numpy.typing as npt
import pandas as pd
import xarray as xr
from joblib import Parallel, delayed, parallel_backend
from pyproj import CRS

from gdptools.agg.stats_methods import (
    Count,
    MACount,
    MAMax,
    MAMin,
    MAWeightedMean,
    MAWeightedMedian,
    MAWeightedStd,
    Max,
    Min,
    StatsMethod,
    WeightedMean,
    WeightedMedian,
    WeightedStd,
)
from gdptools.data.agg_gen_data import AggData
from gdptools.data.user_data import UserData
from gdptools.utils import (
    _cal_point_stats,
    _dataframe_to_geodataframe,
    _get_default_val,
    _get_interp_array,
    _get_line_vertices,
    _get_weight_df,
    _interpolate_sample_points,
)

logger = logging.getLogger(__name__)

AggChunk = namedtuple("AggChunk", ["ma", "wghts", "def_val", "index"])

STAT_TYPES = Union[
    type[MAWeightedMean],
    type[WeightedMean],
    type[MAWeightedStd],
    type[WeightedStd],
    type[MAWeightedMedian],
    type[WeightedMedian],
    type[MACount],
    type[Count],
    type[MAMin],
    type[Min],
    type[MAMax],
    type[Max],
]


class AggEngine(ABC):
    """Abstract aggregation class.

    Args:
    ----
        user_data (UserData): The user data.
        weights (Union[str, pd.DataFrame]): The weights.
        stat (STAT_TYPES): The statistic type.
        jobs (int, optional): The number of jobs. Defaults to -1.

    Returns:
    -------
        Tuple[dict[str, AggData], gpd.GeoDataFrame, List[npt.NDArray[Union[np.int, np.double]]]]: The calculated
            aggregations.

    """

    def calc_agg_from_dictmeta(
        self,
        user_data: UserData,
        weights: str | pd.DataFrame,
        stat: STAT_TYPES,
        jobs: int = -1,
    ) -> tuple[dict[str, AggData], gpd.GeoDataFrame, list[npt.NDArray[np.int_ | np.double]]]:
        """Abstract Base Class for calculating aggregations from dictionary metadata."""
        self.usr_data = user_data
        self.id_feature = user_data.get_feature_id()
        self.vars = user_data.get_vars()
        self.stat = stat
        self.period = None
        self.wghts = _get_weight_df(weights, self.id_feature)
        self._jobs = int(os.cpu_count() / 2) if jobs == -1 else jobs
        # logger.info(f"  ParallelWghtGenEngine using {self._jobs} jobs")

        return self.agg_w_weights()

    @abstractmethod
    def agg_w_weights(
        self,
    ) -> tuple[
        dict[str, AggData],
        gpd.GeoDataFrame,
        list[npt.NDArray[np.int_ | np.double]],
    ]:
        """Abstract method for calculating weights."""
        pass


class SerialAgg(AggEngine):
    """SerialAgg data by feature and time period."""

    def get_period_from_ds(self, data: AggData) -> list[str]:
        """Get starting and ending time strings from a subsetted Dataset.

        Args:
        ----
            data (AggData): The AggData object containing the xarray Dataset.

        Returns:
        -------
            List[str]: A list containing the start and end time strings.
                Returns an empty list if a time coordinate is not found within
                the supplied dataset.

        """
        try:
            tname = data.cat_cr.T_name
            tstrt = str(data.da.coords[tname].values[0])
            tend = str(data.da.coords[tname].values[-1])
            return [tstrt, tend]
        except IndexError:
            # Handle the error
            print("IndexError: This error suggests that the period argument has not been properly specified.")
            # Return an appropriate value or re-raise the error
            # For example, return an empty list or specific error code/message
            return []

    def agg_w_weights(
        self,
    ) -> tuple[
        dict[str, AggData],
        gpd.GeoDataFrame,
        list[npt.NDArray[np.int_ | np.double]],
    ]:
        """Aggregate grid-to-polygon values using area-weighted statistics.

        This method iterates through each variable specified in the user data,
        prepares the data for aggregation, performs the aggregation using the
        `calc_agg` method, and collects the results.

        Returns
        -------
            A tuple containing:
            - A dictionary mapping variable names (str) to their corresponding
              AggData objects.
            - The dissolved GeoDataFrame representing the aggregated geometries.
            - A list of NumPy arrays, where each array contains the aggregated
              values for a specific variable across all geometries and time
              steps.  The shape of each array is (time_steps, geometries).

        """
        # ds_time = self.ds.coords[list(self.param_dict.values())[0]["T_name"]].values
        # date_bracket = np.array_split(ds_time, self.numdiv)
        # print(date_bracket)
        # date_bracket = list(_date_range(self.period[0], self.period[1], self.numdiv))
        r_gdf = []
        r_vals = []
        r_agg_dict = {}
        avars = self.usr_data.get_vars()
        for index, key in enumerate(avars):
            print(f"Processing: {key}")
            tstrt = time.perf_counter()
            agg_data: AggData = self.usr_data.prep_agg_data(key=key)
            tend = time.perf_counter()
            print(f"    Data prepped for aggregation in {tend - tstrt:0.4f} seconds")
            tstrt = time.perf_counter()
            newgdf, nvals = self.calc_agg(key=key, data=agg_data)
            tend = time.perf_counter()
            print(f"    Data aggregated in {tend - tstrt:0.4f} seconds")
            if index == 0:
                # all new GeoDataFrames will be the same so save and return only one.
                r_gdf.append(newgdf)
            r_vals.append(nvals)
            r_agg_dict[key] = agg_data
        return r_agg_dict, r_gdf[0], r_vals

    def calc_agg(
        self: "SerialAgg", key: str, data: AggData
    ) -> tuple[gpd.GeoDataFrame, npt.NDArray[np.int_ | np.double]]:
        """Calculate the aggregation.

        Performs spatial and temporal aggregation of gridded data over geometries
        defined in a GeoDataFrame. This involves sorting, dissolving geometries,
        retrieving data, preparing weights, and performing the aggregation.

        Args:
        ----
            key (str): A reference key for the variable being aggregated.
            data (AggData): Contains the DataArray, GeoDataFrame, and metadata
                required for aggregation.

        Returns:
        -------
            Tuple[gpd.GeoDataFrame, npt.NDArray[Union[np.int_, np.double]]]: A tuple containing:
                - The dissolved GeoDataFrame.
                - Aggregated values as a NumPy array with shape (time_steps, geometries).

        Raises:
        ------
            ValueError: If the data is too large to load into memory. This
                typically occurs when attempting to load a large dataset from a
                remote server.  Consider reducing the time period or working
                with a smaller subset of data.

        """
        cp = data.cat_cr
        gdf = data.feature
        gdf.reset_index(drop=True, inplace=True)
        gdf = gdf.sort_values(data.id_feature).dissolve(by=data.id_feature, as_index=False)
        geo_index = np.asarray(gdf[data.id_feature].values, dtype=type(gdf[data.id_feature].values[0]))
        n_geo = len(geo_index)
        unique_geom_ids = self.wghts.groupby(self.id_feature)
        t_name = cp.T_name
        da = data.da
        nts = len(da.coords[t_name].values)
        native_dtype = da.dtype
        # gdptools will handle floats and ints - catch if gridded type is different
        try:
            dfval = _get_default_val(native_dtype=native_dtype)
        except TypeError as e:
            print(e)

        val_interp = _get_interp_array(n_geo=n_geo, nts=nts, native_dtype=native_dtype, default_val=dfval)
        try:
            da = da.load()
        except Exception as e:
            raise ValueError(
                "This error likely arises when the data requested to aggregate is too large to be retrieved from "
                "a remote server. Please try to reduce the time-period, or work on a smaller subset."
            ) from e
        for i in np.arange(len(geo_index)):
            try:
                weight_id_rows = unique_geom_ids.get_group(str(geo_index[i]))
            except KeyError:
                continue
            tw = weight_id_rows.wght.values
            i_ind = np.array(weight_id_rows.i.values).astype(int)
            j_ind = np.array(weight_id_rows.j.values).astype(int)

            val_interp[:, i] = self.stat(array=da.values[:, i_ind, j_ind], weights=tw, def_val=dfval).get_stat()

        return gdf, val_interp


class ParallelAgg(AggEngine):
    """SerialAgg data by feature and time period."""

    def get_period_from_ds(self, data: AggData) -> list[str]:
        """Get starting and ending time strings from a subsetted Dataset.

        Args:
        ----
            data (AggData): The AggData object containing the xarray Dataset.

        Returns:
        -------
            List[str]: A list containing the start and end time strings. Returns
                an empty list if a time coordinate is not found within the
                supplied dataset.

        """
        try:
            tname = data.cat_cr.T_name
            tstrt = str(data.da.coords[tname].values[0])
            tend = str(data.da.coords[tname].values[-1])
            return [tstrt, tend]
        except IndexError:
            # Handle the error
            print("IndexError: This error suggests that the period argument has not been properly specified.")
            # Return an appropriate value or re-raise the error
            # For example, return an empty list or specific error code/message
            return []

    def agg_w_weights(
        self,
    ) -> tuple[
        dict[str, AggData],
        gpd.GeoDataFrame,
        list[npt.NDArray[np.int_ | np.double]],
    ]:
        """Aggregate grid-to-polygon values using area-weighted statistics.

        This method iterates through each variable specified in the user data,
        prepares the data for aggregation, performs the aggregation using the
        `calc_agg` method, and collects the results.  It leverages parallel
        processing to improve performance.

        Returns
        -------
            A tuple containing:
            - A dictionary mapping variable names (str) to their corresponding
              AggData objects.
            - The dissolved GeoDataFrame representing the aggregated geometries.
            - A list of NumPy arrays, where each array contains the aggregated
              values for a specific variable across all geometries and time
              steps. The shape of each array is (time_steps, geometries).

        """
        # ds_time = self.ds.coords[list(self.param_dict.values())[0]["T_name"]].values
        # date_bracket = np.array_split(ds_time, self.numdiv)
        # print(date_bracket)
        # date_bracket = list(_date_range(self.period[0], self.period[1], self.numdiv))
        r_gdf = []
        r_vals = []
        r_agg_dict = {}
        avars = self.usr_data.get_vars()
        for index, key in enumerate(avars):
            print(f"Processing: {key}")
            tstrt = time.perf_counter()
            agg_data: AggData = self.usr_data.prep_agg_data(key=key)
            tend = time.perf_counter()
            print(f"    Data prepped for aggregation in {tend - tstrt:0.4f} seconds")
            tstrt = time.perf_counter()
            newgdf, nvals = self.calc_agg(key=key, data=agg_data)
            tend = time.perf_counter()
            print(f"    Data aggregated in {tend - tstrt:0.4f} seconds")
            if index == 0:
                # all new GeoDataFrames will be the same so save and return only one.
                r_gdf.append(newgdf)
            r_vals.append(nvals)
            r_agg_dict[key] = agg_data
        return r_agg_dict, r_gdf[0], r_vals

    def calc_agg(
        self: "ParallelAgg", key: str, data: AggData
    ) -> tuple[gpd.GeoDataFrame, npt.NDArray[np.int_ | np.double]]:
        """Calculate the aggregation using Dask.

        Performs spatial and temporal aggregation of gridded data over
        geometries defined in a GeoDataFrame, leveraging Dask for parallel
        computation. This method handles data retrieval, weight preparation,
        Dask-based statistic calculation, and returns the aggregated results.

        Args:
        ----
            key (str): A reference key associated with the variable being
                aggregated.
            data (AggData): An AggData object containing the DataArray (`da`),
                GeoDataFrame (`feature`), and metadata (`cat_cr`) necessary for
                aggregation.  `cat_cr` should include the time coordinate name
                (T_name).

        Returns:
        -------
            Tuple[gpd.GeoDataFrame, npt.NDArray[Union[np.int_, np.double]]]: A tuple containing:
                - The dissolved GeoDataFrame.
                - A NumPy array of aggregated values for each geometry over the
                  specified time period, with shape (time_steps, geometries).

        Raises:
        ------
            ValueError: If the requested data subset is too large to load into
                memory. This can occur when retrieving large datasets from a
                remote server.  Try reducing the time period or working with a
                smaller subset of the data.

        """
        cp = data.cat_cr
        period = self.get_period_from_ds(data=data)
        gdf = data.feature
        # gdf.reset_index(drop=True, inplace=True)
        gdf = gdf.sort_values(self.id_feature, axis=0).dissolve(self.id_feature, as_index=False)
        geo_index = np.asarray(gdf.index, dtype=type(gdf.index.values[0]))
        # geo_index_chunk = np.array_split(geo_index, self._jobs)
        n_geo = len(geo_index)
        unique_geom_ids = self.wghts.groupby(self.id_feature, sort=True)
        t_name = cp.T_name
        selection = {t_name: slice(period[0], period[1])}
        da = data.da.sel(**selection)  # type: ignore
        nts = len(da.coords[t_name].values)
        native_dtype = da.dtype
        # gdptools will handle floats and ints - catch if gridded type is different
        try:
            dfval = _get_default_val(native_dtype=native_dtype)
        except TypeError as e:
            print(e)

        val_interp = _get_interp_array(n_geo=n_geo, nts=nts, native_dtype=native_dtype, default_val=dfval)

        # mdata = np.ma.masked_array(da.values, np.isnan(da.values))  # type: ignore
        try:
            mdata = da.values  # type: ignore
        except Exception as e:
            raise ValueError(
                "This error likely arrises when the data requested to aggregate is too large to be retrieved from,"
                " a remote server."
                "Please try to reduce the time-period, or work on a smaller subset."
            ) from e

        chunks = get_weight_chunks(
            unique_geom_ids=unique_geom_ids,
            feature=gdf,
            id_feature=self.id_feature,
            mdata=mdata,
            dfval=dfval,
        )

        worker_out = get_stats_parallel(
            n_jobs=self._jobs,
            stat=self.stat,
            bag=bag_generator(jobs=self._jobs, chunks=chunks),
        )

        for index, val in worker_out:
            val_interp[:, index] = val

        return gdf, val_interp


def _stats(
    bag: list[AggChunk], method: StatsMethod
) -> tuple[npt.NDArray[np.int_], npt.NDArray[np.int_ | np.double]]:
    vals = np.zeros((bag[0].ma.shape[0], len(bag)), dtype=bag[0].ma.dtype)
    index = np.zeros(len(bag), dtype=np.int_)
    for idx, b in enumerate(bag):
        index[idx] = b.index
        vals[:, idx] = method(array=b.ma, weights=b.wghts, def_val=b.def_val).get_stat()  # type: ignore
    return (index, vals)


def get_stats_parallel(
    n_jobs: int, stat: STAT_TYPES, bag: Generator[list[AggChunk], None, None]
) -> list[tuple[npt.NDArray[np.int_], npt.NDArray[np.int_ | np.double]]]:
    """Calculate statistics in parallel using joblib.

    This function calculates statistics for multiple chunks of data in
    parallel using joblib.  It takes a generator of data chunks, applies a
    statistical method to each chunk, and returns the results as a list of
    tuples.

    Args:
    ----
        n_jobs (int): The number of parallel jobs to run.
        stat (STAT_TYPES): The statistical method to apply to each chunk.
        bag (Generator[List[AggChunk], None, None]): A generator that yields
            lists of AggChunk namedtuples.  Each AggChunk contains the data
            array, weights, default value, and index.

    Returns:
    -------
        List[Tuple[npt.NDArray[np.int_], npt.NDArray[Union[np.int_, np.double]]]]:
            A list of tuples, where each tuple contains:
                - An array of indices corresponding to the chunks.
                - An array of calculated statistic values for each chunk.

    """
    with parallel_backend("loky", inner_max_num_threads=1):
        worker_out = Parallel(n_jobs=n_jobs)(delayed(_stats)(chunk, method=stat) for chunk in bag)
    return worker_out


def get_weight_chunks(
    unique_geom_ids: gpd.GeoDataFrame.groupby,
    feature: gpd.GeoDataFrame,
    id_feature: str,
    # mdata: np.ma.MaskedArray,  # type: ignore
    mdata: npt.NDArray,  # type: ignore
    dfval: np.int_ | np.double,
) -> list[AggChunk]:
    """Chunk data for parallel aggregation."""
    # keys = list(unique_geom_ids.groups.keys())
    keys = feature[id_feature].values
    chunks = []
    # for idx, (name, group) in enumerate(unique_geom_ids):
    for idx, key in enumerate(keys):
        with contextlib.suppress(Exception):
            weight_id_rows = unique_geom_ids.get_group(str(key))
            chunks.append(
                AggChunk(
                    mdata[
                        :,
                        np.array(weight_id_rows.i.values).astype(int),
                        np.array(weight_id_rows.j.values).astype(int),
                    ],
                    weight_id_rows.wght.values,
                    dfval,
                    idx,
                )
            )
    return chunks


def bag_generator(jobs: int, chunks: list[AggChunk]) -> Generator[list[AggChunk], None, None]:
    """Generate chunks."""
    chunk_size = len(chunks) // jobs + 1
    for i in range(0, len(chunks), chunk_size):
        yield chunks[i : i + chunk_size]


class DaskAgg(AggEngine):
    """SerialAgg data by feature and time period."""

    def get_period_from_ds(self, data: AggData) -> list[str]:
        """Get starting and ending time strings from a subsetted Dataset.

        Args:
        ----
            data (AggData): The AggData object containing the xarray Dataset.

        Returns:
        -------
            List[str]: A list containing the start and end time strings. Returns
                an empty list if a time coordinate is not found.

        """
        try:
            tname = data.cat_cr.T_name
            tstrt = str(data.da.coords[tname].values[0])
            tend = str(data.da.coords[tname].values[-1])
            return [tstrt, tend]
        except IndexError:
            # Handle the error
            print("IndexError: This error suggests that the period argument has not been properly specified.")
            # Return an appropriate value or re-raise the error
            # For example, return an empty list or specific error code/message
            return []

    def agg_w_weights(
        self,
    ) -> tuple[
        dict[str, AggData],
        gpd.GeoDataFrame,
        list[npt.NDArray[np.int_ | np.double]],
    ]:
        """Aggregate grid-to-polygon values using area-weighted statistics with Dask.

        This method iterates through each variable specified in the user data,
        prepares the data for aggregation, performs the aggregation using Dask
        and the `calc_agg` method, and collects the results.

        Returns
        -------
            A tuple containing:
            - A dictionary mapping variable names (str) to their corresponding
              AggData objects.
            - The dissolved GeoDataFrame representing the aggregated geometries.
            - A list of NumPy arrays, where each array contains the aggregated
              values for a specific variable across all geometries and time steps.
              The shape of each array is (time_steps, geometries).

        """
        r_gdf = []
        r_vals = []
        r_agg_dict = {}
        avars = self.usr_data.get_vars()
        for index, key in enumerate(avars):
            print(f"Processing: {key}")
            tstrt = time.perf_counter()
            agg_data: AggData = self.usr_data.prep_agg_data(key=key)
            tend = time.perf_counter()
            print(f"    Data prepped for aggregation in {tend - tstrt:0.4f} seconds")
            tstrt = time.perf_counter()
            newgdf, nvals = self.calc_agg(key=key, data=agg_data)
            tend = time.perf_counter()
            print(f"    Data aggregated in {tend - tstrt:0.4f} seconds")
            if index == 0:
                # all new GeoDataFrames will be the same so save and return only one.
                r_gdf.append(newgdf)
            r_vals.append(nvals)
            r_agg_dict[key] = agg_data
        return r_agg_dict, r_gdf[0], r_vals

    def calc_agg(
        self: "DaskAgg", key: str, data: AggData
    ) -> tuple[gpd.GeoDataFrame, npt.NDArray[np.int_ | np.double]]:
        """Calculate the aggregation using Dask.

        Performs spatial and temporal aggregation of gridded data over
        geometries defined in a GeoDataFrame, leveraging Dask for parallel
        computation. This method handles data retrieval, weight preparation,
        Dask-based statistic calculation, and returns the aggregated results.

        Args:
        ----
            key (str): A reference key associated with the variable being
                aggregated.
            data (AggData): An AggData object containing the DataArray (`da`),
                GeoDataFrame (`feature`), and metadata (`cat_cr`) necessary for
                aggregation.  `cat_cr` should include the time coordinate name
                (T_name).

        Returns:
        -------
            Tuple[gpd.GeoDataFrame, npt.NDArray[Union[np.int_, np.double]]]: A tuple containing:
                - The dissolved GeoDataFrame.
                - A NumPy array of aggregated values for each geometry over the
                  specified time period, with shape (time_steps, geometries).

        Raises:
        ------
            ValueError: If the requested data subset is too large to load into
                memory. This can occur when retrieving large datasets from a
                remote server.  Try reducing the time period or working with a
                smaller subset of the data.

        """
        cp = data.cat_cr
        period = self.get_period_from_ds(data=data)
        gdf = data.feature
        gdf = gdf.sort_values(self.id_feature, axis=0).dissolve(self.id_feature, as_index=False)
        geo_index = np.asarray(gdf.index, dtype=type(gdf.index.values[0]))
        # geo_index_chunk = np.array_split(geo_index, self._jobs)
        n_geo = len(geo_index)
        unique_geom_ids = self.wghts.groupby(self.id_feature, sort=True)
        t_name = cp.T_name
        selection = {t_name: slice(period[0], period[1])}
        da = data.da.sel(**selection)  # type: ignore
        nts = len(da.coords[t_name].values)
        native_dtype = da.dtype
        # gdptools will handle floats and ints - catch if gridded type is different
        try:
            dfval = _get_default_val(native_dtype=native_dtype)
        except TypeError as e:
            print(e)

        val_interp = _get_interp_array(n_geo=n_geo, nts=nts, native_dtype=native_dtype, default_val=dfval)

        try:
            mdata = da.values  # type: ignore
        except Exception as e:
            raise ValueError(
                "This error likely arrises when the data requested to aggregate is too large to be retrieved from,"
                " a remote server."
                "Please try to reduce the time-period, or work on a smaller subset."
            ) from e

        chunks = get_weight_chunks(
            unique_geom_ids=unique_geom_ids,
            feature=gdf,
            id_feature=self.id_feature,
            mdata=mdata,
            dfval=dfval,
        )

        worker_out = get_stats_dask(
            n_jobs=self._jobs,
            stat=self.stat,
            bag=bag_generator(jobs=self._jobs, chunks=chunks),
        )

        for index, val in worker_out[0]:
            val_interp[:, index] = val

        return gdf, val_interp


def get_stats_dask(
    n_jobs: int,
    stat: STAT_TYPES,
    bag: Generator[list[AggChunk], None, None],
) -> list[list[tuple[npt.NDArray[np.int_], npt.NDArray[np.int_ | np.double]]]]:
    """Calculate statistics using Dask.

    This function calculates statistics for multiple chunks of data using
    Dask. It takes a generator of data chunks, applies a statistical method
    to each chunk, and returns the results as a list of lists of tuples.

    Args:
    ----
        n_jobs (int): The number of Dask workers to use.  Not currently used.
        stat (STAT_TYPES): The statistical method to apply to each chunk.
        bag (Generator[List[AggChunk], None, None]): A generator that yields
            lists of AggChunk namedtuples. Each AggChunk contains the data
            array, weights, default value, and index.

    Returns:
    -------
        List[List[Tuple[npt.NDArray[np.int_], npt.NDArray[Union[np.int_, np.double]]]]]:
            A list of lists of tuples, where each inner tuple contains:
                - An array of indices corresponding to the chunks.
                - An array of calculated statistic values for each chunk.
            The outer list structure arises from the Dask compute operation.

    """
    worker_out = [dask.delayed(_stats)(chunk, method=stat) for chunk in bag]  # type: ignore
    return dask.compute(worker_out)  # type: ignore


class InterpEngine(ABC):
    """Abstract class for interpolation."""

    def run(
        self,
        *,
        user_data: UserData,
        pt_spacing: float | int | None,
        stat: str,
        interp_method: str,
        calc_crs: int | str | CRS,
        mask_data: float | int | None,
        output_file: str | None = None,
        jobs: int = -1,
    ) -> tuple[pd.DataFrame, gpd.GeoDataFrame] | pd.DataFrame:
        """Run InterpEngine Class.

        _extended_summary_

        Args:
        ----
            user_data (UserData): Data Class for input data
            pt_spacing (Union[float, int, None]): Numerical value in meters for the
                spacing of the interpolated sample points (default is 50)
            stat (str):  A string indicating which statistics to calculate during
                the query. Options: 'all', 'mean', 'median', 'std', 'max', 'min'
                (default is 'all')
            interp_method (str): Optional; String indicating the xarray interpolation method.
                Default method in 'linear'. Options: "linear", "nearest", "zero", "slinear",
                "quadratic", "cubic", "polynomial".
            calc_crs (Union[int, str, CRS]): OGC WKT string, Proj.4 string or int EPSG code.
                Determines which projection is used for the area weighted calculations
            mask_data (bool or None): Optional; When True, nodata values are removed from
                statistical calculations.
            output_file (str or None): Optional; When a file path is specified, a CSV
                of the statistics will be written to that file path. Must end with .csv
                file ending.
            jobs (int): _description_. Defaults to -1.

        Returns:
        -------
            Tuple[pd.DataFrame, gpd.GeoDataFrame]: Returns a DataFrame of the
                statistics and a GeoDataFrame of the point geometries

        """
        self._user_data = user_data
        self._pt_spacing = pt_spacing
        self._stat = stat
        self._interp_method = interp_method
        self._calc_crs = calc_crs
        self._mask_data = mask_data
        self._output_file = output_file
        if jobs == -1:
            self._jobs = int(os.cpu_count() / 2)  # type: ignore
            logger.info(" ParallelWghtGenEngine getting jobs from os.cpu_count()")
        else:
            self._jobs = jobs
        logger.info(f"  ParallelWghtGenEngine using {self._jobs} jobs")

        return self.interp()

    @abstractmethod
    def interp(self) -> None:
        """Abstract method for interpolating point values."""
        pass

    def get_variables(self, key: str) -> dict:
        """Get variable dictionary of values needed for interpolation processing."""
        # Get crs and coord names for gridded data
        user_data_type = self._user_data.get_class_type()

        if user_data_type == "ClimRCatData":
            grid_proj = self._user_data.cat_dict[key]["crs"]
            x_coord = self._user_data.cat_dict[key]["X_name"]
            y_coord = self._user_data.cat_dict[key]["Y_name"]
            t_coord = self._user_data.cat_dict[key]["T_name"]
            varname = self._user_data.cat_dict[key]["varname"]

        elif user_data_type in ["UserCatData", "NHGFStacData"]:
            grid_proj = self._user_data.proj_ds
            x_coord = self._user_data.x_coord
            y_coord = self._user_data.y_coord
            t_coord = self._user_data.t_coord
            varname = key

        elif user_data_type == "UserTiffData":
            grid_proj = self._user_data.proj_ds
            x_coord = self._user_data.x_coord
            y_coord = self._user_data.y_coord
            t_coord = None
            varname = key

        return {
            "key": key,
            "varname": varname,
            "spacing": self._pt_spacing,
            "grid_proj": grid_proj,
            "calc_crs": self._calc_crs,
            "x_coord": x_coord,
            "y_coord": y_coord,
            "t_coord": t_coord,
            "id_feature": self._user_data.id_feature,
            "class_type": user_data_type,
            "stat": self._stat,
            "mask_data": self._mask_data,
        }


class SerialInterp(InterpEngine):
    """Serial Interpolation Class."""

    def get_period_from_ds(self, data: AggData) -> list[str]:
        """Get starting and ending time strings from a subsetted Dataset.

        Args:
        ----
            data (AggData): The AggData object containing the xarray Dataset.

        Returns:
        -------
            List[str]: A list containing the start and end time strings.
                Returns an empty list if a time coordinate is not found within
                the supplied dataset.

        """
        try:
            tname = data.cat_cr.T_name
            tstrt = str(data.da.coords[tname].values[0])
            tend = str(data.da.coords[tname].values[-1])
            return [tstrt, tend]
        except IndexError:
            # Handle the error
            print("IndexError: This error suggests that the period argument has not been properly specified.")
            # Return an appropriate value or re-raise the error
            # For example, return an empty list or specific error code/message
            return []

    def interp(
        self,
    ) -> tuple[dict[str, AggData], pd.DataFrame, gpd.GeoDataFrame]:
        """Interpolate values along line geometries.

        This method iterates through each variable in the user data, prepares
        the data for interpolation, performs the interpolation for each line
        geometry using the `grid_to_line_intersection` method, and collects
        the results.

        Returns
        -------
            A tuple containing:
                - A dictionary mapping variable names (str) to their
                  corresponding AggData objects used in the interpolation.
                - A DataFrame containing the calculated statistics for all
                  interpolated points.
                - A GeoDataFrame containing the point geometries generated along
                  the lines.

        """
        # Get each grid variable
        wvars = self._user_data.get_vars()

        stats_list = []
        points_list = []
        out_grid = {}

        # Loop thru each grid variable
        for _index, key in enumerate(wvars):
            logger.debug(f"Starting to process {key}")
            # loop thru each line geometry
            line_dict = {}
            for i in range(len(self._user_data.f_feature)):
                logger.debug("Looping through lines")
                # Pull geometry ID from geodataframe
                line_id = self._user_data.f_feature.loc[[i]][self._user_data.id_feature][i]
                # Prep the input data
                interp_data: AggData = self._user_data.prep_interp_data(key=key, poly_id=line_id)
                logger.debug("Defined interp_data")
                line_dict[line_id] = interp_data
                # Calculate statistics
                statistics, pts = self.grid_to_line_intersection(interp_data, key=key)
                logger.debug("Calculated stats and pts")
                stats_list.append(statistics)
                points_list.append(pts)

            out_grid[key] = line_dict

        stats = pd.concat(stats_list).reset_index()
        points = pd.concat(points_list).reset_index()

        if self._output_file:
            stats.to_csv(self._output_file)

        # Project points back to original crs
        points = points.to_crs(self._user_data.proj_feature)
        logger.debug("Finished running serial interp")

        return out_grid, stats, points

    def grid_to_line_intersection(
        self: "InterpEngine", interp_data: "AggData", key: str | None = None
    ) -> tuple[pd.DataFrame, gpd.GeoDataFrame]:
        """Extract grid values and statistics for a polyline geometry.

        This method interpolates points along a line geometry, extracts grid
        values at these points, and calculates statistics based on the
        extracted values.

        Args:
        ----
            interp_data (AggData): An AggData object containing information
                about the line geometry and the gridded data to interpolate.
            key (Union[str, None], optional): The name of the variable in the
                xarray Dataset. Defaults to None.

        Returns:
        -------
            Tuple[pd.DataFrame, gpd.GeoDataFrame]: A tuple containing:
                - A DataFrame of the calculated statistics at the interpolated
                  points.
                - A GeoDataFrame of the interpolated point geometries.

        """
        data_array = interp_data.da
        varname = interp_data.cat_cr.varname
        spacing = self._pt_spacing
        user_data_type = self._user_data.get_class_type()

        # Get crs and coord names for gridded data
        if user_data_type in ["ClimRCatData"]:
            grid_proj = self._user_data.cat_dict[key]["crs"]
            x_coord = self._user_data.cat_dict[key]["X_name"]
            y_coord = self._user_data.cat_dict[key]["Y_name"]
        elif user_data_type in ["UserCatData", "NHGFStacData", "UserTiffData"]:
            grid_proj = self._user_data.proj_ds
            x_coord = self._user_data.x_coord
            y_coord = self._user_data.y_coord

        # Reproject line to the grid's crs
        line = interp_data.feature.copy()
        geom = line.geometry.to_crs(grid_proj)
        # Either find line vertices
        if spacing == 0:
            x, y, dist = _get_line_vertices(geom=geom, calc_crs=self._calc_crs, crs=grid_proj)
        # Or interpolate sample points
        else:
            x, y, dist = _interpolate_sample_points(geom=geom, spacing=spacing, calc_crs=self._calc_crs, crs=grid_proj)

        # Get the grid values from the interpolated points
        interp_coords = {
            x_coord: ("pt", x),
            y_coord: ("pt", y)
        }
        interp_dataset = data_array.interp(
            **interp_coords, method=self._interp_method
        )

        feature_id_array = np.full(len(dist), interp_data.feature[self._user_data.id_feature].values[0])
        # Add point spacing distance and line IDs
        interp_dataset = xr.merge(
            [
                interp_dataset,
                xr.DataArray(dist, dims=["pt"], name="dist"),
                xr.DataArray(feature_id_array, dims=["pt"], name=self._user_data.id_feature)
            ]
        )
        # Convert to pandas dataframe, reset index to avoid multi-indexed columns: annoying
        interp_geo_df = _dataframe_to_geodataframe(
            interp_dataset.to_dataframe(),
            crs=grid_proj,
            x_coord=x_coord,
            y_coord=y_coord
        )
        interp_geo_df.rename(columns={varname: "values"}, inplace=True)
        id_feature_array = np.full(len(interp_geo_df), varname)
        interp_geo_df["varname"] = id_feature_array
        # prefer date, feature id and varname, up front of dataframe.
        t_coord = interp_data.cat_cr.T_name
        if self._user_data.get_class_type() != "UserTiffData":
            out_vals: dict[str, float] = {"date": interp_dataset[t_coord].values}
            out_vals[self._user_data.id_feature] = np.full(
                out_vals[next(iter(out_vals.keys()))].shape[0],
                interp_data.feature[self._user_data.id_feature].values[0],
            )
        else:
            out_vals: dict[str, float] = {
                self._user_data.id_feature: interp_data.feature[self._user_data.id_feature].values
            }

        out_vals["varname"] = np.full(
            out_vals[next(iter(out_vals.keys()))].shape[0],
            interp_data.cat_cr.varname,
        )
        out_vals |= _cal_point_stats(
            data=interp_dataset[interp_data.cat_cr.varname],
            userdata_type=self._user_data.get_class_type(),
            stat=self._stat,
            skipna=self._mask_data,
        )
        stats_df = pd.DataFrame().from_dict(out_vals)

        return stats_df, interp_geo_df


class ParallelInterp(InterpEngine):
    """Parallel Interpolation Class.

    This method leverages joblib to parallelize the line interpolation methods.
    """

    def get_period_from_ds(self, data: AggData) -> list[str]:
        """Get starting and ending time strings from a subsetted Dataset.

        Args:
        ----
            data (AggData): The AggData object containing the xarray Dataset.

        Returns:
        -------
            List[str]: A list containing the start and end time strings. Returns
                an empty list if a time coordinate is not found within the
                supplied dataset.

        """
        try:
            tname = data.cat_cr.T_name
            tstrt = str(data.da.coords[tname].values[0])
            tend = str(data.da.coords[tname].values[-1])
            return [tstrt, tend]
        except IndexError:
            # Handle the error
            print("IndexError: This error suggests that the period argument has not been properly specified.")
            # Return an appropriate value or re-raise the error
            # For example, return an empty list or specific error code/message
            return []

    def interp(
        self,
    ) -> tuple[dict[str, xr.DataArray], pd.DataFrame, gpd.GeoDataFrame]:
        """Interpolate values along line geometries in parallel.

        This method performs parallel interpolation of gridded data along line
        geometries. It uses joblib to parallelize the processing across
        multiple cores.

        Returns
        -------
            A tuple containing:
                - A dictionary mapping variable names (str) to their
                  corresponding xarray DataArrays.
                - A DataFrame containing the calculated statistics for all
                  interpolated points.
                - A GeoDataFrame containing the point geometries generated along
                  the lines.

        """
        # Get each grid variable
        wvars = self._user_data.get_vars()

        stats_list = []
        points_list = []
        out_grid = {}

        # Loop thru each grid variable
        for _index, key in enumerate(wvars):
            # Chunk the geodataframe into equal parts
            gdf_list = _chunk_gdf(self._jobs, self._user_data.f_feature)

            # Clip gridded data to 2d bounds of the input gdf
            data_array: xr.DataArray = self._user_data.get_source_subset(key)

            # Comb the user_data object for variables needed for the processing
            variables: dict = self.get_variables(key)
            variables["interp_method"] = self._interp_method

            with parallel_backend("loky", inner_max_num_threads=1):
                worker_out = Parallel(n_jobs=self._jobs)(
                    delayed(_grid_to_line_intersection)(chunk, data_array, variables) for chunk in gdf_list
                )

            key_stats: pd.DataFrame = pd.concat(list(zip(*worker_out))[0])  # noqa B905
            key_points: gpd.GeoDataFrame = pd.concat(list(zip(*worker_out))[1])  # noqa B905
            stats_list.append(key_stats)
            points_list.append(key_points)
            out_grid[key] = data_array
            del worker_out, key_stats, key_points

        stats = pd.concat(stats_list).reset_index()
        points = pd.concat(points_list).reset_index()

        if self._output_file:
            stats.to_csv(self._output_file)

        # Project points back to original crs
        points = points.to_crs(self._user_data.proj_feature)

        return out_grid, stats, points


class DaskInterp(InterpEngine):
    """Dask Interpolation Class.

    This method leverages Dask to parallelize the interpolation methods.
    """

    def get_period_from_ds(self, data: AggData) -> list[str]:
        """Get starting and ending time strings from a subsetted Dataset.

        Args:
        ----
            data (AggData): The AggData object containing the xarray Dataset.

        Returns:
        -------
            List[str]: A list containing the start and end time strings. Returns
                an empty list if a time coordinate is not found.

        """
        try:
            tname = data.cat_cr.T_name
            tstrt = str(data.da.coords[tname].values[0])
            tend = str(data.da.coords[tname].values[-1])
            return [tstrt, tend]
        except IndexError:
            # Handle the error
            print("IndexError: This error suggests that the period argument has not been properly specified.")
            # Return an appropriate value or re-raise the error
            # For example, return an empty list or specific error code/message
            return []

    def interp(
        self,
    ) -> tuple[dict[str, xr.DataArray], pd.DataFrame, gpd.GeoDataFrame]:
        """Interpolate values along line geometries using Dask.

        This method performs parallel interpolation of gridded data along line
        geometries using Dask.

        Returns
        -------
            A tuple containing:
                - A dictionary mapping variable names (str) to their
                  corresponding xarray DataArrays.
                - A DataFrame containing the calculated statistics for all
                  interpolated points.
                - A GeoDataFrame containing the point geometries generated
                  along the lines.

        """
        import dask.bag as db

        # Get each grid variable, get line ids
        wvars = self._user_data.get_vars()
        line_ids_list = self._user_data.f_feature.index.to_list()

        stats_list = []
        points_list = []
        out_grid = {}

        # Loop thru each grid variable
        for _index, key in enumerate(wvars):
            # Clip gridded data to 2d bounds of the gdf
            self.data_array: xr.DataArray = self._user_data.get_source_subset(key)
            # Comb the user_data object for variables needed for the processing
            self.variables: dict = self.get_variables(key)

            bag = db.from_sequence(line_ids_list).map(self.g2l)
            results = bag.compute()
            del bag

            key_stats: pd.DataFrame = pd.concat(list(zip(*results))[0])  # noqa B905
            key_points: gpd.GeoDataFrame = pd.concat(list(zip(*results))[1])  # noqa B905
            stats_list.append(key_stats)
            points_list.append(key_points)
            out_grid[key] = self.data_array
            del results, key_stats, key_points

        stats = pd.concat(stats_list).reset_index()
        points = pd.concat(points_list).reset_index()

        if self._output_file:
            stats.to_csv(self._output_file)

        # Project points back to original crs
        points = points.to_crs(self._user_data.proj_feature)

        return out_grid, stats, points

    def g2l(self, id: int) -> tuple[pd.DataFrame, gpd.GeoDataFrame]:
        """Simplified grid to line function.

        This method performs the core interpolation logic for a single line
        geometry, extracting grid values at interpolated points and calculating
        statistics.  It's designed to be used within a Dask bag for parallel
        processing.

        Args:
        ----
            id (int): Row index of the line geometry in the GeoDataFrame.

        Returns:
        -------
            Tuple[pd.DataFrame, gpd.GeoDataFrame]: A tuple containing:
                - A single-row DataFrame of the calculated statistics for the
                  interpolated points along the line.
                - A single-row GeoDataFrame of the interpolated point
                  geometries along the line.

        """
        variables = self.variables
        variables["interp_method"] = self._interp_method

        line = self._user_data.f_feature.loc[[id]]
        geom = line.geometry

        # Either find line vertices
        if variables["spacing"] == 0:
            x, y, dist = _get_line_vertices(geom=geom, calc_crs=variables["calc_crs"], crs=variables["grid_proj"])

        # Or interpolate sample points
        else:
            x, y, dist = _interpolate_sample_points(
                geom=geom,
                spacing=variables["spacing"],
                calc_crs=variables["calc_crs"],
                crs=variables["grid_proj"],
            )

        # Get the grid values from the interpolated points
        interp_coords = {
            variables["x_coord"]: ("pt", x),
            variables["y_coord"]: ("pt", y)
        }
        interp_dataset = self.data_array.interp(
            **interp_coords, method=variables["interp_method"]
        )

        feature_id_array = np.full(len(dist), line[variables["id_feature"]].values[0])
        # Add distsance and polygon IDs
        interp_dataset = xr.merge(
            [
                interp_dataset,
                xr.DataArray(dist, dims=["pt"], name="dist"),
                xr.DataArray(feature_id_array, dims=["pt"], name=variables["id_feature"]),
            ]
        )

        interp_geo_df = _dataframe_to_geodataframe(
            interp_dataset.to_dataframe(),
            crs=variables["grid_proj"],
            x_coord=variables["x_coord"],
            y_coord=variables["y_coord"]
        )
        interp_geo_df.rename(columns={variables["varname"]: "values"}, inplace=True)
        id_feature_array = np.full(len(interp_geo_df), variables["varname"])
        interp_geo_df["varname"] = id_feature_array

        # prefer date, feature id and varname, up front of dataframe.
        if variables["t_coord"] is not None:
            out_vals: dict[str, float] = {"date": interp_dataset[variables["t_coord"]].values}
            out_vals[variables["id_feature"]] = np.full(
                out_vals[next(iter(out_vals.keys()))].shape[0],
                line[variables["id_feature"]].values[0],
            )
        else:
            out_vals: dict[str, float] = {variables["id_feature"]: line[variables["id_feature"]].values}

        out_vals["varname"] = np.full(
            out_vals[next(iter(out_vals.keys()))].shape[0],
            variables["varname"],
        )
        out_vals |= _cal_point_stats(
            data=interp_dataset[variables["varname"]],
            userdata_type=variables["class_type"],
            stat=variables["stat"],
            skipna=variables["mask_data"],
        )

        stats = pd.DataFrame().from_dict(out_vals)

        return stats, interp_geo_df


def _chunk_gdf(processes: int, f_feature: gpd.GeoDataFrame) -> list[gpd.GeoDataFrame]:
    """Divide a GeoDataFrame into equal chunks.

    Divides the input GeoDataFrame into a specified number of chunks,
    primarily for parallel processing purposes.  Each chunk is a
    GeoDataFrame containing a subset of the original data.

    Args:
    ----
        processes (int): The number of chunks to create.
        f_feature (gpd.GeoDataFrame): The GeoDataFrame to divide.

    Returns:
    -------
        List[gpd.GeoDataFrame]: A list of GeoDataFrames, each representing a
            chunk of the original.

    """
    from math import ceil

    gdf_list = []
    num_feat = len(f_feature)
    batch_size = ceil(num_feat / processes)
    bottom_row = batch_size
    top_row = 0
    while top_row < num_feat:
        gdf_list.append(f_feature[top_row:bottom_row])
        top_row += batch_size
        bottom_row += batch_size
        bottom_row = min(bottom_row, num_feat)
    return gdf_list


def _grid_to_line_intersection(
    chunk: gpd.GeoDataFrame, data_array: xr.DataArray, variables: dict
) -> tuple[pd.DataFrame, gpd.GeoDataFrame]:
    """Interpolates gridded data along line geometries.

    This function iterates through each line geometry in the input
    GeoDataFrame, interpolates points along the line at a specified spacing,
    extracts gridded data values at these interpolated points, and calculates
    statistics based on these values.  It returns a DataFrame containing the
    calculated statistics and a GeoDataFrame containing the interpolated
    point geometries.

    Args:
    ----
        chunk (gpd.GeoDataFrame): GeoDataFrame containing one or more line
            geometries to interpolate along.
        data_array (xr.DataArray): xarray DataArray containing the gridded
            data to interpolate.  Can contain one or more time steps.
        variables (Dict): Dictionary containing variables required for the
            interpolation process.  This should include grid projection
            information, coordinate names, interpolation method, and
            statistic to calculate.

    Returns:
    -------
        Tuple[pd.DataFrame, gpd.GeoDataFrame]: A tuple containing:
            - stats_df (pd.DataFrame): DataFrame containing calculated
              statistics for each interpolated point along each line.
            - interp_geo_df (gpd.GeoDataFrame): GeoDataFrame containing the
              interpolated point geometries.

    """
    stats_list = []
    interp_geo_list = []

    for i in range(len(chunk)):
        line: gpd.GeoDataFrame = chunk.reset_index().loc[[i]]
        geom: gpd.GeoSeries = line.geometry.to_crs(variables["grid_proj"])

        # Either find line vertices
        if variables["spacing"] == 0:
            x, y, dist = _get_line_vertices(geom=geom, calc_crs=variables["calc_crs"], crs=variables["grid_proj"])

        # Or interpolate sample points
        else:
            x, y, dist = _interpolate_sample_points(
                geom=geom,
                spacing=variables["spacing"],
                calc_crs=variables["calc_crs"],
                crs=variables["grid_proj"],
            )
        # Get the grid values from the interpolated points
        interp_coords = {
            variables["x_coord"]: ("pt", x),
            variables["y_coord"]: ("pt", y)
        }
        interp_dataset = data_array.interp(
            **interp_coords, method=variables["interp_method"]
        )

        feature_id_array = np.full(len(dist), line[variables["id_feature"]].values[0])
        # Add distsance and polygon ids
        interp_dataset = xr.merge(
            [
                interp_dataset,
                xr.DataArray(dist, dims=["pt"], name="dist"),
                xr.DataArray(feature_id_array, dims=["pt"], name=variables["id_feature"])
            ]
        )

        interp_geo_df = _dataframe_to_geodataframe(
            interp_dataset.to_dataframe(),
            crs=variables["grid_proj"],
            x_coord=variables["x_coord"],
            y_coord=variables["y_coord"]
        )
        interp_geo_df.rename(columns={variables["varname"]: "values"}, inplace=True)
        id_feature_array = np.full(len(interp_geo_df), variables["varname"])
        interp_geo_df["varname"] = id_feature_array
        interp_geo_list.append(interp_geo_df)

        # prefer date, feature id and varname, up front of dataframe.
        if variables["t_coord"] is not None:
            out_vals: dict[str, float] = {"date": interp_dataset[variables["t_coord"]].values}
            out_vals[variables["id_feature"]] = np.full(
                out_vals[next(iter(out_vals.keys()))].shape[0],
                line[variables["id_feature"]].values[0],
            )
        else:
            out_vals: dict[str, float] = {variables["id_feature"]: line[variables["id_feature"]].values}

        out_vals["varname"] = np.full(
            out_vals[next(iter(out_vals.keys()))].shape[0],
            variables["varname"],
        )
        out_vals |= _cal_point_stats(
            data=interp_dataset[variables["varname"]],
            userdata_type=variables["class_type"],
            stat=variables["stat"],
            skipna=variables["mask_data"],
        )
        stats_list.append(pd.DataFrame().from_dict(out_vals))

    interp_geo_df: gpd.GeoDataFrame = pd.concat(interp_geo_list)
    stats_df: pd.DataFrame = pd.concat(stats_list)

    return stats_df, interp_geo_df
