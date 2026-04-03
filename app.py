"""
app.py — Entry point
────────────────────
Bootstraps the Streamlit app: injects CSS, renders the sidebar,
loads data, and delegates rendering to the correct page module.

Run:  streamlit run app.py
"""

import sys
from pathlib import Path

import streamlit as st

# ── Ensure project root is on sys.path ────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

# ── Dashboard modules ─────────────────────────────────────────────────────────
from dashboard.config import (
    SECTIONS,
    configure_page,
    inject_css,
)
from dashboard.data import SAMPLE_ROWS, load_clean, load_raw
from dashboard.pages import (
    about_author,
    bivariate,
    data_cleaning,
    data_understanding,
    insights,
    introduction,
    univariate,
    visualisations,
)

# ── Page config (must be first Streamlit call) ────────────────────────────────
configure_page()
inject_css()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('## 🃏 The House Always Wins?')
    st.markdown('**PPIU — Data Analytics EDA**')
    st.caption('Story Angle #2')
    st.divider()

    page = st.radio('Navigate', SECTIONS, label_visibility='collapsed')

    st.divider()
    st.markdown('**Dataset options**')
    use_sample = st.checkbox('Use sample dataset (fastest)', value=True)
    nrows = SAMPLE_ROWS if use_sample else None
    st.caption(f"{'50,000-row sample' if use_sample else 'Full 1.2 M dataset'}")

# ── Load data ────────────────────────────────────────────────────────────────
df_raw             = load_raw(nrows, use_sample=use_sample)
df, cleaning_log   = load_clean(nrows, use_sample=use_sample)

# ── Route to page ─────────────────────────────────────────────────────────────
if   page == SECTIONS[0]: introduction.render(df, df_raw)
elif page == SECTIONS[1]: data_understanding.render(df, df_raw)
elif page == SECTIONS[2]: data_cleaning.render(df, cleaning_log)
elif page == SECTIONS[3]: univariate.render(df)
elif page == SECTIONS[4]: bivariate.render(df)
elif page == SECTIONS[5]: visualisations.render(df)
elif page == SECTIONS[6]: insights.render(df)
elif page == SECTIONS[7]: about_author.render()
