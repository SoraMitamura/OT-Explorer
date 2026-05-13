import streamlit as st
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="OT Paper Explorer",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("OT Paper Explorer")
st.caption("Olfactory Tubercle literature explorer")

# =========================================================
# LOAD DATA
# =========================================================

def load_data():

    df = pd.read_excel("papers.xlsx")

    # year を数値化
    if "year" in df.columns:

        df["year"] = pd.to_numeric(
            df["year"],
            errors="coerce"
        )

    return df


df = load_data()

# =========================================================
# SEARCH
# =========================================================

search = st.text_input(
    "Search title"
)

# =========================================================
# FILTERING
# =========================================================

filtered = df.copy()

if search:

    filtered = filtered[
        filtered["title"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

# =========================================================
# SORT
# =========================================================

if "year" in filtered.columns:

    filtered = filtered.sort_values(
        by="year",
        ascending=False
    )

# =========================================================
# RESULT COUNT
# =========================================================

st.write(f"{len(filtered)} papers")

st.divider()

# =========================================================
# PAPER LIST
# =========================================================

for _, row in filtered.iterrows():

    col1, col2 = st.columns([1, 12])

    # -------------------------
    # year
    # -------------------------

    with col1:

        if pd.notna(row["year"]):

            st.write(int(row["year"]))

    # -------------------------
    # title
    # -------------------------

    with col2:

        st.markdown(
            f"""
            <a href="{row['url']}"
               target="_blank"
               style="
                   text-decoration:none;
                   font-size:18px;
                   font-weight:500;
               ">
               {row['title']}
            </a>
            """,
            unsafe_allow_html=True
        )




# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption("Built with Streamlit")
