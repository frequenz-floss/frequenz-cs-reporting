# Frequenz CS Reporting Library Release Notes

## Summary

- Update reporting to work with the latest `frequenz-lib-notebooks` and
  `frequenz-gridpool` APIs, including Assets API-backed microgrid configuration
  loading, meter display names, day-ahead prices, and the battery-usecase
  overview plot.

## Upgrading

- Set `ASSETS_API_URL` in addition to `REPORTING_API_URL`, `API_KEY`, and
  `API_SECRET`. The reporting dashboard now uses the Assets API to merge
  microgrid configuration data and fetch component display names.
- Set `ENTSOE_API_KEY` to show day-ahead prices in the reporting overview plot.
  If it is not configured, the dashboard still renders without the price trace.

## New Features

- Load microgrid configuration through `frequenz.gridpool.load_configs()` with
  local TOML defaults and Assets API data.
- Use Assets API component display names when creating the reporting energy report dataframe.
- Add day-ahead prices to the reporting overview data and render them on a secondary axis in the battery-usecase overview plot.
- Replace the generic overview time-series plot with
  `plot_time_series_battery_usecase()` using the psc visualization
  flow from `frequenz-lib-notebooks`.

## Bug Fixes
