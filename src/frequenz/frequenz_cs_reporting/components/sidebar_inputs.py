# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Sidebar filter rendering helpers."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any, Sequence

import streamlit as st

from frequenz.frequenz_cs_reporting.components import inputs
from frequenz.frequenz_cs_reporting.services.client_factory import get_microgrid_ids

TIMEZONE_OPTIONS = (
    "Europe/Berlin",
    "Europe/Vienna",
    "Europe/Zurich",
    "Europe/Amsterdam",
    "Europe/Brussels",
    "Europe/Copenhagen",
    "UTC",
)


# pylint: disable=too-many-locals, too-many-arguments
def collect_sidebar_inputs(
    *,
    default_start: date,
    default_end: date,
    resolution_options: Sequence[str] = ("15min", "30min", "1hour", "4hour"),
    default_resolution: str = "15min",
    timezone_options: Sequence[str] = TIMEZONE_OPTIONS,
    default_timezone: str = "Europe/Berlin",
    key_prefix: str = "",
) -> dict[str, Any]:
    """Render structured sidebar filters with clear visual hierarchy.

    Creates an organized sidebar with sections for microgrid selection, date
    range, and resolution. Uses icons, dividers, and proper grouping for
    professional appearance and better UX.

    Args:
        default_start: Default start date for the date picker.
        default_end: Default end date for the date picker.
        resolution_options: Allowed resolution values for selection.
        default_resolution: Default resolution shown initially.
        timezone_options: Allowed timezone values for selection.
        default_timezone: Default timezone shown initially.
        key_prefix: Optional prefix for Streamlit widget keys.

    Returns:
        Dictionary containing ``microgrid_id``, ``start_date``,
            ``end_date``, ``timezone``, and ``resolution`` selected by the user.
    """
    # Header with icon and caption
    st.sidebar.header("🎛️ Filter Einstellungen")
    st.sidebar.caption("Wählen Sie die gewünschten Parameter für die Analyse")

    form_key = f"{key_prefix}filters_form" if key_prefix else "filters_form"
    state_key = f"{key_prefix}applied_filters" if key_prefix else "applied_filters"

    with st.sidebar.form(form_key):
        # Microgrid Section
        st.subheader("🏭 Microgrid")
        microgrid_id = inputs.microgrid_selector(
            label="Microgrid ID",
            ids=get_microgrid_ids(),
            key_prefix=key_prefix,
            container=st,
        )

        st.divider()

        # Date & Time Section
        st.subheader("📅 Zeitraum")

        today = date.today()
        fallback_start = default_start or (today - timedelta(days=7))

        start_key = f"{key_prefix}start_date"
        end_key = f"{key_prefix}end_date"
        timezone_key = f"{key_prefix}timezone"

        start_initial = st.session_state.get(start_key, fallback_start)

        columns = st.columns(2)
        with columns[0]:
            start_date = st.date_input(
                "Start",
                value=start_initial,
                max_value=today,
                key=start_key,
            )

        end_initial = min(
            st.session_state.get(end_key, default_end or today),
            today,
        )

        with columns[1]:
            end_date = st.date_input(
                "Ende",
                value=end_initial,
                max_value=today,
                key=end_key,
            )

        timezone_options_list = list(timezone_options)
        timezone_index = next(
            (
                idx
                for idx, option in enumerate(timezone_options_list)
                if option == default_timezone
            ),
            0,
        )

        timezone = st.selectbox(
            "🌍 Zeitzone",
            options=timezone_options_list,
            index=timezone_index,
            key=timezone_key,
            help="Zeitzone zur Interpretation der ausgewählten Tage",
        )

        st.divider()

        # Resolution selector (full width)
        resolution = st.selectbox(
            "⏱️ Auflösung",
            options=list(resolution_options),
            index=next(
                (
                    idx
                    for idx, option in enumerate(resolution_options)
                    if option == default_resolution
                ),
                0,
            ),
            key=f"{key_prefix}resolution",
            help="Zeitliche Auflösung der Daten",
        )

        st.divider()

        # Prominent submit button
        submitted = st.form_submit_button(
            "✓ Filter anwenden", use_container_width=True, type="primary"
        )

    current_selection = {
        "microgrid_id": microgrid_id,
        "start_date": start_date,
        "end_date": end_date,
        "timezone": timezone,
        "resolution": resolution,
    }

    if submitted or state_key not in st.session_state:
        st.session_state[state_key] = current_selection

    return dict(st.session_state[state_key])
