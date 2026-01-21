# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Chart rendering functions for the reporting module."""

import plotly.express as px
import plotly.graph_objects as go


# pylint: disable=too-many-locals
def plot_percentage_bar(
    data_points: dict[str, float | None], total_key: str
) -> go.Figure:
    """Render a stacked percentage bar showing contributions to a total.

    Args:
        data_points: Mapping of labels to numeric values.
        total_key: Key representing the total value in ``data_points``.

    Returns:
        Plotly figure containing the stacked bar chart.

    Raises:
        ValueError: If ``total_key`` is missing from ``data_points``.
    """
    if total_key not in data_points:
        raise ValueError(f"Total key '{total_key}' not found.")

    # sanitize values
    clean = {k: (float(v) if v is not None else 0.0) for k, v in data_points.items()}
    total = clean[total_key]
    if total <= 0:
        fig = go.Figure()
        fig.update_layout(
            showlegend=False,
            annotations=[
                {
                    "text": "No data to display: total is zero or negative",
                    "x": 0.5,
                    "xref": "paper",
                    "y": 0.5,
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 14, "color": "gray"},
                }
            ],
        )
        return fig

    # segments
    used = sum(v for k, v in clean.items() if k != total_key)
    segments = {k: v for k, v in clean.items() if k != total_key and v > 0}
    display_base = max(total, used)
    leftover = max(0.0, display_base - used)

    # Only add "Others" if it has a positive value
    if leftover > 0:
        segments["Others"] = leftover

    # compute percentages
    seg_with_pct = [
        (k, v, (v / display_base * 100.0 if display_base > 0 else 0.0))
        for k, v in segments.items()
    ]

    # sort left → right by descending absolute value (so largest chunk comes first in bar)
    seg_with_pct.sort(key=lambda x: x[1], reverse=True)

    # colors
    palette = px.colors.qualitative.Plotly
    color_map, i = {}, 0
    for label, _, _ in seg_with_pct:
        if label == "Others":
            color_map[label] = "#7f7f7f"
        else:
            color_map[label] = palette[i % len(palette)]
            i += 1

    # figure
    fig = go.Figure()

    for label, value, pct in seg_with_pct:
        text = f"{pct:.1f}%" if value > 0 else None
        fig.add_trace(
            go.Bar(
                x=[pct],
                y=[""],
                name=label,
                orientation="h",
                marker={"color": color_map[label]},
                text=text,
                textposition="inside",
                insidetextanchor="middle",
                hovertemplate=f"{label}: %{{x:.1f}}%<extra></extra>",
            )
        )

    fig.update_layout(
        barmode="stack",
        xaxis={
            "title": None,
            "range": [0, 100],
            "tickformat": ".0f%%",  # show % ticks
            "showgrid": False,
            "zeroline": False,
        },
        yaxis={"showticklabels": False},
        height=160,  # controls bar thickness
        margin={"l": 0, "r": 0, "t": 20, "b": 40},
        legend={
            "orientation": "h",
            "yanchor": "top",
            "y": -0.35,  # place legend below bar
            "xanchor": "center",
            "x": 0.5,
        },
    )

    fig.update_layout(
        annotations=[
            {
                "text": f"{total_key}: {total:.0f} kWh",
                "x": 0.5,
                "xref": "paper",
                "y": 1.3,
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 14, "color": "black"},
            }
        ],
        margin={"t": 40},  # add extra top margin for annotation
    )
    return fig
