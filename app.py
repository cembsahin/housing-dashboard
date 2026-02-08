"""
Housing Market Dashboard
========================
An interactive dashboard for exploring US housing market trends.

Run with:
    streamlit run app.py
"""

import streamlit as st
import plotly.express as px
import pandas as pd

from utils.data_loader import load_zhvi_data, get_states, filter_data


# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Housing Market Dashboard",
    page_icon="🏠",
    layout="wide",
)

st.title("🏠 Housing Market Dashboard")
st.markdown("Explore US median home value trends using [Zillow Research Data](https://www.zillow.com/research/data/).")


# ── Load data ────────────────────────────────────────────────
@st.cache_data
def get_data():
    """Load data once and cache it so the app stays fast."""
    return load_zhvi_data()


try:
    df = get_data()
except FileNotFoundError:
    st.error(
        "⚠️ Data file not found. Please run the download script first:\n\n"
        "```bash\npython scripts/download_data.py\n```"
    )
    st.stop()


# ── Sidebar filters ─────────────────────────────────────────
st.sidebar.header("Filters")

all_states = get_states(df)

selected_states = st.sidebar.multiselect(
    "Select states to compare",
    options=all_states,
    default=["California", "Texas", "New York", "Florida"],
    help="Pick one or more states to see on the chart.",
)

min_date = df["date"].min().to_pydatetime()
max_date = df["date"].max().to_pydatetime()

date_range = st.sidebar.slider(
    "Date range",
    min_value=min_date,
    max_value=max_date,
    value=(pd.Timestamp("2015-01-01").to_pydatetime(), max_date),
    format="MMM YYYY",
)

# Apply filters
filtered_df = filter_data(
    df,
    states=selected_states if selected_states else None,
    start_date=str(date_range[0]),
    end_date=str(date_range[1]),
)


# ── Main chart: price trends ────────────────────────────────
if filtered_df.empty:
    st.warning("No data to display. Try adjusting your filters.")
    st.stop()

st.subheader("Median Home Value Over Time")

fig_trend = px.line(
    filtered_df,
    x="date",
    y="median_home_value",
    color="state",
    labels={
        "date": "Date",
        "median_home_value": "Median Home Value ($)",
        "state": "State",
    },
    template="plotly_white",
)

fig_trend.update_layout(
    hovermode="x unified",
    yaxis_tickprefix="$",
    yaxis_tickformat=",",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=500,
)

st.plotly_chart(fig_trend, use_container_width=True)


# ── Summary metrics ──────────────────────────────────────────
st.subheader("Current Snapshot")

latest_date = filtered_df["date"].max()
latest_data = filtered_df[filtered_df["date"] == latest_date]

# Show metric cards in columns
cols = st.columns(min(len(latest_data), 4))

for i, (_, row) in enumerate(latest_data.iterrows()):
    col = cols[i % len(cols)]

    # Calculate year-over-year change
    one_year_ago = latest_date - pd.DateOffset(years=1)
    prev = filtered_df[
        (filtered_df["state"] == row["state"])
        & (filtered_df["date"] == filtered_df[filtered_df["date"] <= one_year_ago]["date"].max())
    ]

    yoy_change = None
    if not prev.empty:
        prev_val = prev["median_home_value"].iloc[0]
        yoy_change = (row["median_home_value"] - prev_val) / prev_val * 100

    col.metric(
        label=row["state"],
        value=f"${row['median_home_value']:,.0f}",
        delta=f"{yoy_change:+.1f}% YoY" if yoy_change is not None else None,
    )


# ── Bar chart: latest values comparison ──────────────────────
st.subheader("State Comparison (Latest Month)")

fig_bar = px.bar(
    latest_data.sort_values("median_home_value", ascending=True),
    x="median_home_value",
    y="state",
    orientation="h",
    labels={
        "median_home_value": "Median Home Value ($)",
        "state": "",
    },
    template="plotly_white",
    color="median_home_value",
    color_continuous_scale="Blues",
)

fig_bar.update_layout(
    xaxis_tickprefix="$",
    xaxis_tickformat=",",
    showlegend=False,
    coloraxis_showscale=False,
    height=max(300, len(latest_data) * 40),
)

st.plotly_chart(fig_bar, use_container_width=True)


# ── Footer ───────────────────────────────────────────────────
st.divider()
st.caption(
    f"Data source: Zillow Home Value Index (ZHVI) · Last data point: {latest_date.strftime('%B %Y')} · "
    "Built with Streamlit & Plotly"
)
