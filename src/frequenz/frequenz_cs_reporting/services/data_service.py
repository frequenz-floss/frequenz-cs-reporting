# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Async and cached data access helpers for microgrid measurements."""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

from frequenz.frequenz_cs_reporting.services.client_factory import (
    get_component_types,
    get_microgrid_client,
)
from frequenz.frequenz_cs_reporting.utils.time import validate_range


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
    df = await asyncio.wait_for(coro, timeout)

    if df is None or (hasattr(df, "empty") and df.empty):
        return pd.DataFrame()
    return df


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
