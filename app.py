import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="OT Scope",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

div.stLinkButton a {

    background-color: #111827 !important;

    color: white !important;

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 14px;

    padding: 10px 16px;

    text-decoration: none;

    display: inline-block;

    width: 100%;

    text-align: center;

    transition: 0.2s;
}

div.stLinkButton a:hover {

    border: 1px solid #22c55e;

    color: white !important;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* selected value */

div[data-baseweb="select"] div {
    color: black !important;
}

/* dropdown menu items */

ul[role="listbox"] li {
    color: black !important;
}

/* dropdown text */

div[data-baseweb="popover"] * {
    color: black !important;
}


/* =======================================================
GLOBAL
======================================================= */

.stApp {
    background: linear-gradient(
        180deg,
        #050816 0%,
        #071225 100%
    );
    color: white;
}

/* =======================================================
SIDEBAR
======================================================= */

section[data-testid="stSidebar"] {

    background: linear-gradient(
        180deg,
        #09101f 0%,
        #0b1325 100%
    );

    width: 320px !important;

    border-right: 1px solid rgba(255,255,255,0.05);
}

/* =======================================================
SIDEBAR SPACING
======================================================= */

div[role="radiogroup"] > label {
    margin-bottom: -8px;
}

div[data-baseweb="select"] {
    margin-bottom: -8px;
}

div[data-baseweb="input"] {
    margin-bottom: -8px;
}

/* =======================================================
TEXT
======================================================= */

h1, h2, h3, h4, h5, h6, p, label, div {
    color: white;
}

/* =======================================================
METRICS
======================================================= */

    font-size: 30px !important;
    line-height: 1.0 !important;

    color: white !important;
}

    padding-top: 0px !important;
    padding-bottom: 0px !important;

    margin-top: -8px !important;
    margin-bottom: -8px !important;
}

div[data-testid="stMetricLabel"] {

    font-size: 24px !important;
    color: #9ca3af !important;
}

div[data-testid="stMetricValue"] {

    font-size: 30px !important;
    line-height: 1.0 !important;

    color: white !important;
}

/* =======================================================
BUTTONS
======================================================= */

.stButton button {
div.stLinkButton a {

    background-color: #111827 !important;

    color: white !important;

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 14px;

    padding: 10px 16px;

    text-decoration: none;

    display: block;

    width: 50%;

    margin-left: auto;
    margin-right: auto;

    text-align: center;

    transition: 0.2s;
}
    background: #111827;

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 14px;

    color: white;

    width: 100%;

    padding: 10px;

    transition: 0.2s;
}

.stButton button:hover {
    border: 1px solid #22c55e;
}

/* =======================================================
DOWNLOAD BUTTON
======================================================= */

.stDownloadButton button {

    background: rgba(239,68,68,0.08);

    border: 1px solid rgba(239,68,68,0.5);

    border-radius: 14px;

    color: #ff5f5f;

    width: 100%;

    padding: 10px;

    transition: 0.2s;
}

.stDownloadButton button:hover {

    background: rgba(239,68,68,0.15);
}

/* =======================================================
STATISTICS CARD
======================================================= */

.card {

    background: rgba(17,24,39,0.65);

    border: 1px solid rgba(255,255,255,0.06);

    border-radius: 24px;

    padding: 20px;

    backdrop-filter: blur(12px);
}

/* =======================================================
REMOVE TOP PADDING
======================================================= */

.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIZE PARAMETERS
# =========================================================

coronal_width = 800
coronal_height = 440

dorsal_width = 800
dorsal_height = 440

gap = 0.24
jitter = 0.10

# =========================================================
# SESSION STATE
# =========================================================

if "selected_index" not in st.session_state:
    st.session_state.selected_index = None

if "plot_key" not in st.session_state:
    st.session_state.plot_key = 0

# =========================================================
# SIDEBAR
# =========================================================

logo = Image.open("otscope_logo.png")

st.sidebar.image(
    logo,
    use_container_width=True
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW
# ---------------------------------------------------------

view_mode = st.sidebar.radio(
    "View",
    ["Coronal", "Pseudo-Dorsal"]
)

# ---------------------------------------------------------
# CLUSTER
# ---------------------------------------------------------

cluster = st.sidebar.selectbox(
    "Cluster",
    ["Pdyn(+)Penk(-) D1", "D2", "Pdyn(+)Penk(+) D1", "ICj", "Cap"],
    index=0
)
# =========================================================
# LOAD DATA
# =========================================================

if cluster == "Pdyn(+)Penk(-) D1":

    df = pd.read_csv("c61_whole_OT.csv")

elif cluster == "D2":

    df = pd.read_csv("c62_whole_OT.csv")

elif cluster == "Pdyn(+)Penk(+) D1":

    df = pd.read_csv("c63_whole_OT.csv")

elif cluster == "ICj":

    df = pd.read_csv("whole_ICj.csv")

else:

    df = pd.read_csv("c264_whole_Cap.csv")

# ---------------------------------------------------------
# GENE LIST
# ---------------------------------------------------------

gene_list = sorted([
    col for col in df.columns
    if col not in [
        "x",
        "y",
        "z",
        "dorsal_y",
        "section_num",
        "cell_label",
        "brain_section_label"
    ]
])

# ---------------------------------------------------------
# GENE SELECTBOX
# ---------------------------------------------------------

gene = st.sidebar.selectbox(
    "Gene",
    gene_list,
    index=gene_list.index("Oprm1")
    if "Oprm1" in gene_list else 0
)
# =========================================================
# SECTION NUMBER
# =========================================================

df["section_num"] = (
    df["brain_section_label"]
    .astype(str)
    .str.split(".")
    .str[-1]
    .astype(int)
)

# =========================================================
# CORONAL MODE
# =========================================================

if view_mode == "Coronal":

    section = st.sidebar.number_input(
        "Section",
        min_value=int(df["section_num"].min()),
        max_value=int(df["section_num"].max()),
        value=int(df["section_num"].max()),
        step=1
    )

    df = df[df["section_num"] == section]

# ---------------------------------------------------------
# POINT SIZE
# ---------------------------------------------------------

point_size = st.sidebar.slider(
    "Point size",
    1,
    10,
    5
)
# ---------------------------------------------------------
# COLOR RANGE
# ---------------------------------------------------------

#cmin = st.sidebar.number_input(
#    "Min",
#    value=0.0,
#    step=0.1,
#    format="%.1f"
#)
cmin = 0;
cmax = st.sidebar.number_input(
    "Max",
    value=5.0,
    step=0.5,
    format="%.1f"
)

# =========================================================
# RESET STATE
# =========================================================

current_state = (
    view_mode,
    cluster
)

if "last_state" not in st.session_state:
    st.session_state.last_state = current_state

if current_state != st.session_state.last_state:

    st.session_state.selected_index = None

    st.session_state.plot_key += 1

    st.session_state.last_state = current_state





# =========================================================
# DORSAL MAP
# =========================================================

sections_plot = [55,54,53,52,51,50,49,48,47]

section_map = {
    s:i for i,s in enumerate(sections_plot)
}

df["dorsal_y"] = (
    df["section_num"]
    .map(section_map)
    * gap
)

np.random.seed(42)

df["dorsal_y"] += (
    np.random.rand(len(df)) - 0.5
) * 2 * jitter



# =========================================================
# RESET INDEX
# =========================================================

df = df.reset_index(drop=True)

# =========================================================
# CHECK GENE
# =========================================================

if gene not in df.columns:

    st.error(f"Gene '{gene}' not found.")
    st.stop()

# =========================================================
# Y AXIS
# =========================================================

if view_mode == "Coronal":
    y_plot = "y"
else:
    y_plot = "dorsal_y"

# =========================================================
# FIGURE
# =========================================================

fig = px.scatter(
    df,
    x="x",
    y=y_plot,
    color=gene,
    hover_data=[
        gene,
        "brain_section_label"
    ],
    color_continuous_scale="Viridis",
    template="plotly_dark"
)

# =========================================================
# COLOR SCALE
# =========================================================

fig.update_coloraxes(

    cmin=cmin,
    cmax=cmax,

    colorbar=dict(
        title="log2(CPM+1)",
        thickness=20,
        title_font=dict(size=18),
        tickfont=dict(size=14)
    )
)

# =========================================================
# MARKER SIZE
# =========================================================

fig.update_traces(
    marker=dict(
        size=point_size
    )
)

# =========================================================
# AXIS
# =========================================================

if view_mode == "Coronal":

    fig.update_yaxes(
        autorange="reversed",
        scaleanchor="x"
    )

    fig_width = coronal_width
    fig_height = coronal_height

else:

    fig.update_yaxes(
        autorange="reversed"
    )

    fig_width = dorsal_width
    fig_height = dorsal_height

fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)

# =========================================================
# LAYOUT
# =========================================================

fig.update_layout(

    width=fig_width,
    height=fig_height,

    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",

    font=dict(
        color="white"
    ),

    margin=dict(
        l=0,
        r=0,
        t=20,
        b=0
    )
)

# =========================================================
# MAIN LAYOUT
# =========================================================

plot_col, stat_col = st.columns([7,2.5])

# =========================================================
# PLOT
# =========================================================

with plot_col:

    st.markdown(
        f"""
        <h2 style="
        font-size:28px;
        font-weight:700;
        margin-top:40px;
        margin-bottom:-10px;
        padding-left:5px;
        line-height:1.0;
        ">
        {gene} | {cluster} | {view_mode} (L⟷M)
        </h2>
        """,
        unsafe_allow_html=True
    )

    clicked = st.plotly_chart(
        fig,
        key=f"main_plot_{st.session_state.plot_key}",
        on_select="rerun",
        selection_mode=("lasso", "box"),
        config={"displayModeBar": True}
    )

    # -----------------------------------------------------
    # UPDATE SELECTION
    # -----------------------------------------------------

    if (
        clicked is not None
        and clicked.selection
        and "points" in clicked.selection
        and len(clicked.selection["points"]) > 0
    ):

        points = clicked.selection["points"]

        st.session_state.selected_index = [
            p["point_index"]
            for p in points
        ]
# =========================================================
# SELECTED DATA
# =========================================================

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
# =========================================================
# HISTOGRAM
# =========================================================

st.markdown(
    f"""
    <h2 style="
    font-size:26px;
    font-weight:700;
    margin-top:-60px;
    margin-bottom:-70px;
    padding-left:5px;
    ">
    Histogram
    </h2>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# HISTOGRAM FIGURE
# ---------------------------------------------------------

hist_fig = px.histogram(
    selected_df,
    x=gene,
    nbins=50,
    template="plotly_dark"
)

# ---------------------------------------------------------
# LAYOUT
# ---------------------------------------------------------

hist_fig.update_layout(

    autosize=False,

    width=500,
    height=180,

    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",

    font=dict(
        color="white",
        size=18
    ),

    margin=dict(
        l=0,
        r=0,
        t=0,
        b=0
    )
)

# ---------------------------------------------------------
# AXES
# ---------------------------------------------------------

hist_fig.update_xaxes(

    tickfont=dict(size=18),

    title=dict(
        text="Expression (log2(CPM+1))",
        font=dict(size=24)
    )
)

hist_fig.update_yaxes(

    tickfont=dict(size=18),

    title=dict(
        text="Count",
        font=dict(size=24)
    )
)

# ---------------------------------------------------------
# HISTOGRAM CONTAINER
# ---------------------------------------------------------

hist_container = st.container()

with hist_container:

    st.plotly_chart(
        hist_fig,
        use_container_width=False,
        config={"displayModeBar": False}
    )

# =========================================================
# STATISTICS CARD
# =========================================================

with stat_col:

    
    # -----------------------------------------------------
    # STATISTICS TITLE
    # -----------------------------------------------------

    st.markdown("""
    <h2 style="
    font-size:24px;
    font-weight:650;
    margin-top:20px;
    margin-bottom:8px;
    line-height:1.1;
    ">
    Statistics
    </h2>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

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
    # -----------------------------------------------------
    # CLEAR BUTTON
    # -----------------------------------------------------

    clear_selection = st.button(
        "Clear Selection",
        key="clear_selection_button"
    )

    if clear_selection:

        st.session_state.selected_index = None

        st.session_state.plot_key += 1

        st.rerun()

    

    # -----------------------------------------------------
    # DOWNLOAD CSV
    # -----------------------------------------------------

    csv = selected_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Selected CSV",
        data=csv,
        file_name=f"{gene}_{cluster}_selected.csv",
        mime="text/csv",
        key="download_selected_csv"
    )

    # -----------------------------------------------------
    # LINK BUTTON
    # -----------------------------------------------------

    st.markdown(
        "<div style='height:20px'></div>",
        unsafe_allow_html=True
    )

    st.link_button(
        "What is OT?",
        "https://www.frontiersin.org/journals/neural-circuits/articles/10.3389/fncir.2020.577880/full",
        use_container_width=False
    )
    
