# Frequenz CS Reporting Library Release Notes

## Summary
- Initial Streamlit-based reporting app that discovers packaged pages, shows branded navigation, and renders microgrid reporting dashboards backed by the frequenz data stack.

## Upgrading


## New Features
- Added app.py entrypoint that loads PageSpec definitions, persists navigation in query params, and renders sidebar branding.
- New Home and Reporting pages: the dashboard offers microgrid/date/timezone/resolution filters, fetches/caches microgrid power data, builds a master dataframe, and drives overview metrics plus consumption breakdowns.
- Dashboard visuals now include time-series plots, energy-mix pie, component-specific tabs (PV, battery, wind, BHKW, EV), and styled plot cards.
- Data tables use AgGrid with CSV downloads for power mix, component analyses, and the combined master dataframe; reusable UI helpers and constants were added for consistent styling and column naming.

## Bug Fixes

