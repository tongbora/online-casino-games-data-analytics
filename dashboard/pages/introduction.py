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
    st.markdown('# 🃏 The House Always Wins?')
    st.markdown(
        '#### Analysing the relationship between RTP, house edge, volatility, '
        'and player odds across 1.2 M casino game records.'
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

> **Does the data support the saying "The House Always Wins"?**

The **Return to Player (RTP)** is the percentage of total bets a game pays back
to players over time. If a game has 96 % RTP, the casino keeps an average of
**4 ¢ for every $1 bet** — this is the **house edge**.

This EDA investigates:
- How large is the house edge across the game library?
- Which game types, providers, and volatility levels favour the house most?
- How does the maximum possible win compare to the minimum bet (reward-to-risk)?
- Do bonus features genuinely improve player returns?
- Has the industry become more or less player-friendly over time?
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
| **3.1 Data Understanding** | Shape, types, missing values, summary stats |
| **3.2 Data Cleaning** | Steps taken, feature engineering justifications |
| **3.3 Univariate Analysis** | Distributions of RTP, house edge, volatility, bets, wins |
| **3.4 Bivariate & Multivariate** | Relationships, correlations, grouped comparisons |
| **3.5 Visualisations Summary** | All key charts in one view |
| **3.6 Key Insights & Conclusion** | 5 findings + limitations |
    """)
