<!--header-start-->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://data.nhm.ac.uk/images/nhm_logo.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://data.nhm.ac.uk/images/nhm_logo_black.svg">
  <img alt="The Natural History Museum logo." src="https://data.nhm.ac.uk/images/nhm_logo_black.svg" align="left" width="150px" height="100px" hspace="40">
</picture>

# ckanext-versioned-tiledmap

[![Tests](https://img.shields.io/github/actions/workflow/status/NaturalHistoryMuseum/ckanext-versioned-tiledmap/tests.yml?style=flat-square)](https://github.com/NaturalHistoryMuseum/ckanext-versioned-tiledmap/actions/workflows/tests.yml)
[![Coveralls](https://img.shields.io/coveralls/github/NaturalHistoryMuseum/ckanext-versioned-tiledmap/main?style=flat-square)](https://coveralls.io/github/NaturalHistoryMuseum/ckanext-versioned-tiledmap)
[![CKAN](https://img.shields.io/badge/ckan-2.9.7-orange.svg?style=flat-square)](https://github.com/ckan/ckan)
[![Python](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue.svg?style=flat-square)](https://www.python.org/)
[![Docs](https://img.shields.io/readthedocs/ckanext-versioned-tiledmap?style=flat-square)](https://ckanext-versioned-tiledmap.readthedocs.io)

_A CKAN extension with a map view for versioned-datastore backed resources._

<!--header-end-->

# Overview

<!--overview-start-->
A CKAN plugin with a map view for versioned-datastore backed resources allowing for map visualizations of large resources with millions of data points.

This repository is a fork* of [ckanext-map](https://github.com/NaturalHistoryMuseum/ckanext-map).

_*you can't fork repositories within the same organisation, so this repository is a duplicate of ckanext-map._

<!--overview-end-->

# Installation

<!--installation-start-->
Path variables used below:
- `$INSTALL_FOLDER` (i.e. where CKAN is installed), e.g. `/usr/lib/ckan/default`
- `$CONFIG_FILE`, e.g. `/etc/ckan/default/development.ini`

## Pre-install setup

This extension depends on the following projects, which must be installed _first_:
- [versioned-datastore-tile-server](https://github.com/NaturalHistoryMuseum/versioned-datastore-tile-server)

## Installing from PyPI

```shell
pip install ckanext-versioned-tiledmap
```

## Installing from source

1. Clone the repository into the `src` folder:
   ```shell
   cd $INSTALL_FOLDER/src
   git clone https://github.com/NaturalHistoryMuseum/ckanext-versioned-tiledmap.git
   ```

2. Activate the virtual env:
   ```shell
   . $INSTALL_FOLDER/bin/activate
   ```

3. Install via pip:
   ```shell
   pip install $INSTALL_FOLDER/src/ckanext-versioned-tiledmap
   ```

### Installing in editable mode

Installing from a `pyproject.toml` in editable mode (i.e. `pip install -e`) requires `setuptools>=64`; however, CKAN 2.9 requires `setuptools==44.1.0`. See [our CKAN fork](https://github.com/NaturalHistoryMuseum/ckan) for a version of v2.9 that uses an updated setuptools if this functionality is something you need.

## Post-install setup

1. Add 'versioned_tiledmap' to the list of plugins in your `$CONFIG_FILE`:
   ```ini
   ckan.plugins = ... versioned_tiledmap
   ```

2. Install `lessc` globally:
   ```shell
   npm install -g "less@~4.1"
   ```

3. Add latitude and longitude fields for the resources you want to use this view for.

<!--installation-end-->

# Configuration

<!--configuration-start-->
These are the options that can be specified in your .ini config file.

| Name                                              | Description                                                                                                                                                                                                        | Default                                                            |
|---------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| `versioned_tilemap.tile_layer.url`                | The URL to use for the base world tiles                                                                                                                                                                            | `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`               |
| `versioned_tilemap.tile_layer.attribution`        | The attribution text to show for this layer (can be HTML)                                                                                                                                                          | `Base tiles provided by OpenStreetMap. <a href="openstreetmap.org/copyright">View copyright information</a>`                                                                   |
| `versioned_tilemap.tile_layer.opacity`            | The opacity for the tile layer                                                                                                                                                                                     | `0.8`                                                              |
| `versioned_tilemap.zoom_bounds.min`               | Minimum zoom level for initial display of the resource's data                                                                                                                                                      | `3`                                                                |
| `versioned_tilemap.zoom_bounds.max`               | Maximum zoom level for initial display of the resource's data                                                                                                                                                      | `18`                                                               |
| `versioned_tilemap.style.plot.point_radius`       | The integer radius of the rendered points (including the border)                                                                                                                                                   | `4`                                                                |
| `versioned_tilemap.style.plot.point_colour`       | The hex value to render the points in                                                                                                                                                                              | `#ee0000` ![#ee0000](https://placehold.it/15/ee0000/000000?text=+) |
| `versioned_tilemap.style.plot.border_width`       | The integer border width of the rendered points                                                                                                                                                                    | `1`                                                                |
| `versioned_tilemap.style.plot.border_colour`      | The hex value to render the borders of the points in                                                                                                                                                               | `#ffffff` ![#ffffff](https://placehold.it/15/ffffff/000000?text=+) |
| `versioned_tilemap.style.plot.grid_resolution`    | The integer size of the cells in the grid that each tile is split into for the UTFGrid. The default of `4` produces a 64x64 grid within each tile                                                                  | `4`                                                                |
| `versioned_tilemap.style.gridded.cold_colour`     | The hex value to be used to render the points with the lowest counts                                                                                                                                               | `#f4f11a` ![#f4f11a](https://placehold.it/15/f4f11a/000000?text=+) |
| `versioned_tilemap.style.gridded.hot_colour`      | The hex value to be used to render the points with the highest counts                                                                                                                                              | `#f02323` ![#f02323](https://placehold.it/15/f02323/000000?text=+) |
| `versioned_tilemap.style.gridded.range_size`      | This many colours will be used to render the points dependant on their counts                                                                                                                                      | `12`                                                               |
| `versioned_tilemap.style.gridded.resize_factor`   | A resize value to use when smoothing the tile. This value will be used to scale the tile and then down (with anti-aliasing) to produce a smoother output. Increasing this value will negatively impact performance | `4`                                                                |
| `versioned_tilemap.style.gridded.grid_resolution` | The integer size of the cells in the grid that each tile is split into. The default of `8` produces a 32x32 grid within each tile and therefore matches the default `grid.json` setting too                        | `8`                                                                |
| `versioned_tilemap.style.heatmap.point_radius`    | The integer radius of the rendered points (including the border)                                                                                                                                                   | `8`                                                                |
| `versioned_tilemap.style.heatmap.cold_colour`     | The hex value to be used to render the points with the lowest counts                                                                                                                                               | `#0000ee` ![#0000ee](https://placehold.it/15/0000ee/000000?text=+) |
| `versioned_tilemap.style.heatmap.hot_colour`      | The hex value to be used to render the points with the highest counts                                                                                                                                              | `#ee0000` ![#ee0000](https://placehold.it/15/ee0000/000000?text=+) |
| `versioned_tilemap.style.heatmap.intensity`       | The decimal intensity (between 0 and 1) to render the tile with                                                                                                                                                    | `0.5`                                                              |
| `versioned_tilemap.info_template`                 | The name of the template to use when a point is clicked                                                                                                                                                            | `point_detail`                                                     |
| `versioned_tilemap.quick_info_template`           | The name of the template to use when a point is hovered over                                                                                                                                                       | `point_detail_hover`                                               |

<!--configuration-end-->

# Usage

<!--usage-start-->
After enabling this extension in the list of plugins, the Map view should become available for resources with latitude and longitude values.

<!--usage-end-->

# Testing

<!--testing-start-->
There is a Docker compose configuration available in this repository to make it easier to run tests. The ckan image uses the Dockerfile in the `docker/` folder.

To run the tests against ckan 2.9.x on Python3:

1. Build the required images:
   ```shell
   docker compose build
   ```

2. Then run the tests.
   The root of the repository is mounted into the ckan container as a volume by the Docker compose
   configuration, so you should only need to rebuild the ckan image if you change the extension's
   dependencies.
   ```shell
   docker compose run ckan
   ```

<!--testing-end-->
