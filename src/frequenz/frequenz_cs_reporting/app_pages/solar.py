# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Placeholder for the solar monitoring page."""

from __future__ import annotations

# import streamlit as st
# import pandas as pd
# from frequenz.frequenz_cs_reporting.rep_cs_core.logging_utils import get_logger
# from frequenz.frequenz_cs_reporting.rep_cs_core.utils import pretty_json
# from frequenz.frequenz_cs_reporting.services import data_loader
# from frequenz.frequenz_cs_reporting.services import reporting

# log = get_logger(__name__)

# st.title("Solar Monitoring")
# st.caption("Run reusable notebook functions/pipelines")

# tab1, tab2 = st.tabs(["Run pipeline", "Run specific cell"])

# with tab1:
#     st.subheader("Pipeline")
#     state = {}
#     if st.button("Run pipeline"):
#         out = reporting.run_pipeline(state)
#         st.code(pretty_json(out))

# with tab2:
#     st.subheader("Run a wrapped code cell")
#     cell_num = st.number_input("Cell number", min_value=1, step=1)
#     if st.button("Run cell"):
#         fn_name = f"run_cell_{int(cell_num)}"
#         if hasattr(reporting, fn_name):
#             out = getattr(reporting, fn_name)({})
#             st.success(f"Executed {fn_name}")
#         else:
#             st.error(f"No such function: {fn_name}")
