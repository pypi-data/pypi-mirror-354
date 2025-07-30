"""Calculate weights."""

import time
from typing import Literal

import geopandas as gpd
import pandas as pd
from pyproj import CRS

from gdptools.data.user_data import UserData
from gdptools.data.weight_gen_data import WeightData
from gdptools.weights.calc_weight_engines import DaskWghtGenEngine, ParallelWghtGenEngine, SerialWghtGenEngine

WEIGHT_GEN_METHODS = Literal["serial", "parallel", "dask"]
"""Specifies the methods available for weight generation in the `WeightGen` class.

Methods:
    - `serial`: Iterates through each polygon one by one to calculate weights.
                This is generally sufficient for most use-cases.

    - `parallel`: Divides the polygons into chunks and distributes them across
                  available CPU cores for parallel processing. This method offers
                  a significant speedup when dealing with a large number of polygons.

    - `dask`: Utilizes Dask for distributed computing to perform weighted-area
              aggregation. This method is effective when a Dask client is available.

Raises:
    TypeError: Raised if the specified method is not one of "serial", "parallel", or "dask".

Returns:
    str: The method used for weight generation.

Note:
    Choose the method that best suits your computational resources and problem size.
"""


class WeightGen:
    """Class for calculating weights based on user data and specified methods.

    This class is designed to calculate weights for a given UserData object.
    The weights are calculated using the `calculate_weights` method and are
    returned as a pandas DataFrame. The DataFrame can optionally be saved to
    a .csv file for future use.

    Attributes
    ----------
        user_data (UserData): The user data for which weights are to be calculated.
            Must be an instance of one of the UserData base class such as UserCatData, NHGFStacData,
            ClimateCatData.
        method (str): The method used for weight calculation. Must be one of the values
            defined in WEIGHT_GEN_METHODS.
        weight_gen_crs (Any): The coordinate reference system to be used. Accepts any
            projection that can be used by pyproj.CRS.from_user_input.
        output_file (str, optional): The path to the output file where the DataFrame will
            be saved. If None, no output file will be created. Default is None.
        jobs (int, optional): The number of processors to be used for parallel or dask
            methods. Default is -1, which means the number of processors available divided
            by 2 will be used.
        verbose (bool, optional): If True, additional output will be printed during
            execution. Default is False.

    Methods
    -------
        calculate_weights(): Calculates the weights based on the specified method and
            user data.

    Raises
    ------
        TypeError: If the `method` attribute is not one of the values defined in
            WEIGHT_GEN_METHODS.

    """

    def __init__(
        self,
        *,
        user_data: UserData,
        method: str,
        weight_gen_crs: str | int | CRS,
        output_file: str | None | None = None,
        jobs: int | None = -1,
        verbose: bool | None = False,
    ) -> None:
        """Initialize the WeightGen class with the given parameters.

        Args:
        ----
            user_data (UserData): The user data for which weights are to be calculated.
                Must be an instance of one of the following classes: UserCatData,
                NHGFStacData, ClimateCatData.
            method (str): The method used for weight calculation. Must be one of the
                values defined in WEIGHT_GEN_METHODS.
            weight_gen_crs (Union[str, int, CRS]): The coordinate reference system to be used. Accepts any
                projection that can be used by pyproj.CRS.from_user_input.
            output_file (str, optional): The path to the output file where the DataFrame
                will be saved. If None, no output file will be created. Default is None.
            jobs (int, optional): The number of processors to be used for parallel or
                dask methods. Default is -1, which means the number of processors available
                divided by 2 will be used.
            verbose (bool, optional): If True, additional output will be printed during
                execution. Default is False.

        Raises:
        ------
            TypeError: If the `method` attribute is not one of the values defined in
                WEIGHT_GEN_METHODS

        """
        self.user_data = user_data
        self.method = method
        if output_file is None:
            self.output_file = ""
        else:
            self.output_file = output_file
        self.weight_gen_crs = weight_gen_crs
        self.jobs = jobs
        self.verbose = verbose
        self._intersections: gpd.GeoDataFrame
        self.__calc_method: SerialWghtGenEngine | ParallelWghtGenEngine | DaskWghtGenEngine
        if self.method == "serial":
            self.__calc_method = SerialWghtGenEngine()
            print("Using serial engine")
        elif self.method == "parallel":
            self.__calc_method = ParallelWghtGenEngine()
            print("Using parallel engine")
        elif self.method == "dask":
            self.__calc_method = DaskWghtGenEngine()
        else:
            raise TypeError(f"method: {self.method} not in [serial, parallel]")

    def calculate_weights(self, intersections: bool = False) -> pd.DataFrame:
        """Calculate and return weights.

        Calculates weights for target and source polygons based on user data
        and the specified method.

        Args:
        ----
            intersections (bool): If True, calculate and store
                intersections between target and source polygons. Defaults to
                False.

        Returns:
        -------
            pd.DataFrame: DataFrame containing the calculated weights, with
                columns depending on the source type:
                - For grid sources: "target_id", "i_index", "j_index",
                  "weight".
                - For polygon sources: "target_id", "source_id", "weight".

        """
        tstrt = time.perf_counter()
        self._weight_data: WeightData = self.user_data.prep_wght_data()
        tend = time.perf_counter()
        print(f"Data preparation finished in {tend - tstrt:0.4f} seconds")
        if intersections:
            print("Saving interesections in weight generation.")
            weights, self._intersections = self.__calc_method.calc_weights(
                target_poly=self._weight_data.feature,
                target_poly_idx=self._weight_data.id_feature,
                source_poly=self._weight_data.grid_cells,
                source_poly_idx=["i_index", "j_index"],
                source_type="grid",
                wght_gen_crs=self.weight_gen_crs,
                filename=self.output_file,
                intersections=intersections,
                jobs=self.jobs,
                verbose=self.verbose,
            )
        else:
            weights = self.__calc_method.calc_weights(
                target_poly=self._weight_data.feature,
                target_poly_idx=self._weight_data.id_feature,
                source_poly=self._weight_data.grid_cells,
                source_poly_idx=["i_index", "j_index"],
                source_type="grid",
                wght_gen_crs=self.weight_gen_crs,
                filename=self.output_file,
                intersections=intersections,
                jobs=self.jobs,
                verbose=self.verbose,
            )
        return weights

    @property
    def grid_cells(self) -> gpd.GeoDataFrame:
        """Gets the grid cells as a GeoDataFrame.

        This property returns the grid cells that are used in weight calculations.
        If the grid cells have not been calculated yet, a message will be printed
        suggesting to run `calculate_weights()`.

        Returns
        -------
            gpd.GeoDataFrame: A GeoDataFrame containing the grid cells used in weight
                calculations. If not calculated yet, a message will be printed.

        """
        if self._weight_data.grid_cells is None:
            print("grid_cells not calculated yet. Run calculate_weights().")
        return self._weight_data.grid_cells

    @property
    def intersections(self) -> gpd.GeoDataFrame:
        """Gets the intersections as a GeoDataFrame.

        This property returns the intersections between the target and source polygons.
        If the intersections have not been calculated yet, a message will be printed
        suggesting to run `calculate_weights(intersections=True)`.

        Returns
        -------
            gpd.GeoDataFrame: A GeoDataFrame containing the intersections between the
                target and source polygons. If not calculated yet, a message will be printed.

        """
        if self._intersections is None:
            print("intersections not calculated, " "Run calculate_weights(intersectiosn=True)")
        return self._intersections
