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
        '#### A student-friendly data story about casino games and long-run winning chances.'
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

**RTP** means how much money a game gives back over time.
If RTP is 96%, players get back about 96 cents for each $1 bet.
The casino keeps the other 4 cents. We call that the **house edge**.

In this dashboard, we answer:
1. Measure the house edge (100 − RTP) across 50,000 casino games.
2. Compare fairness across game types, volatility, and providers.
3. Investigate whether bonus features (free spins, bonus buy) improve player odds.
4. Identify which providers offer the most player-friendly games.
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
| **1.1 Understand the Data** | What the data contains, missing values, and quick summaries |
| **1.2 Clean the Data** | What was removed, fixed, and added |
| **1.3 One-Thing-at-a-Time View** | Simple views of RTP, house edge, risk, bets, and wins |
| **1.4 Compare Variables** | Put values side by side to spot patterns |
| **1.5 All Charts in One Place** | Quick chart summary on one page |
| **1.6 Main Findings & Conclusion** | Main takeaways and limits of this analysis |
    """)
