import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =========================================
# PAGE
# =========================================

st.set_page_config(
    page_title="OT Explorer",
    layout="wide"
)

st.title("OT Explorer")

# =========================================
# SMALLER METRICS
# =========================================

st.markdown("""
<style>
[data-testid="stMetricValue"] {
    font-size: 18px;
}

[data-testid="stMetricLabel"] {
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# SIDEBAR
# =========================================

st.sidebar.header("Controls")

# ----- View mode -----

view_mode = st.sidebar.radio(
    "View",
    ["Coronal", "Dorsal"]
)

# ----- Cluster -----

cluster = st.sidebar.selectbox(
    "Cluster",
    ["D1", "D2"]
)

# ----- Gene -----

gene = st.sidebar.text_input(
    "Gene",
    "Oprm1"
)

# ----- Point size -----

point_size = st.sidebar.slider(
    "Point size",
    1,
    10,
    3
)

# ----- Color scale -----

cmin = st.sidebar.number_input(
    "Color Min",
    value=0.0
)

cmax = st.sidebar.number_input(
    "Color Max",
    value=5.0
)

# =========================================
# SESSION STATE INIT
# =========================================

if "selected_index" not in st.session_state:
    st.session_state.selected_index = None

# =========================================
# RESET SELECTION WHEN STATE CHANGES
# =========================================

current_state = (
    view_mode,
    cluster
)

if "last_state" not in st.session_state:
    st.session_state.last_state = current_state

if current_state != st.session_state.last_state:

    st.session_state.selected_index = None
    st.session_state.last_state = current_state

# =========================================
# LOAD DATA
# =========================================

if cluster == "D1":
    df = pd.read_csv("c61_whole_OT.csv")
else:
    df = pd.read_csv("c62_whole_OT.csv")

# =========================================
# SECTION NUMBER
# =========================================

df["section_num"] = (
    df["brain_section_label"]
    .astype(str)
    .str.split(".")
    .str[-1]
    .astype(int)
)

# =========================================
# DORSAL MAP
# =========================================

sections_plot = [55,54,53,52,51,50,49,48,47]

section_map = {
    s:i for i,s in enumerate(sections_plot)
}

gap = 0.24
jitter = 0.1

df["dorsal_y"] = (
    df["section_num"]
    .map(section_map)
    * gap
)

# ----- FIXED JITTER -----

np.random.seed(42)

df["dorsal_y"] += (
    np.random.rand(len(df)) - 0.5
) * 2 * jitter

# =========================================
# CORONAL MODE
# =========================================

if view_mode == "Coronal":

    section = st.sidebar.number_input(
        "Section",
        min_value=int(df["section_num"].min()),
        max_value=int(df["section_num"].max()),
        value=int(df["section_num"].max()),
        step=1
    )

    df = df[df["section_num"] == section]

# =========================================
# RESET INDEX
# =========================================

df = df.reset_index(drop=True)

# =========================================
# CHECK GENE
# =========================================

if gene not in df.columns:

    st.error(f"Gene '{gene}' not found.")

    st.write(df.columns.tolist())

    st.stop()

# =========================================
# Y AXIS
# =========================================

if view_mode == "Coronal":
    y_plot = "y"
else:
    y_plot = "dorsal_y"

# =========================================
# MAIN FIGURE
# =========================================

fig = px.scatter(
    df,
    x="x",
    y=y_plot,
    color=gene,
    hover_data=[
        gene,
        "brain_section_label",
        "x",
        "y"
    ],
    color_continuous_scale="Viridis"
)

# ----- Color scale -----

fig.update_coloraxes(
    cmin=cmin,
    cmax=cmax
)

# ----- Marker size -----

fig.update_traces(
    marker=dict(size=point_size)
)

# ----- Reverse y axis -----

fig.update_yaxes(
    autorange="reversed"
)

# ----- Hide axes -----

fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)

# =========================================
# LAYOUT
# =========================================

fig.update_layout(
    template="simple_white",

    width=1400,
    height=500,

    margin=dict(
        l=0,
        r=0,
        t=40,
        b=0
    ),

    title=f"{gene} | {cluster} | {view_mode}"
)

# =========================================
# CLEAR SELECTION BUTTON
# =========================================

clear_selection = st.button(
    "Clear Selection"
)

if clear_selection:

    st.session_state.selected_index = None
    st.rerun()
# =========================================
# TOP COLUMNS
# =========================================

plot_col, stat_col = st.columns([5,1])

# =========================================
# PLOT PANEL
# =========================================

with plot_col:

    clicked = st.plotly_chart(
        fig,
        key="main_plot",
        on_select="rerun",
        selection_mode=("lasso", "box")
    )

    # ----- Update selection -----

    if (
        not clear_selection
        and clicked.selection
        and "points" in clicked.selection
        and len(clicked.selection["points"]) > 0
    ):

        points = clicked.selection["points"]

        st.session_state.selected_index = [
            p["point_index"]
            for p in points
        ]

# =========================================
# SELECTED DATA
# =========================================

if st.session_state.selected_index is not None:

    valid_index = [
        i for i in st.session_state.selected_index
        if i < len(df)
    ]

    if len(valid_index) > 0:

        selected_df = df.iloc[valid_index]

    else:

        selected_df = df

else:

    selected_df = df

# =========================================
# STATISTICS PANEL
# =========================================

with stat_col:

    st.subheader("Statistics")

    expr = selected_df[gene]

    st.metric(
        "Cells",
        len(expr)
    )

    st.metric(
        "Mean",
        round(expr.mean(), 3)
    )

    st.metric(
        "Median",
        round(expr.median(), 3)
    )

    st.metric(
        "Max",
        round(expr.max(), 3)
    )

# =========================================
# HISTOGRAM
# =========================================

st.subheader("Histogram")

hist_fig = px.histogram(
    selected_df,
    x=gene,
    nbins=50
)

hist_fig.update_layout(
    template="simple_white",

    width=1400,
    height=250,

    margin=dict(
        l=0,
        r=0,
        t=20,
        b=0
    )
)

st.plotly_chart(hist_fig)
