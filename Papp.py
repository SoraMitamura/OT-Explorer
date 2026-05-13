import streamlit as st
import pandas as pd

# ------------------------------------------------
# page config
# ------------------------------------------------

st.set_page_config(
    page_title="OT Paper Explorer",
    layout="wide"
)

# ------------------------------------------------
# title
# ------------------------------------------------

st.title("OT Paper Explorer")
st.caption("Olfactory Tubercle literature explorer")

# ------------------------------------------------
# load data
# ------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv(
    "papers.csv",
    encoding="utf-8-sig"
)

df = load_data()

# ------------------------------------------------
# sidebar
# ------------------------------------------------

st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Category",
    sorted(df["category"].dropna().unique())
)

species = st.sidebar.multiselect(
    "Species",
    sorted(df["species"].dropna().unique())
)

method = st.sidebar.multiselect(
    "Method",
    sorted(df["method"].dropna().unique())
)

search = st.sidebar.text_input("Search")

# ------------------------------------------------
# filtering
# ------------------------------------------------

filtered = df.copy()

if category:
    filtered = filtered[
        filtered["category"].isin(category)
    ]

if species:
    filtered = filtered[
        filtered["species"].isin(species)
    ]

if method:
    filtered = filtered[
        filtered["method"].isin(method)
    ]

if search:
    filtered = filtered[
        filtered.apply(
            lambda row:
            search.lower() in str(row).lower(),
            axis=1
        )
    ]

# newest first
filtered = filtered.sort_values(
    by="year",
    ascending=False
)

# ------------------------------------------------
# display
# ------------------------------------------------

st.write(f"{len(filtered)} papers")

for _, row in filtered.iterrows():

    with st.container(border=True):

        st.subheader(row["title"])

        st.write(row["authors"])

        st.caption(
            f"{row['journal']} ({row['year']})"
        )

        st.write(row["summary"])

        st.caption(row["tags"])

        st.link_button(
            "Open Paper",
            row["url"]
        )