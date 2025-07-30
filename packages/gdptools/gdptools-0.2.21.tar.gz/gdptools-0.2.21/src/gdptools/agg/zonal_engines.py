"""Engines for calculated zonal stats based on non-area-weighted statistics."""

import time
import warnings
from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import Any

import dask
import dask.dataframe as dd
import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import xarray as xr
from dask.distributed import Client, LocalCluster, get_client
from joblib import Parallel, delayed, parallel_backend
from pyproj import CRS
from rioxarray.exceptions import OneDimensionalRaster
from shapely.geometry import Polygon
from statsmodels.stats.weightstats import DescrStatsW
from tqdm import tqdm

from gdptools.data.agg_gen_data import AggData
from gdptools.data.user_data import UserData
from gdptools.helpers import build_subset_tiff_da
from gdptools.utils import _get_shp_bounds_w_buffer, _make_valid


def _calculate_stats(
    row: pd.Series,
    target_gdf: gpd.GeoDataFrame,
    source_ds: xr.Dataset,
    source_ds_proj: str | int | CRS,
    var_name: str,
    categorical: bool,
    stats_columns: list,
    weights_proj: str | int | CRS,
) -> dict:
    """Calculate statistics for a given zone.

    This function calculates weighted or unweighted statistics for a given zone,
    depending on whether a weights projection is provided. It handles both
    categorical and continuous data.

    Args:
    ----
        row (pd.Series): A Pandas Series representing a single zone.
        target_gdf (gpd.GeoDataFrame): A GeoDataFrame containing all zones.
        source_ds (xr.Dataset): An xarray Dataset containing the source data.
        source_ds_proj (Union[str, int, CRS]): The projection of the source dataset.
        var_name (str): The name of the variable to calculate statistics for.
        categorical (bool): A boolean indicating whether the data is categorical.
        stats_columns (list): A list of columns to calculate statistics for.
        weights_proj (Union[str, int, CRS]): The projection to use for calculating weights.

    Returns:
    -------
        dict: A dictionary containing the calculated statistics.

    """
    zone = gpd.GeoDataFrame([row], columns=target_gdf.columns, crs=target_gdf.crs)
    polys, i_pixel, j_pixel, data = _intersecting_pixels_with_shape(
        raster=source_ds,
        raster_proj=source_ds_proj,
        shape=zone,
    )
    # Check if the returned arrays are empty indicating no intersecting pixels
    if len(polys) == 0:
        # Return zero values for all statistics
        print(f"Target Polygon has no values: {row.index}")
        if categorical:
            return {cat: None for cat in stats_columns}
        else:
            return {
                "median": None,
                "mean": None,
                "count": None,
                "sum": None,
                "stddev": None,
                "sum_weights": None,
                "masked_mean": None,
            }
    # if polys.crs is not zone.crs:
    #     print("this is an error") #  Check this
    if weights_proj is not None:
        weights = _pixel_spatial_weights_in_shape(polys.to_crs(weights_proj), zone.to_crs(weights_proj))
    else:
        weights = _pixel_spatial_weights_in_shape(polys, zone)
    sub_data = data[var_name].values
    sub_data_values = sub_data[i_pixel, j_pixel]
    if categorical:
        cat_data = pd.DataFrame({"Value": sub_data_values, "Weight": weights})
        weighted_counts = cat_data.groupby("Value")["Weight"].sum().to_dict()

        # Initialize all categories with zero count
        stats = {cat: None for cat in stats_columns}

        # Update counts for categories present in the zone
        for cat, count in weighted_counts.items():
            if cat in stats:
                stats[cat] = count
        stats["top"] = max(weighted_counts, key=weighted_counts.get)

        return stats
    else:
        stats = DescrStatsW(data=sub_data_values, weights=weights)
        masked_sdv = np.ma.masked_array(sub_data_values, np.isnan(sub_data_values))
        ma_mean = np.ma.average(masked_sdv, weights=weights)
        return {
            "median": stats.quantile(0.5, return_pandas=False)[0],
            "mean": stats.mean,
            "count": len(weights),
            "sum": stats.sum,
            "stddev": stats.std_mean,
            "sum_weights": stats.sum_weights,
            "masked_mean": ma_mean,
        }


def process_chunk(
    chunk: gpd.GeoDataFrame,
    source_ds: xr.Dataset,
    source_ds_proj: str | int | CRS,
    var: str,
    categorical: bool,
    stats_columns: list,
    weights_proj: str | int | CRS,
    chunk_id: int,
) -> dict:
    """Process a chunk of the target GeoDataFrame.

    This function processes a chunk of the target GeoDataFrame and calculates
    zonal statistics for each zone in the chunk. It handles both categorical
    and continuous data and supports weighted statistics.

    Args:
    ----
        chunk (gpd.GeoDataFrame): Chunk of the target GeoDataFrame.
        source_ds (xr.Dataset): The source xarray Dataset.
        source_ds_proj (Union[str, int, CRS]): Projection of the source Dataset.
        var (str): Name of the variable in source_ds to compute stats for.
        categorical (bool): True if the variable is categorical.
        stats_columns (list): List of columns to calculate statistics for.
        weights_proj (Union[str, int, CRS]): Projection to use for weighting.
        chunk_id (int): ID of the current chunk.

    Returns:
    -------
        dict: Dictionary of calculated statistics for each zone.

    """
    warnings.simplefilter("ignore", FutureWarning)
    warnings.simplefilter("ignore", RuntimeWarning)
    ngdf_chunk = chunk.copy()
    # for col in stats_columns:
    #     ngdf_chunk[col] = np.nan
    result_dict = {}
    partition_index = chunk.iloc[0]["partition_index"]
    for i, row in tqdm(chunk.iterrows(), total=chunk.shape[0], desc=f"Processing chunk: {partition_index}"):
        zone = gpd.GeoDataFrame([row], columns=chunk.columns, crs=chunk.crs)
        polys, i_pixel, j_pixel, data = _intersecting_pixels_with_shape(
            raster=source_ds, raster_proj=source_ds_proj, shape=zone
        )
        # Check if the returned arrays are empty indicating no intersecting pixels
        if len(polys) == 0:
            print(f"skipping: {i}")
            for col in stats_columns:
                ngdf_chunk.at[i, col] = None
            continue
        if source_ds_proj is not None:
            weights = _pixel_spatial_weights_in_shape(polys.to_crs(weights_proj), zone.to_crs(weights_proj))
        else:
            weights = _pixel_spatial_weights_in_shape(polys, zone)
        sub_data = data[var].values
        sub_data_values = sub_data[i_pixel, j_pixel]

        if categorical:
            cat_data = pd.DataFrame({"Value": sub_data_values, "Weight": weights})
            weighted_counts = cat_data.groupby("Value")["Weight"].sum()
            weighted_counts_dict = weighted_counts.to_dict()

            # Initialize all categories with zero count
            stats = {cat: None for cat in stats_columns}

            # Update counts for categories present in the zone
            for cat, count in weighted_counts_dict.items():
                if cat in stats_columns:
                    stats[cat] = count
            stats["top"] = weighted_counts.idxmax()

        else:
            dstats = DescrStatsW(data=sub_data_values, weights=weights)
            masked_sdv = np.ma.masked_array(sub_data_values, np.isnan(sub_data_values))
            ma_mean = np.ma.average(masked_sdv, weights=weights)
            stats = {
                "median": dstats.quantile(0.5, return_pandas=False)[0],
                "mean": dstats.mean,
                "count": len(weights),
                "sum": dstats.sum,
                "stddev": dstats.std_mean,
                "sum_weights": dstats.sum_weights,
                "masked_mean": ma_mean,
            }
        result_dict[i] = stats

    return result_dict


def _intersecting_pixels_with_shape(
    raster: xr.Dataset,
    raster_proj: str | int | CRS,
    shape: gpd.GeoDataFrame,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, xr.Dataset]:
    """Find intersecting pixels between a raster and a shape.

    This function takes a raster dataset, its projection, and a shape,
    and returns the intersecting pixels, their indices, and the clipped raster.

    Args:
    ----
        raster (xr.Dataset): The raster dataset.
        raster_proj (Union[str, int, CRS]): The projection of the raster.
        shape (gpd.GeoDataFrame): The shape to intersect with.

    Returns:
    -------
        Tuple[np.ndarray, np.ndarray, np.ndarray, xr.Dataset]: A tuple containing the
            intersecting pixel geometries, their row indices, their column indices,
            and the clipped raster dataset.

    """
    # Clip the raster to the shape.
    # If bounds are not in the correct format (floats), convert them
    # Reproject shape into raster projection
    shape = shape.to_crs(raster_proj)
    try:
        bounds = shape.iloc[0].geometry.bounds
        box = raster.rio.clip_box(*bounds)
    except OneDimensionalRaster as e:
        # Handle the exception
        print(f"Target Polygon has no intersections: {e}")
        # You can choose to return a default value or raise a custom exception
        # For example, return an empty dataset or handle it as per your use case
        return np.array([]), np.array([]), np.array([]), xr.Dataset()
    tlon = box["x"]  # These are cell centre coordinates
    tlat = box["y"]  # These are cell centre coordinates

    # Work with fractions of integer cell indices to get node locations.
    # i.e. -0.5 and 0.5 are first cells nodes using the transform of the CRS
    lon, lat = np.meshgrid(np.arange(-0.5, tlon.size + 0.5), np.arange(-0.5, tlat.size + 0.5))

    # These are 2D arrays to handle non-uniformly increasing projections on cell sizes.
    xs, ys = rasterio.transform.xy(box.rio.transform(), lat, lon)
    ys = np.asarray(ys)  # These are cell nodal coordinates
    xs = np.asarray(xs)  # These are cell nodal coordinates

    # Ensure they are 2D, not flattened due to edge clipping
    if xs.ndim == 1:
        expected_shape = lon.shape  # from np.meshgrid
        xs = xs.reshape(expected_shape)
        ys = ys.reshape(expected_shape)

    # Create the numpy array of the rasterized polygon's pixels
    # I dont like this double loop.  But we are stuck with this granularity
    # due to how shapely is written.
    polys = np.empty(tlat.size * tlon.size, dtype=object)
    k = 0
    for i in range(tlat.size):
        for j in range(tlon.size):
            polys[k] = Polygon(
                [
                    [xs[i, j], ys[i, j]],
                    [xs[i + 1, j], ys[i + 1, j]],
                    [xs[i + 1, j + 1], ys[i + 1, j + 1]],
                    [xs[i, j + 1], ys[i, j + 1]],
                ]
            )
            k += 1

    # Create the dataframe.  No need for pixel i,j
    # since we can use unravel_index later using the tgt indices
    df = gpd.GeoDataFrame(geometry=polys, crs=raster_proj)
    i_pixels_in_zone, _ = shape.sindex.query(polys, predicate="intersects")

    # we have the global index into the pixels of the zone,
    # unravel them using the size of the bounding box of the zone.
    i_pixel, j_pixel = np.unravel_index(i_pixels_in_zone, (tlat.size, tlon.size))
    return df.geometry.values[i_pixels_in_zone], i_pixel, j_pixel, box


def _pixel_spatial_weights_in_shape(
    polygons: gpd.array.GeometryArray, shape: gpd.GeoDataFrame
) -> np.ndarray:
    """Calculate the spatial weights of pixels within a shape.

    This function calculates the normalized intersection weights of a set of
    pixel polygons with a given shape. The weights represent the proportion
    of each pixel's area that intersects with the shape.

    Args:
    ----
        polygons (gpd.array.GeometryArray): An array of pixel polygons.
        shape (gpd.GeoDataFrame): The shape to calculate weights against.

    Returns:
    -------
        np.ndarray: An array of normalized intersection weights.

    """
    # Normalized intersection weights
    return (polygons.intersection(shape.iloc[0].geometry).area) / shape.iloc[0].geometry.area


class ZonalEngine(ABC):
    """Base class for zonal stats engines."""

    def calc_zonal_from_aggdata(
        self,
        user_data: UserData,
        categorical: bool = False,
        jobs: int = 1,
    ) -> pd.DataFrame:
        """Calculate zonal statistics from aggregated data.

        This function calculates zonal statistics from pre-aggregated data.
        It sets up the necessary parameters and calls the zonal_stats method.

        Args:
        ----
            user_data (UserData): The user data object.
            categorical (bool, optional): Whether the data is categorical. Defaults to False.
            jobs (int, optional): Number of jobs for parallel processing. Defaults to 1.

        Returns:
        -------
            pd.DataFrame: A DataFrame containing the zonal statistics.

        """
        self._user_data = user_data
        self._categorical = categorical
        self._jobs = jobs

        return self.zonal_stats()

    def calc_weights_zonal_from_aggdata(
        self,
        user_data: UserData,
        crs: str | int | CRS = 6931,
        categorical: bool = False,
        jobs: int = 1,
    ) -> gpd.GeoDataFrame:
        """Calculate weighted zonal statistics from aggregated data.

        This function sets up the necessary parameters and calls the
        weighted_zonal_stats method to calculate weighted zonal statistics.

        Args:
        ----
            user_data (UserData): The user data object.
            crs (Union[str, int, CRS], optional): The CRS for weighting. Defaults to 6931.
            categorical (bool, optional): Whether the data is categorical. Defaults to False.
            jobs (int, optional): Number of jobs for parallel processing. Defaults to 1.

        Returns:
        -------
            gpd.GeoDataFrame: A GeoDataFrame containing the weighted zonal statistics.

        """
        self._user_data = user_data
        self._weight_gen_crs = crs
        self._categorical = categorical
        self._jobs = jobs

        return self.weighted_zonal_stats()

    @abstractmethod
    def zonal_stats(self) -> pd.DataFrame:
        """Calculate zonal statistics serially.

        This function calculates zonal statistics based on the provided input data. It handles
        both categorical and continuous data, performing spatial joins and calculating
        summary statistics. Missing values are filled using nearest neighbor imputation.

        Returns
        -------
            pd.DataFrame: A DataFrame containing the calculated zonal statistics.

        """
        """Abstract method for calculating zonal stats."""
        pass

    @abstractmethod
    def weighted_zonal_stats(self) -> gpd.GeoDataFrame:
        """Calculate weighted zonal statistics in parallel.

        This function calculates weighted zonal statistics for each zone in the input
        GeoDataFrame using parallel processing. It divides the GeoDataFrame into chunks
        and processes each chunk concurrently.

        Returns
        -------
            gpd.GeoDataFrame: A GeoDataFrame containing the weighted zonal statistics.

        """
        """Calculate weighted zonal statistics for each zone in the GeoDataFrame.

        This function calculates weighted zonal statistics for each zone in the input
        GeoDataFrame. It uses the provided user data, CRS, and other parameters to
        perform the calculations.

        Returns:
            gpd.GeoDataFrame: A GeoDataFrame containing the weighted zonal statistics.
        """
        """Abstract method for calculating weighted zonal stats."""
        pass


class ZonalEngineSerial(ZonalEngine):
    """Serial zonal stats engine."""

    def weighted_zonal_stats(self) -> gpd.GeoDataFrame:
        """Calculate weighted zonal statistics for each zone in the GeoDataFrame.

        This function calculates weighted zonal statistics for each zone in the input
        GeoDataFrame. It uses the provided user data, CRS, and other parameters to
        perform the calculations.

        Returns
        -------
            gpd.GeoDataFrame: A GeoDataFrame containing the weighted zonal statistics.

        """
        tqdm.pandas(desc="Applying zonal stats")
        zvars = self._user_data.get_vars()
        tstrt = time.perf_counter()
        agg_data = self._user_data.prep_agg_data(zvars[0])
        tend = time.perf_counter()
        print(f"data prepped for zonal in {tend - tstrt:0.4f} seconds")
        var_name = zvars[0]
        source_ds = agg_data.da.to_dataset(name=var_name)
        target_gdf = agg_data.feature
        if self._categorical:
            data_array = agg_data.da.values
            filtered_data_array = data_array[~np.isnan(data_array)]
            unique_categories = np.unique(filtered_data_array)
            stats_columns = [*unique_categories.tolist(), "top"]
        else:
            stats_columns = ["median", "mean", "count", "sum", "stddev", "sum_weights", "masked_mean"]
        target_gdf[stats_columns] = target_gdf.progress_apply(
            lambda row: _calculate_stats(
                row=row,
                target_gdf=target_gdf,
                source_ds=source_ds,
                source_ds_proj=self._user_data.proj_ds,
                var_name=var_name,
                categorical=self._categorical,
                stats_columns=stats_columns,
                weights_proj=self._weight_gen_crs,
            ),
            axis=1,
            result_type="expand",
        )
        return target_gdf

    def zonal_stats(self) -> pd.DataFrame:
        """Calculate zonal statistics serially.

        This function calculates zonal statistics based on the provided input data. It handles
        both categorical and continuous data, performing spatial joins and calculating
        summary statistics. Missing values are filled using nearest neighbor imputation.

        Returns
        -------
            pd.DataFrame: A DataFrame containing the calculated zonal statistics.

        """
        # Step 1: Get variable name, and aggregate data object (raster and polygons)
        zvars = self._user_data.get_vars()
        tstrt = time.perf_counter()
        agg_data: AggData = self._user_data.prep_agg_data(zvars[0])
        tend = time.perf_counter()
        print(f"data prepped for zonal in {tend - tstrt:0.4f} seconds")
        ds_ss = agg_data.da

        # Step 2: If categorical, get unique classes
        if self._categorical:
            d_categories = list(pd.Categorical(ds_ss.values.flatten()).categories)

        # Step 3: Convert raster to table of points
        tstrt = time.perf_counter()
        lon, lat = np.meshgrid(
            ds_ss[agg_data.cat_cr.X_name].values,
            ds_ss[agg_data.cat_cr.Y_name].values,
        )
        lat_flat = lat.flatten()
        lon_flat = lon.flatten()
        ds_vals = ds_ss.values.flatten()
        df_points = pd.DataFrame(
            {
                "index": np.arange(len(lat_flat)),
                "vals": ds_vals,
                "lat": lat_flat,
                "lon": lon_flat,
            }
        )

        # Remove fill values
        try:
            fill_val = ds_ss._FillValue
            df_points_filt = df_points[df_points.vals != fill_val]
        except Exception:
            df_points_filt = df_points

        source_df = gpd.GeoDataFrame(
            df_points_filt,
            geometry=gpd.points_from_xy(df_points_filt.lon, df_points_filt.lat),
        )
        tend = time.perf_counter()
        print(f"converted tiff to points in {tend - tstrt:0.4f} seconds")

        # Step 4: Make points GeoDataFrame and ensure CRS
        source_df.set_crs(agg_data.cat_cr.proj, inplace=True)
        target_df = agg_data.feature.to_crs(agg_data.cat_cr.proj)
        target_df = _make_valid(target_df)
        target_df.reset_index()
        target_df_keys = target_df[agg_data.id_feature].values

        # Step 5: Spatial join: which points fall in which polygons?
        tstrt = time.perf_counter()
        ids_tgt, ids_src = source_df.sindex.query(target_df.geometry, predicate="contains")
        tend = time.perf_counter()
        print(f"overlaps calculated in {tend - tstrt:0.4f} seconds")

        # Step 6: Aggregate stats by polygon
        if self._categorical:
            # For categorical: calculate fraction of each category per polygon
            val_series = pd.Categorical(source_df["vals"].iloc[ids_src], categories=d_categories)
            agg_df = pd.DataFrame({agg_data.id_feature: target_df[agg_data.id_feature].iloc[ids_tgt].values})
            agg_df["vals"] = val_series
            unique_vals = np.unique(ds_vals)
            del val_series
            tstrt = time.perf_counter()
            vals_dict = agg_df.groupby(agg_data.id_feature)["vals"].apply(list).to_dict()

            comp_stats = []
            for key in vals_dict.keys():
                unique, frequency = np.unique(np.array(vals_dict[key]), return_counts=True)
                total_count = frequency.sum()
                # Loop through each category and calculate the percentage
                zonal_dict = {}
                # for u,f in zip(unique, frequency):
                #     zonal_dict[u]=[f / total_count]
                # flake8: noqa: B905
                zonal_dict = {unique_value: f / total_count for unique_value, f in zip(unique, frequency)}

                stat = pd.DataFrame(zonal_dict, dtype=float, columns=unique_vals, index=["0"]).fillna(0.0)
                stat["count"] = total_count
                stat[agg_data.id_feature] = key
                comp_stats.append(stat)

            stats = pd.concat(comp_stats)
            stats = stats.set_index(agg_data.id_feature)
            tend = time.perf_counter()
            print(f"categorical zonal stats calculated in {tend - tstrt:0.4f} seconds")

        else:
            # For continuous: group and describe values per polygon
            agg_df = pd.DataFrame(
                {
                    agg_data.id_feature: target_df[agg_data.id_feature].iloc[ids_tgt].values,
                    "vals": source_df["vals"].iloc[ids_src],
                }
            )
            tstrt = time.perf_counter()
            # Group the values by the polygon, run Pandas descibe() on each group of values, and round to 10 decimals
            stats = agg_df.groupby(agg_data.id_feature)["vals"].describe()  # .map(lambda x: np.float64(f"{x:0.10f}"))
            stats["sum"] = agg_df.groupby(agg_data.id_feature).sum()
            tend = time.perf_counter()
            print(f"zonal stats calculated in {tend - tstrt:0.4f} seconds")

        # Step 7: Fill missing polygons with stats from nearest neighbor
        tstrt = time.perf_counter()
        stats_inds = stats.index
        missing = np.setdiff1d(target_df_keys, stats_inds)
        target_df_stats = target_df.loc[target_df[agg_data.id_feature].isin(list(stats_inds))]
        target_df_missing = target_df.loc[target_df[agg_data.id_feature].isin(list(missing))]
        nearest = target_df_stats.sindex.nearest(target_df_missing.geometry, return_all=False)
        print(nearest)
        print(f"number of missing values: {len(missing)}")
        stats_missing = stats.iloc[nearest[1]]
        stats_missing.index = missing
        stats_tot = pd.concat([stats, stats_missing])
        stats_tot.index.name = agg_data.id_feature
        tend = time.perf_counter()
        print(f"fill missing values with nearest neighbors in {tend - tstrt:0.4f} seconds")

        return stats_tot


class ZonalEngineParallel(ZonalEngine):
    """Parallel zonal stats engine."""

    def weighted_zonal_stats(self) -> gpd.GeoDataFrame:
        """Calculate weighted zonal statistics in parallel.

        This function calculates weighted zonal statistics for each zone in the input
        GeoDataFrame using parallel processing. It divides the GeoDataFrame into chunks
        and processes each chunk concurrently.

        Returns
        -------
            gpd.GeoDataFrame: A GeoDataFrame containing the weighted zonal statistics.

        """
        zvars = self._user_data.get_vars()
        tstrt = time.perf_counter()
        agg_data: AggData = self._user_data.prep_agg_data(zvars[0])
        tend = time.perf_counter()
        print(f"data prepped for zonal in {tend - tstrt:0.4f} seconds")
        source_ds = agg_data.da.to_dataset(name=self._user_data.get_vars()[0])
        # source_ds = source_ds.rio.reproject(self._weight_gen_crs)
        target_gdf = agg_data.feature  # .to_crs(self._weight_gen_crs)
        target_gdf["partition_index"] = [i // (len(target_gdf) // self._jobs) for i in range(len(target_gdf))]
        if self._categorical:
            data_array = agg_data.da.values
            filtered_data_array = data_array[~np.isnan(data_array)]
            unique_categories = np.unique(filtered_data_array)
            stats_columns = [*unique_categories.tolist(), "top"]
        else:
            stats_columns = ["median", "mean", "count", "sum", "stddev", "sum_weights", "masked_mean"]
        chunk_size = len(target_gdf) // self._jobs + 1
        # Split target_gdf into chunks
        chunks = [target_gdf.iloc[i : i + chunk_size] for i in range(0, len(target_gdf), chunk_size)]

        # Process each chunk in parallel
        results = Parallel(n_jobs=self._jobs)(
            delayed(process_chunk)(
                chunk,
                source_ds,
                self._user_data.proj_ds,
                zvars[0],
                self._categorical,
                stats_columns,
                self._weight_gen_crs,
                chunk_id=i,
            )
            for i, chunk in enumerate(chunks)
        )
        for d in results:
            for index, row_data in d.items():
                for col, value in row_data.items():
                    target_gdf.at[index, col] = value
        return pd.DataFrame(target_gdf)

    def zonal_stats(self) -> pd.DataFrame:
        """Calculate zonal statistics in parallel using a parallel backend.

        This function calculates zonal statistics for each zone in the input GeoDataFrame
        using parallel processing with a specified parallel backend. It handles both
        categorical and continuous data and performs missing value imputation using
        nearest neighbors.

        Returns
        -------
            pd.DataFrame: A DataFrame containing the calculated zonal statistics.

        """
        n_jobs: int = self._jobs
        # n_jobs = 2
        zvars = self._user_data.get_vars()
        tstrt = time.perf_counter()
        agg_data: AggData = self._user_data.prep_agg_data(zvars[0])
        tend = time.perf_counter()
        print(f"data prepped for parallel zonal stats in {tend - tstrt:0.4f} seconds")
        ds_ss = agg_data.da

        target_df = agg_data.feature.to_crs(agg_data.cat_cr.proj)
        target_df = _make_valid(target_df)
        target_df_keys = target_df[agg_data.id_feature].values
        to_workers = _chunk_dfs(
            geoms_to_chunk=target_df,
            df=ds_ss,
            x_name=agg_data.cat_cr.X_name,
            y_name=agg_data.cat_cr.Y_name,
            proj=agg_data.cat_cr.proj,
            ttb=agg_data.cat_cr.toptobottom,
            id_feature=agg_data.id_feature,
            categorical=self._categorical,
            n_jobs=n_jobs,
        )

        tstrt = time.perf_counter()
        worker_out = self.get_stats_parallel(n_jobs, to_workers)
        for i in range(len(worker_out)):
            if i == 0:
                stats = worker_out[i]
                print(type(stats))
            else:
                stats = pd.concat([stats, worker_out[i]])
        stats.set_index(agg_data.id_feature, inplace=True)
        # stats = pd.concat(worker_out)
        tend = time.perf_counter()
        print(f"Parallel calculation of zonal stats in {tend - tstrt:0.04} seconds")

        tstrt = time.perf_counter()
        stats_inds = stats.index

        missing = np.setdiff1d(target_df_keys, stats_inds)
        if len(missing) <= 0:
            return stats
        target_df_stats = target_df.loc[target_df[agg_data.id_feature].isin(list(stats_inds))]
        target_df_missing = target_df.loc[target_df[agg_data.id_feature].isin(list(missing))]
        nearest = target_df_stats.sindex.nearest(target_df_missing.geometry, return_all=False)
        print(nearest)
        print(f"number of missing values: {len(missing)}")
        stats_missing = stats.iloc[nearest[1]]
        stats_missing.index = missing
        stats_tot = pd.concat([stats, stats_missing])
        stats_tot.index.name = agg_data.id_feature
        tend = time.perf_counter()
        print(f"fill missing values with nearest neighbors in {tend - tstrt:0.4f} seconds")

        return stats_tot

    def get_stats_parallel(
        self,
        n_jobs: int,
        to_workers: Generator[
            tuple[gpd.GeoDataFrame, xr.DataArray, str, str, Any, int, bool, str],
            None,
            None,
        ],
    ) -> list[pd.DataFrame]:
        """Calculate statistics in parallel using a parallel backend.

        This function calculates statistics for each chunk of data in parallel using
        the specified parallel backend. It uses the 'loky' backend with a maximum
        of one thread per worker.

        Args:
        ----
            n_jobs (int): The number of jobs to run in parallel.
            to_workers (Generator[Tuple[gpd.GeoDataFrame, xr.DataArray, str, str, Any, int, bool, str], None, None]):
                A generator that yields tuples of data for each worker.

        Returns:
        -------
            list[pd.DataFrame]: A list of DataFrames, where each DataFrame contains the
                calculated statistics for a chunk of data.

        """
        with parallel_backend("loky", inner_max_num_threads=1):
            worker_out = Parallel(n_jobs=n_jobs)(delayed(_get_stats_on_chunk)(*chunk_pair) for chunk_pair in to_workers)
        return worker_out


class ZonalEngineDask(ZonalEngine):
    """Parallel zonal stats engine."""

    def weighted_zonal_stats(self) -> gpd.GeoDataFrame:
        """Calculate weighted zonal statistics using Dask.

        This function calculates weighted zonal statistics for each zone in the input
        GeoDataFrame using Dask for parallel processing. It partitions the data and
        processes each partition concurrently.

        Returns
        -------
            gpd.GeoDataFrame: A GeoDataFrame containing the weighted zonal statistics.

        """
        dask_create = False
        try:
            client = get_client()
        except ValueError:
            # If no client exists, you can either create a new one or handle it accordingly
            cluster = LocalCluster(n_workers=self._jobs)
            client = Client(cluster)  # This line creates a new client, which might not be desirable in all cases
            dask_create = True

        zvars = self._user_data.get_vars()
        tstrt = time.perf_counter()
        agg_data: AggData = self._user_data.prep_agg_data(zvars[0])
        tend = time.perf_counter()
        print(f"data prepped for zonal in {tend - tstrt:0.4f} seconds")
        source_ds = agg_data.da.to_dataset(name=self._user_data.get_vars()[0])
        # source_ds_scat = client.scatter(source_ds, broadcast=True)
        # source_ds = source_ds.rio.reproject(self._weight_gen_crs)
        target_gdf = agg_data.feature  # .to_crs(self._weight_gen_crs)
        target_gdf["partition_index"] = [i // (len(target_gdf) // self._jobs) for i in range(len(target_gdf))]
        ddf = dd.from_pandas(target_gdf, npartitions=self._jobs)
        # Extract unique categories if categorical data
        if self._categorical:
            data_array = agg_data.da.values
            filtered_data_array = data_array[~np.isnan(data_array)]
            unique_categories = np.unique(filtered_data_array)
            stats_columns = [*unique_categories.tolist(), "top"]
        else:
            stats_columns = ["median", "mean", "count", "sum", "stddev", "sum_weights", "masked_mean"]

        result = ddf.map_partitions(
            process_chunk,
            source_ds,
            self._user_data.proj_ds,
            zvars[0],
            self._categorical,
            stats_columns,
            self._weight_gen_crs,
            1,
            meta=dict,
        )
        compute_result = result.compute()
        print("Finished Compute", flush=True)
        # Update the main DataFrame with the processed values
        ngdf = target_gdf.copy()
        for d in compute_result:
            for index, row_data in d.items():
                for col, value in row_data.items():
                    ngdf.at[index, col] = value
        if dask_create:
            cluster.close()
            client.close()
        return pd.DataFrame(ngdf)

    def zonal_stats(self) -> pd.DataFrame:
        """Calculate zonal statistics using Dask.

        This function calculates zonal statistics for each zone in the input GeoDataFrame
        using Dask for parallel processing. It handles both categorical and continuous
        data and performs missing value imputation using nearest neighbors.

        Returns
        -------
            pd.DataFrame: A DataFrame containing the calculated zonal statistics.

        """
        n_jobs: int = self._jobs
        # n_jobs = 2
        zvars = self._user_data.get_vars()
        tstrt = time.perf_counter()
        agg_data: AggData = self._user_data.prep_agg_data(zvars[0])
        tend = time.perf_counter()
        print(f"data prepped for zonal in {tend - tstrt:0.4f} seconds")
        ds_ss = agg_data.da

        target_df = agg_data.feature.to_crs(agg_data.cat_cr.proj)
        target_df = _make_valid(target_df)
        # target_df.reset_index(inplace=True)
        target_df_keys = target_df[agg_data.id_feature].values
        to_workers = _chunk_dfs(
            geoms_to_chunk=target_df,
            df=ds_ss,
            x_name=agg_data.cat_cr.X_name,
            y_name=agg_data.cat_cr.Y_name,
            proj=agg_data.cat_cr.proj,
            ttb=agg_data.cat_cr.toptobottom,
            id_feature=agg_data.id_feature,
            categorical=self._categorical,
            n_jobs=n_jobs,
        )

        tstrt = time.perf_counter()
        worker_out = _get_stats_dask(to_workers)
        for i in range(len(worker_out[0])):
            if i == 0:
                stats = worker_out[0][i]
                print(type(stats))
            else:
                stats = pd.concat([stats, worker_out[0][i]])
        stats.set_index(agg_data.id_feature, inplace=True)
        # stats = pd.concat(worker_out)
        tend = time.perf_counter()
        print(f"Parallel calculation of zonal stats in {tend - tstrt:0.04} seconds")

        tstrt = time.perf_counter()
        stats_inds = stats.index

        missing = np.setdiff1d(target_df_keys, stats_inds)
        if len(missing) <= 0:
            return stats
        target_df_stats = target_df.loc[target_df[agg_data.id_feature].isin(list(stats_inds))]
        target_df_missing = target_df.loc[target_df[agg_data.id_feature].isin(list(missing))]
        nearest = target_df_stats.sindex.nearest(target_df_missing.geometry, return_all=False)
        print(nearest)
        print(f"number of missing values: {len(missing)}")
        stats_missing = stats.iloc[nearest[1]]
        stats_missing.index = missing
        stats_tot = pd.concat([stats, stats_missing])
        stats_tot.index.name = agg_data.id_feature
        tend = time.perf_counter()
        print(f"fill missing values with nearest neighbors in {tend - tstrt:0.4f} seconds")

        return stats_tot


def _get_stats_dask(
    to_workers: Generator[
        tuple[gpd.GeoDataFrame, xr.DataArray, str, str, Any, int, bool, str],
        None,
        None,
    ],
) -> pd.DataFrame:
    """Calculate statistics using Dask.

    This function calculates statistics for each chunk of data in parallel using Dask.
    It takes a generator of worker inputs and returns a list of DataFrames containing
    the calculated statistics.

    Args:
    ----
        to_workers (Generator[Tuple[gpd.GeoDataFrame, xr.DataArray, str, str, Any, int, bool, str], None, None]):
            A generator that yields tuples of data for each worker.

    Returns:
    -------
        list[pd.DataFrame]: A list of DataFrames, where each DataFrame contains the
            calculated statistics for a chunk of data.

    """
    worker_out = [dask.delayed(_get_stats_on_chunk)(*worker) for worker in to_workers]
    return dask.compute(worker_out)

def _get_stats_on_chunk(
    geom: gpd.GeoDataFrame,
    df: xr.DataArray,
    x_name: str,
    y_name: str,
    proj: str | int | CRS,
    toptobottom: int,
    categorical: bool,
    id_feature: str,
) -> pd.DataFrame:
    """Calculate statistics on a chunk of data.

    This function calculates statistics for a given chunk of geometry and data.
    It performs spatial operations to determine which data points fall within
    each geometry and then calculates summary statistics.

    Args:
    ----
        geom (gpd.GeoDataFrame): The geometry data.
        df (xr.DataArray): The data as an xarray DataArray.
        x_name (str): Name of the x-coordinate.
        y_name (str): Name of the y-coordinate.
        proj (Union[str, int, CRS]): The projection of the data.
        toptobottom (int): Whether the image is top to bottom.
        categorical (bool): True if the data is categorical.
        id_feature (str): Name of the ID feature.

    Returns:
    -------
        pd.DataFrame: The calculated statistics.

    """
    num_features = len(geom.index)
    comp_stats = []
    unique_vals = np.unique(df.values)
    for index in range(num_features):
        target_df = geom.iloc[[index]]
        feat_bounds = _get_shp_bounds_w_buffer(gdf=target_df, ds=df, crs=proj, lon=x_name, lat=y_name)

        subset_dict = build_subset_tiff_da(bounds=feat_bounds, xname=x_name, yname=y_name, toptobottom=toptobottom)
        ds_ss = df.sel(**subset_dict)
        lon, lat = np.meshgrid(
            ds_ss[x_name].values,
            ds_ss[y_name].values,
        )
        lat_flat = lat.flatten()
        lon_flat = lon.flatten()
        ds_vals = ds_ss.values.flatten()  # type: ignore
        df_points = pd.DataFrame(
            {
                "index": np.arange(len(lat_flat)),
                "vals": ds_vals,
                "lat": lat_flat,
                "lon": lon_flat,
            }
        )
        try:
            fill_val = ds_ss._FillValue
            df_points = df_points[df_points.vals != fill_val]
        except Exception:
            df_points = df_points

        source_df = gpd.GeoDataFrame(
            df_points,
            geometry=gpd.points_from_xy(df_points.lon, df_points.lat),
            crs=proj,
        )

        ids_src = source_df.sindex.query(target_df.geometry.values[0], predicate="contains")
        if categorical:
            # Get unique values
            cats = list(pd.Categorical(source_df["vals"].iloc[ids_src]).categories)
            # Get the list of the values within the polygon
            val_series = list(pd.Categorical(source_df["vals"].iloc[ids_src], categories=cats))
            # Count each value
            unique, frequency = np.unique(val_series, return_counts=True)
            # Sum the total number of cells within the polygon
            total_count = frequency.sum()
            # Loop through each category and calculate the percentage
            zonal_dict = {}
            # for u,f in zip(unique, frequency):
            #     zonal_dict[u]=[f / total_count]
            # flake8: noqa: B905
            zonal_dict = {u: f / total_count for u, f in zip(unique, frequency)}

            stats = pd.DataFrame(zonal_dict, dtype=float, columns=unique_vals, index=["0"]).fillna(0.0)
            stats["count"] = total_count

        else:
            agg_df = pd.DataFrame(
                data={
                    "vals": source_df["vals"].iloc[ids_src].values,
                }
            )
            # Group the values by the polygon, run Pandas descibe() on each group of values, and round to 10 decimals
            stats = agg_df.describe().T  # .map(lambda x: np.float64(f"{x:0.10f}")).T
            stats["sum"] = agg_df["vals"].sum()
        # Add the polygon ID
        stats[id_feature] = target_df[id_feature].values[0]
        if stats["count"].values[0] <= 0:
            continue

        comp_stats.append(stats)

    # Merge all the rows and return the output
    return pd.concat(comp_stats)


def _chunk_dfs(
    geoms_to_chunk: gpd.GeoDataFrame,
    df: xr.DataArray,
    x_name: str,
    y_name: str,
    proj: str | int | CRS,
    ttb: int,
    id_feature: str,
    categorical: bool,
    n_jobs: int,
) -> Generator[
    tuple[gpd.GeoDataFrame, xr.DataArray, str, str, Any, int, bool, str],
    None,
    None,
]:
    """Chunk GeoDataFrames for parallel processing.

    This function takes a GeoDataFrame and splits it into chunks for parallel processing.
    It returns a generator that yields tuples of data for each worker.

    Args:
    ----
        geoms_to_chunk (gpd.GeoDataFrame): The GeoDataFrame to chunk.
        df (xr.DataArray): The xarray DataArray containing the data.
        x_name (str): The name of the x-coordinate.
        y_name (str): The name of the y-coordinate.
        proj (Union[str, int, CRS]): The projection of the data.
        ttb (int): Whether the image is top to bottom.
        id_feature (str): The name of the ID feature.
        categorical (bool): True if the data is categorical.
        n_jobs (int): The number of jobs to run in parallel.

    Yields:
    ------
        Generator[Tuple[gpd.GeoDataFrame, xr.DataArray, str, str, Any, int, bool, str], None, None]:
            A generator that yields tuples of data for each worker.

    """
    start = 0
    chunk_size = geoms_to_chunk.shape[0] // n_jobs + 1

    for i in range(n_jobs):
        start = i * chunk_size
        yield geoms_to_chunk.iloc[start : start + chunk_size], df, x_name, y_name, proj, ttb, categorical, id_feature
