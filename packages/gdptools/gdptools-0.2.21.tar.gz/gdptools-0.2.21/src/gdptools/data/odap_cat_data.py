"""OpenDAP Catalog Data classes."""

from __future__ import annotations

from typing import Any

import numpy as np
from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator, model_validator


class CatClimRItem(BaseModel):
    """Mike Johnson's CatClimRItem class.

    Source data from:
    'https://github.com/mikejohnson51/climateR-catalogs/releases/download/June-2024/catalog.parquet'
    """

    id: str | None = None
    asset: str | None = None
    URL: str
    varname: str
    long_name: str | None = None
    variable: str | None = None
    description: str | None = None
    units: str | None = None
    model: str | None = None
    ensemble: str | None = None
    scenario: str | None = None
    T_name: str | None = None
    duration: str | None = None
    interval: str | None = None
    nT: int | None = Field(default=0)  # noqa: N815
    X_name: str
    Y_name: str
    X1: float | None = None
    Xn: float | None = None
    Y1: float | None = None
    Yn: float | None = None
    resX: float  # noqa: N815
    resY: float  # noqa: N815
    ncols: int | None = None
    nrows: int | None = None
    proj: str | None = None
    toptobottom: bool
    tiled: str | None = None
    crs: str | None = None

    @model_validator(mode="after")
    def set_default_long_name(self, info: ValidationInfo) -> CatClimRItem:
        """Set `long_name` from `description` if missing."""
        if not self.long_name:
            self.long_name = self.description or "None"
        return self

    @model_validator(mode="after")
    def _set_proj(self, info: ValidationInfo) -> CatClimRItem:
        """Set `proj` from `crs` if `proj` is missing."""
        if not self.proj:
            self.proj = self.crs or "EPSG:4326"
        return self

    @field_validator("nT", mode="before", check_fields=False)
    @classmethod
    def set_nt(cls, v: Any) -> int:  # noqa: ANN401
        """Convert nT to int, handle NaN."""
        if v is None:
            return 0
        if isinstance(v, float | np.floating) and np.isnan(v):
            return 0
        return int(v)

    @field_validator("toptobottom", mode="before")
    @classmethod
    def _toptobottom_as_bool(cls, v: Any) -> bool:  # noqa: ANN401
        """Convert 'TRUE'/'FALSE' strings to real boolean True/False."""
        if isinstance(v, str):
            return v.strip().upper() == "TRUE"
        return bool(v)

    @field_validator("tiled", mode="before", check_fields=False)
    @classmethod
    def _tiled(cls, val: str | None) -> str:
        """Ensure tiled value is valid."""
        if not val:
            return "NA"
        val = val.upper()
        if val not in ["", "NA", "T", "XY"]:
            raise ValueError("tiled must be one of ['', 'NA', 'T', 'XY']")
        return val

    model_config = ConfigDict(
        str_strip_whitespace=False,
        frozen=False,  # allow mutation (new way)
    )
