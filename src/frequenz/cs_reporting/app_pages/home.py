# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Home page introducing the Frequenz reporting suite."""

from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st

from frequenz.cs_reporting.rep_cs_core.page_spec import PageSpec

PACKAGE_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = PACKAGE_DIR / "assets"
BACKGROUND_PATH = ASSETS_DIR / "neustrom_background.png"
HERO_CARD_STYLE = """
        position: fixed;
        top: 40%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: min(92vw, 960px);
        background: rgba(255, 255, 255, 0.88);
        border-radius: 16px;
        padding: 34px 40px;
        box-shadow: 0 24px 60px rgba(0, 0, 0, 0.30);
        text-align: left;
        line-height: 1.6;
    """


def _set_page_bg(image_path: Path) -> None:
    """Set a base64-encoded background image for the page.

    Args:
        image_path: Path to the background image file.

    Returns:
        Streamlit styles are injected directly.
    """
    if not image_path.exists():
        st.warning(f"Background image not found: {image_path}")
        return

    b64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{b64}");
            background-size: cover;            /* fill full width */
            background-repeat: no-repeat;
            background-position: center top;   /* keep main subject visible */
            background-attachment: fixed;      /* stays still on scroll */
            background-color: #ffffff;         /* fallback color */
            min-height: 100vh;
        }}
        [data-testid="stHeader"] {{ background: transparent; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render() -> None:
    """Render the landing page with a welcome message and background.

    Returns:
        Streamlit components are rendered directly.
    """
    _set_page_bg(BACKGROUND_PATH)

    # Content on top of the background
    st.markdown(
        f"""
        <div style="{HERO_CARD_STYLE.strip()}">
            <h1>Welcome to the Frequenz Reporting Suite</h1>
            <p><em>Operational intelligence at a glance.</em></p>
            <p>
                The Frequenz Reporting Suite provides visibility and insights across your energy
                infrastructure. Use the navigation sidebar to explore live dashboards, solar
                performance, and asset optimization tools tailored for your organization.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


PAGE = PageSpec(
    key="home",
    title="Home",
    icon="🏠",
    order=0,
    render=render,
)
