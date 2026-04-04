"""
dashboard/pages/introduction.py
────────────────────────────────
Page: 🏠 Introduction
Presents the research question, dataset snapshot, and navigation guide.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.config import COLORS, render_chart


def render(df: pd.DataFrame, df_raw: pd.DataFrame) -> None:
    st.title('Introduction')
    st.markdown('## 🃏 The House Always Wins?')
    st.markdown(
        '#### A casino owner-focused view of margin, product mix, and long-run revenue potential.'
    )
    st.divider()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric('Total Games',    f"{len(df):,}")
    c2.metric('Casinos',        f"{df['casino'].nunique():,}")
    c3.metric('Providers',      f"{df['provider'].nunique():,}")
    c4.metric('Avg House Edge', f"{df['house_edge'].mean():.2f}%")
    c5.metric('Avg RTP',        f"{df['rtp'].mean():.2f}%")

    st.divider()
    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown("""
## Our Research Question

> **How can casino owners use this data to improve profit and revenue?**

**RTP** means how much money a game gives back over time.
If RTP is 96%, players get back about 96 cents for each $1 bet.
The casino keeps the other 4 cents. We call that the **house edge**.

In this dashboard, we answer:
1. Measure the house edge (100 − RTP) across 50,000 casino games.
2. Compare expected margin across game types, volatility, and providers.
3. Evaluate whether bonus features support commercial performance.
4. Identify which providers are strongest for operator profitability.
        """)

    with col_r:
        fig = px.histogram(
            df, x='house_edge', nbins=40,
            color_discrete_sequence=[COLORS['primary']],
            labels={'house_edge': 'House Edge (%)'},
            title='House Edge Distribution (preview)',
        )
        fig.add_vline(
            x=df['house_edge'].mean(), line_dash='dash',
            line_color=COLORS['red'],
            annotation_text=f"Avg {df['house_edge'].mean():.2f}%",
            annotation_font_color=COLORS['red'],
        )
        fig.update_layout(showlegend=False, bargap=0.05)
        render_chart(fig, height=300)

    st.markdown("""
---
#### Navigate using the sidebar →

| Section | Content |
|---|---|
| **1.1 Data Understanding** | Data coverage, missing values, and variable summaries |
| **1.2 Data Cleaning** | What was removed, fixed, and engineered |
| **1.3 Univariate Analysis** | Distribution of core commercial metrics |
| **1.4 Bivariate & Multivariate** | Drivers of house edge across segments |
| **1.5 Visualisations Summary** | Fast executive view of all key charts |
| **1.6 Key Insights & Conclusion** | Owner-focused findings and actions |
    """)
