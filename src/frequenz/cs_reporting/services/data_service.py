# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Async and cached data access helpers for microgrid measurements."""

from __future__ import annotations

import asyncio
import logging
import warnings
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
from pandas.errors import PerformanceWarning

from frequenz.cs_reporting.services.client_factory import (
    get_component_types,
    get_microgrid_client,
)
from frequenz.cs_reporting.utils.time import validate_range

_COMPONENT_DATA_LOGGER = "frequenz.data.microgrid.component_data"


class _MissingComponentFilter(logging.Filter):
    """Filter expected missing-component warnings from the data client."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Return whether a log record should be emitted."""
        if record.name != _COMPONENT_DATA_LOGGER:
            return True
        message = record.getMessage()
        return not (
            message.startswith("Component ID ")
            and message.endswith(" not found in data, setting zero")
        )


@contextmanager
def _quiet_expected_component_data_warnings() -> Iterator[None]:
    """Suppress expected noisy warnings emitted while building component data."""
    logger = logging.getLogger(_COMPONENT_DATA_LOGGER)
    component_filter = _MissingComponentFilter()
    logger.addFilter(component_filter)
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                category=PerformanceWarning,
                message="DataFrame is highly fragmented.*",
                module=r"frequenz\.data\.microgrid\.component_data",
            )
            yield
    finally:
        logger.removeFilter(component_filter)


async def fetch_microgrid_data(
    microgrid_id: int,
    start_date: datetime,
    end_date: datetime,
    resolution: timedelta,
    timeout: float = 30.0,
) -> pd.DataFrame:
    """Fetch AC active power for a microgrid in ``[start_date, end_date)``.

    Args:
        microgrid_id: Identifier for the target microgrid.
        start_date: Inclusive start date of the query range.
        end_date: Exclusive end date of the query range.
        resolution: Resampling period for the returned data.
        timeout: Request timeout in seconds.

    Returns:
        Dataframe of AC active power measurements. Empty when no
            data is available.
    """
    start_iso, end_iso = validate_range(start_date, end_date)
    client = get_microgrid_client(microgrid_id)
    component_types: tuple[str, ...] = get_component_types(microgrid_id)

    coro = client.ac_active_power(
        microgrid_id=microgrid_id,
        component_types=component_types,
        start=start_iso,
        end=end_iso,
        resampling_period=resolution,
        keep_components=True,
        splits=True,
    )
    with _quiet_expected_component_data_warnings():
        df = await asyncio.wait_for(coro, timeout)

    if df is None or (hasattr(df, "empty") and df.empty):
        return pd.DataFrame()
    return df.copy()


# Cached sync wrapper for Streamlit pages
@st.cache_data(ttl=300, show_spinner=False)
def get_microgrid_data(
    microgrid_id: int,
    start_date: datetime,
    end_date: datetime,
    resolution: timedelta,
    timeout: float = 30.0,
) -> pd.DataFrame:
    """Sync wrapper for Streamlit pages with caching (5 min TTL).

    Args:
        microgrid_id: Identifier for the target microgrid.
        start_date: Inclusive start date of the query range.
        end_date: Exclusive end date of the query range.
        resolution: Resampling period for the returned data.
        timeout: Request timeout in seconds.

    Returns:
        Dataframe of AC active power measurements. Empty when no
            data is available.

    Raises:
        RuntimeError: If invoked from within an active event loop instead of
            using the async ``fetch_microgrid_data``.
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        # No active loop: safe to block
        return asyncio.run(
            fetch_microgrid_data(
                microgrid_id, start_date, end_date, resolution, timeout=timeout
            )
        )
    # Active loop: force caller to use the async API
    raise RuntimeError(
        "get_microgrid_data() called from within an active event loop. "
        "Use `await fetch_microgrid_data(...)` in async contexts."
    )
