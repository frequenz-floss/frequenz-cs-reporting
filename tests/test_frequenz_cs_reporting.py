# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for the frequenz.cs_reporting package."""

from datetime import UTC, date, datetime, timedelta

import pytest

from frequenz.cs_reporting.utils import time
from frequenz.cs_reporting.views.metric_renderers import (
    SECTION_SPECS,
    _filter_section_box_specs,
)


def test_validate_range_accepts_chronological_values() -> None:
    """validate_range returns converted datetimes when start < end."""
    start = date(2024, 1, 1)
    end = datetime(2024, 1, 2, 12, 0, tzinfo=UTC)

    start_dt, end_dt = time.validate_range(start, end)

    assert start_dt == datetime(2024, 1, 1, tzinfo=UTC)
    assert end_dt == datetime(2024, 1, 2, 12, 0, tzinfo=UTC)
    assert end_dt - start_dt == timedelta(days=1, hours=12)


def test_validate_range_rejects_invalid_order() -> None:
    """validate_range raises when end is not after start."""
    with pytest.raises(ValueError):
        time.validate_range("2024-01-02", "2024-01-02")
    with pytest.raises(ValueError):
        time.validate_range("2024-01-03", "2024-01-02")


def test_battery_kpi_section_is_hidden_without_battery_component() -> None:
    """Battery KPI specs are removed when the MID has no battery component."""
    battery_section = next(
        section for section in SECTION_SPECS if section["title"] == "Batteriekennzahlen"
    )

    box_specs = _filter_section_box_specs(
        battery_section,
        component_type_set={"grid", "pv"},
        component_types_provided=True,
        microgrid_id=123,
    )

    assert box_specs == []


def test_battery_kpi_section_is_shown_with_battery_component() -> None:
    """Battery KPI specs are kept when the MID has a battery component."""
    battery_section = next(
        section for section in SECTION_SPECS if section["title"] == "Batteriekennzahlen"
    )

    box_specs = _filter_section_box_specs(
        battery_section,
        component_type_set={"battery", "grid", "pv"},
        component_types_provided=True,
        microgrid_id=123,
    )

    assert box_specs
