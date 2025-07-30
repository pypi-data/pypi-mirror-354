"""Statistical Funtions for aggregation."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import numpy as np
import numpy.typing as npt


@dataclass  # type: ignore[misc]
class StatsMethod(ABC):
    """Abstract method for gdptools weighted stats.

    Args:
    ----
        array: 2-dimensional array of gridded data values for a given target polygon
            Axis 0: element along flattened input XY grid array
            Axis 1: time index
        weights: 1-dimensional array of weights associated with each element in data
            subset array; does not change with time dimension.
        def_val: default value

    """

    array: npt.NDArray  # type: ignore
    weights: npt.NDArray[np.double]
    def_val: Any

    @abstractmethod
    def get_stat(
        self,
    ) -> npt.NDArray[np.int_ | np.double]:
        """Abstract method for aquiring stats."""
        pass


@dataclass
class MAWeightedMean(StatsMethod):
    """Weighted Masked Mean."""

    def get_stat(self) -> npt.NDArray[np.int_ | np.double]:
        """Calculate the masked weighted mean.

        Calculates the weighted mean of the input array, handling missing
        values using NumPy's masked array functionality.  Weights are applied
        along the specified axis.

        Returns
        -------
            npt.NDArray[Union[np.int_, np.double]]: The masked weighted mean.

        """
        masked = np.ma.masked_array(self.array, np.isnan(self.array))
        try:
            tmp = np.ma.average(masked, weights=self.weights, axis=1)
        except KeyError:
            numpts = self.weights.shape[0]
            tmp = np.full((numpts), self.def_val)

        return np.nan_to_num(tmp, nan=self.def_val)


@dataclass
class WeightedMean(StatsMethod):
    """Weighted Mean."""

    def get_stat(self) -> npt.NDArray[np.int_ | np.double]:
        """Calculate the weighted mean.

        Calculates the weighted mean of the input array. Weights are applied
        along the specified axis.

        Returns
        -------
            npt.NDArray[Union[np.int_, np.double]]: The weighted mean.

        """
        try:
            tmp = np.average(self.array, weights=self.weights, axis=1)
        except KeyError:
            numpts = self.weights.shape[0]
            tmp = np.full((numpts), self.def_val)
        return np.nan_to_num(tmp, nan=self.def_val)


@dataclass
class WeightedStd(StatsMethod):
    """Weighted Standard Deviation."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> npt.NDArray[np.double]:
        """Calculate the weighted standard deviation.

        Calculates the weighted standard deviation of the input array.
        Weights are applied along the specified axis.

        Returns
        -------
            npt.NDArray[np.double]: The weighted standard deviation.

        """
        try:
            avg = np.average(self.array, weights=self.weights, axis=1)
            variance = np.average((self.array - avg[:, None]) ** 2, weights=self.weights, axis=1)
            tmp = np.sqrt(variance)
        except KeyError:
            numpts = self.weights.shape[0]
            tmp = np.full((numpts), self.def_val)
        return np.nan_to_num(tmp, nan=self.def_val)


@dataclass
class MAWeightedStd(StatsMethod):
    """Weighted Masked Standard Deviation."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> npt.NDArray[np.double]:
        """Calculate the masked weighted standard deviation.

        Calculates the weighted standard deviation of the input array,
        handling missing values using NumPy's masked array functionality.
        Weights are applied along the specified axis.

        Returns
        -------
            npt.NDArray[np.double]: The masked weighted standard deviation.

        """
        try:
            masked = np.ma.masked_array(self.array, np.isnan(self.array))
            avg = np.ma.average(masked, weights=self.weights, axis=1)
            variance = np.ma.average((masked - avg[:, None]) ** 2, weights=self.weights, axis=1)
            tmp = np.sqrt(variance)
        except KeyError:
            numpts = self.weights.shape[0]
            tmp = np.full((numpts), self.def_val)
        return np.nan_to_num(tmp, nan=self.def_val)


@dataclass
class MAWeightedMedian(StatsMethod):
    """Weighted Masked Median."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def _get_median(self, array: npt.NDArray, weights: npt.NDArray[np.double], def_val: np.double) -> np.double:
        """Calculate the masked weighted median for a single time step.

        Calculates the weighted median of the input array for a single time
        step, handling missing values using NumPy's masked array
        functionality.

        Args:
        ----
            array (npt.NDArray[np.double]): Input array for a single time step.
            weights (npt.NDArray[np.double]): Weights for the input array.
            def_val (np.double): Default fill value.

        Returns:
        -------
            np.double: The masked weighted median.

        """
        try:
            masked = np.ma.masked_array(array, np.isnan(array))
            # zip and sort array values and their corresponding weights
            pairs = sorted(list(zip(masked, weights)))  # noqa
            # mask nodata values from zipped values and weights
            masked_pairs = [tuple for tuple in pairs if not np.isnan(tuple[0])]
            # unzip tuples into a list of masked array values and their weights
            masked_vals, masked_wghts = map(list, zip(*masked_pairs))  # noqa
            i = np.array(masked_vals).argsort()
            sorted_weights = np.array(masked_wghts)[i]
            sorted_values = np.array(masked_vals)[i]
            s = sorted_weights.cumsum()
            p = (s - sorted_weights / 2) / s[-1]
            tmp = np.interp(0.5, p, sorted_values)
        except KeyError:
            tmp = def_val
        return tmp

    def get_stat(self) -> npt.NDArray[np.double]:
        """Calculate the masked weighted median.

        Calculates the weighted median of the input array, handling missing
        values using NumPy's masked array functionality.  Applies the
        _get_median function along each time step.

        Returns
        -------
            npt.NDArray[np.double]: An array of masked weighted medians, one
                for each time step.

        """
        return np.apply_along_axis(self._get_median, 1, self.array, self.weights, self.def_val)


@dataclass
class WeightedMedian(StatsMethod):
    """Weighted Median."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def _get_median(
            self, array: npt.NDArray, weights: npt.NDArray[np.double], def_val: np.double
    ) -> npt.NDArray[np.double]:
        """Calculate the weighted median for a single time step.

        Calculates the weighted median of the input array for a single time
        step.

        Args:
        ----
            array (npt.NDArray[np.double]): Input array for a single time step.
            weights (npt.NDArray[np.double]): Weights for the input array.
            def_val (np.double): Default fill value.

        Returns:
        -------
            np.double: The weighted median.

        """
        # First check to see if there are NoData values. Function will return np.nan
        # if there are NoData values, as medians cannot be calculated if NoData values
        # exist.
        if np.isnan(array).any():
            return def_val
        try:
            # zip and sort array values and their corresponding weights
            pairs = sorted(list(zip(array, weights)))  # noqa
            # unzip tuples into a list of array values and their weights
            vals, wghts = map(list, zip(*pairs))  # noqa
            i = np.array(vals).argsort()
            sorted_weights = np.array(wghts)[i]
            sorted_values = np.array(vals)[i]
            s = sorted_weights.cumsum()
            p = (s - sorted_weights / 2) / s[-1]
            tmp = np.interp(0.5, p, sorted_values)

        except KeyError:
            tmp = def_val
        return tmp

    def get_stat(self) -> npt.NDArray[np.double]:
        """Calculate the weighted median.

        Calculates the weighted median of the input array. Applies the
        _get_median function along each time step.

        Returns
        -------
            npt.NDArray[np.double]: An array of weighted medians, one for
                each time step.

        """
        return np.apply_along_axis(self._get_median, 1, self.array, self.weights, self.def_val)


@dataclass
class MACount(StatsMethod):
    """Masked Count."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> npt.NDArray[np.int_]:
        """Count masked grid cells.

        Counts the number of masked (non-missing) grid cells, considering
        both the data array mask and zero weights.

        Returns
        -------
            npt.NDArray[np.int_]: An array of counts, one for each time step.

        """
        try:
            masked = np.ma.masked_array(self.array, np.isnan(self.array))
            weight_mask = self.weights == 0
            tmp = np.ma.masked_array(masked, mask=weight_mask | masked.mask).count(axis=1)
        except KeyError:
            numpts = self.weights.shape[0]
            tmp = np.full((numpts), 0)
        return tmp


@dataclass
class Count(StatsMethod):
    """Count."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> npt.NDArray[np.int_]:
        """Count grid cells.

        Counts the number of grid cells with non-zero weights.

        Returns
        -------
            npt.NDArray[np.int_]: The count of grid cells.

        """
        try:
            tmp = np.ma.masked_array(self.weights, mask=self.weights == 0).count()
        except KeyError:
            numpts = self.weights.shape[0]
            tmp = np.full((numpts), 0)
        return tmp


@dataclass
class MASum(StatsMethod):
    """Masked Sum."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> npt.NDArray[np.double]:
        """Calculate the masked sum.

        Calculates the sum of the input array, handling missing values using
        NumPy's masked array functionality.

        Returns
        -------
            npt.NDArray[np.double]: The masked sum.

        """
        try:
            masked = np.ma.masked_array(self.array, np.isnan(self.array))
            tmp = np.ma.sum(masked * self.weights, axis=1)
        except KeyError:
            numpts = len(self.weights)
            tmp = np.full((numpts), self.def_val)
        return tmp


@dataclass
class Sum(StatsMethod):
    """Sum."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> npt.NDArray[np.double]:
        """Calculate the sum.

        Calculates the sum of the input array.

        Returns
        -------
            npt.NDArray[np.double]: The sum.

        """
        try:
            tmp = np.sum(self.array * self.weights, axis=1)
        except KeyError:
            numpts = len(self.weights)
            tmp = np.full((numpts), 0)
        return np.nan_to_num(tmp, nan=self.def_val)


@dataclass
class MAMin(StatsMethod):
    """Masked Minimum Value."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> npt.NDArray[np.double]:
        """Calculate the masked minimum.

        Calculates the minimum value of the input array, handling missing
        values using NumPy's masked array functionality.

        Returns
        -------
            npt.NDArray[np.double]: The masked minimum.

        """
        try:
            masked = np.ma.masked_array(self.array, np.isnan(self.array))
            tmp = np.ma.min(masked, axis=1)
        except KeyError:
            numpts = self.weights.shape[0]
            tmp = np.full((numpts), self.def_val)
        return tmp


@dataclass
class Min(StatsMethod):
    """Minimum Value."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> npt.NDArray[np.double]:
        """Calculate the minimum.

        Calculates the minimum value of the input array.

        Returns
        -------
            npt.NDArray[np.double]: The minimum value.

        """
        try:
            tmp = np.min(self.array, axis=1)
        except KeyError:
            numpts = self.weights.shape[0]
            tmp = np.full((numpts), self.def_val)
        return np.nan_to_num(tmp, nan=self.def_val)


@dataclass
class MAMax(StatsMethod):
    """Masked Maximum Value."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> npt.NDArray[np.double]:
        """Calculate the masked maximum.

        Calculates the maximum value of the input array, handling missing
        values using NumPy's masked array functionality.

        Returns
        -------
            npt.NDArray[np.double]: The masked maximum.

        """
        try:
            masked = np.ma.masked_array(self.array, np.isnan(self.array))
            tmp = np.ma.max(masked, axis=1)
        except KeyError:
            numpts = self.weights.shape[0]
            tmp = np.full((numpts), self.def_val)
        return np.nan_to_num(tmp, nan=self.def_val)


@dataclass
class Max(StatsMethod):
    """Maximum Value."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> npt.NDArray[np.double]:
        """Calculate the maximum.

        Calculates the maximum value of the input array.

        Returns
        -------
            npt.NDArray[np.double]: The maximum value.

        """
        try:
            tmp = np.max(self.array, axis=1)
        except KeyError:
            numpts = self.weights.shape[0]
            tmp = np.full((numpts), self.def_val)
        return np.nan_to_num(tmp, nan=self.def_val)
