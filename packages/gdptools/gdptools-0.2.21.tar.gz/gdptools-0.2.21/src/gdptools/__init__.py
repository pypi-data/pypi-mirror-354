"""Top-level package for pygeoapi plugin: Gdptools."""

import logging

from .agg_gen import AggGen, InterpGen
from .data.user_data import ClimRCatData, NHGFStacData, UserCatData, UserTiffData
from .weight_gen import WeightGen
from .weight_gen_p2p import WeightGenP2P
from .zonal_gen import WeightedZonalGen, ZonalGen

__author__ = "Richard McDonald"
__email__ = "rmcd@usgs.gov"
__version__ = "0.2.21"

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
    "WeightGen",
    "WeightGenP2P",
    "AggGen",
    "ZonalGen",
    "WeightedZonalGen",
    "ClimRCatData",
    "UserCatData",
    "InterpGen",
    "UserTiffData",
    "NHGFStacData",
]
