# Readme

[![PyPI](https://img.shields.io/pypi/v/gdptools.svg)](https://pypi.org/project/gdptools/)
[![conda](https://anaconda.org/conda-forge/gdptools/badges/version.svg)](https://anaconda.org/conda-forge/gdptools)
[![Latest Release](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/badges/release.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/releases)

[![Status](https://img.shields.io/pypi/status/gdptools.svg)](https://pypi.org/project/gdptools/)
[![Python Version](https://img.shields.io/pypi/pyversions/gdptools)](https://pypi.org/project/gdptools)

[![License](https://img.shields.io/pypi/l/gdptools)](https://creativecommons.org/publicdomain/zero/1.0/legalcode)

[![Read the documentation at https://gdptools.readthedocs.io/](https://img.shields.io/readthedocs/gdptools/latest.svg?label=Read%20the%20Docs)](https://gdptools.readthedocs.io/)
[![pipeline status](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/badges/main/pipeline.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/commits/main)
[![coverage report](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/badges/main/coverage.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/commits/main)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://code.usgs.gov/pre-commit/pre-commit)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://code.usgs.gov/psf/black)
[![Poetry](https://img.shields.io/badge/poetry-enabled-blue)](https://python-poetry.org/)
[![Conda](https://img.shields.io/badge/conda-enabled-green)](https://anaconda.org/)

## Welcome

Welcome to gdptools, a python package for grid- or polyon-to-polygon area-weighted interpolation statistics.

![Welcome figure](./docs/assets/Welcom_fig.png)

<figcaption>Example grid-to-polygon interpolation.  A) Huc12 basins for Delaware River Watershed. B) Gridded monthly water evaporation amount (mm) from TerraClimate dataset. C) Area-weighted-average interpolation of gridded TerraClimate data to Huc12 polygons.</figcaption>

## Documentation

[gdptools documentation](https://gdptools.readthedocs.io/en/latest/)

## Features

- Grid-to-polygon interpolation of area-weighted statistics.
- Use [Mike Johnson's ClimateR catalog][2] Will eventually supercede the OPeNDAP catalog.
- Use any gridded dataset that can be read by xarray.

[1]: https://mikejohnson51.github.io/opendap.catalog/articles/catalog.html
[2]: https://github.com/mikejohnson51/climateR-catalogs

### Example catalog datasets

```{list-table} Sample selection of climater-catalog datasets
:header-rows: 1
:stub-columns: 1
:width: 100
:widths: auto

* - Dataset (Best available reference)
  - Description
  - Search ID

* - [BCCA](https://gdo-dcp.ucllnl.org/downscaled_cmip_projections/dcpInterface.html#About)
  - Bias Corrected Constructed Analogs V2 Daily Climate Projections (BACA) contains projections of daily   BCCA CMIP3 and CMIP5 projections of precipitation, daily maximum, and daily minimum temperature over the contiguous United States
  - bcca

* - [BCSD](https://gdo-dcp.ucllnl.org/downscaled_cmip_projections/dcpInterface.html#About)
  - Bias Corrected Spatially Downscaled (BCSD) Monthly CMIP5 Climate Projections
  - bcsd

* - [LOCA](https://gdo-dcp.ucllnl.org/downscaled_cmip_projections/dcpInterface.html#**About**)
  - Statistically downscaled CMIP5 climate and hydrology projections for North America, usingLocalized Constructed Analogs (LOCA) method.
  - loca, loca_hydrology

* - [Daymet](https://daymet.ornl.gov/)
  - Daymet provides long-term, continuous, gridded estimates of daily weather and climatology variables by interpolating and extrapolating ground-based observations through statistical modeling techniques.
  - daymet4

* - [gridMET](https://www.climatologylab.org/gridmet.html)
  - GridMET is a gridded meteorological data product that provides estimates of daily weather and climatology variables for the conterminous United States.
  - gridmet

* - [MACA](https://www.climatologylab.org/maca.html)
  - Multivariate Adaptive Constructed Analogs (MACA) is a statistical method for downscaling Global Climate Models (GCMs) from their native coarse resolution to a higher spatial resolution that captures reflects observed patterns of daily near-surface meteorology and simulated changes in GCMs experiments.
  - maca_day, maca_month

* - [TerraClimate](https://www.climatologylab.org/terraclimate.html)
  - TerraClimate is a dataset of monthly climate and climatic water balance for global terrestrial surfaces from 1958-2019. These data provide important inputs for ecological and hydrological studies at global scales that require high spatial resolution and time-varying data.
  - terraclim, terraclim_normals

* - [CHIRPS](https://www.chc.ucsb.edu/data/chirps)
  - Climate Hazards Group InfraRed Precipitation with Station data (CHIRPS) is a 35+ year quasi-global rainfall data set. Spanning 50°S-50°N (and all longitudes) and ranging from 1981 to near-present, CHIRPS incorporates our in-house climatology, CHPclim, 0.05° resolution satellite imagery, and in-situ station data to create gridded rainfall time series for trend analysis and seasonal drought monitoring.
  - chirps20GlobalPentadP05 chirps20GlobalPentadP05_Lon0360, chirps20GlobalAnnualP05, chirps20GlobalAnnualP05_Lon0360, chirps20GlobalDailyP05, chirps20GlobalDailyP05_Lon0360, chirps20GlobalMonthlyP05, chirps20GlobalMonthlyP05_Lon0360

* - [PRISM](https://www.prism.oregonstate.edu/)
  - PRISM (Parameter-elevation Regressions on Independent Slopes Model) is a family of gridded climate data products that provide estimates of monthly climate variables for the conterminous United States (CONUS) and Alaska.
  - prism_monthly, prism_daily

* - [Livneh](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.nodc%3A0129374)
  - A data set of observed daily and monthly averaged precipitation, maximum and minimum temperature, gridded to a 1/16° (~6km) resolution that spans the entire country of Mexico, the conterminous U.S. (CONUS), and regions of Canada south of 53° N for the period 1950-2013.
  - Livneh_daily, Livneh_monthly, Livneh_fluxes

* - [topowx](https://www.scrim.psu.edu/resources/topowx/)
  - (“Topography Weather”) is an 800-meter resolution gridded dataset of daily minimum and maximum air temperature for the conterminous U.S.
  - topowx_daily, topowx_monthly, topowx_normals

* - [WorldClim v2](https://rmets.onlinelibrary.wiley.com/doi/abs/10.1002/joc.5086)
  - Spatially interpolated monthly climate data for global land areas at a very high spatial resolution (approximately 1 km2)
  - wc2.1_10m, wc2.1_5m, wc2.1_2m, wc2.1_30s

* - [3DEP](https://www.usgs.gov/3d-elevation-**program**)
  - The 3D Elevation Program is managed by the U.S. Geological Survey (USGS) National Geospatial Program to respond to growing needs for high-quality topographic data
  - USGS_3DEP
* - [LCMAP](https://www.usgs.gov/special-topics/lcmap)
  - Land Change Monitoring, Assessment, and Projection (LCMAP) represents a new generation of land cover mapping and change monitoring from the U.S. Geological Survey’s Earth Resources Observation and Science (EROS) Center. LCMAP answers a need for higher quality results at greater frequency with additional land cover and change variables than previous efforts.
  - LCMAP

* - [ssebopeta](https://earlywarning.usgs.gov/ssebop/modis)
  - Actual Evapotranspiration (ETA) from The operational Simplified Surface Energy Balance (SSEBop)
  - ssebopeta

* - [maurer](https://www.engr.scu.edu/~emaurer/data.html)
  - Downscaled climate projections as part of CMIP3 and CMIP5, and gridded observed data that can be used in downscaling
  - maurer

* - [GLDAS](https://ldas.gsfc.nasa.gov/gldas)
  - Global Land Data Assimilation System (GLDAS)
  - GLDAS

* - [NLDAS](https://ldas.gsfc.nasa.gov/nldas)
  - North American Land Data Assimilation System (NLDAS)
  - NLDAS

```

## Requirements

### Data - xarray (gridded data) and Geopandas (Polygon data)

- Xarray

  - Any endpoint that can be read by Xarray and contains projected coordinates.
  - Projection: any projection that can be read by proj.CRS (similar to Geopandas)

- Geopandas
  - Any file that can be read by Geopandas
  - Projection: any projection that can be read by proj.CRS

## Installation

You can install _Gdptools_ via [pip](https://pip.pypa.io/) from [PyPI](https://pypi.org/):

```bash
pip install gdptools
```

or install via [conda](https://anaconda.org/) from [conda-forge](https://anaconda.org/conda-forge/gdptools):

```bash
conda install -c conda-forge gdptools
```

## Usage

Please see the example notebooks in the [documentation](https://gdptools.readthedocs.io/en/latest/)

## History

The changelog can be found [here](HISTORY.md)

## Credits

This project was generated from [@hillc-usgs](https://code.usgs.gov/hillc-usgs)'s [Pygeoapi Plugin Cookiecutter](https://code.usgs.gov/wma/nhgf/pygeoapi-plugin-cookiecutter) template.
