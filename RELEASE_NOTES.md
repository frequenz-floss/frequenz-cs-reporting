# Frequenz CS Reporting Library Release Notes

## Summary


## Upgrading

- Update dockerfile to have grpcio.

## New Features

- Added a "Filter der Tabelle zurücksetzen" control to reporting tables, allowing
  users to clear AgGrid filters without rerunning the page.

## Bug Fixes

- Fixed reporting table pagination and sizing by using a stable page size and
  calculated grid height instead of automatic page sizing.
- Improved reporting dashboard error handling for timeouts, missing microgrid
  configuration, invalid filter parameters, service configuration problems, and
  API/network failures.
