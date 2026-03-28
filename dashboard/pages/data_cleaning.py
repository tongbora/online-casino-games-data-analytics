"""
dashboard/pages/data_cleaning.py
─────────────────────────────────
Page: 3.2 Data Cleaning & Preparation
Displays all cleaning steps, their justifications,
and the engineered features. (EDA Requirement 3.2)
"""

import pandas as pd
import streamlit as st

from dashboard.config import badge


def render(df: pd.DataFrame, cleaning_log: list) -> None:
    st.title('3.2  Data Cleaning & Preparation')
    badge('EDA REQUIREMENT 3.2')

    st.markdown("""
## Overview

The raw dataset was generally clean. The main tasks were **removing an unusable
column**, **handling sparse rows**, and **engineering features** that directly
support the "House Always Wins?" narrative.
    """)

    # ── Row counts ────────────────────────────────────────────────────────────
    st.markdown(f'**Rows after cleaning:** `{len(df):,}`')

    # ── Cleaning steps ────────────────────────────────────────────────────────
    st.markdown('## Cleaning Steps')
    for step, (action, justification, icon) in enumerate(cleaning_log, 1):
        st.markdown(f"""
<div class="cleaning-step">
<strong>{icon} Step {step}: {action}</strong><br/>
<span style="color:#8b949e; font-size:0.88rem;">{justification}</span>
</div>""", unsafe_allow_html=True)

    # ── Engineered features ───────────────────────────────────────────────────
    st.markdown('## Engineered Features')
    eng = pd.DataFrame([
        ('house_edge',             'float64', '100 − rtp',
         'Core measure of casino advantage per unit bet'),
        ('win_to_bet_ratio',       'float64', 'max_win / min_bet',
         'Maximum potential return relative to entry stake'),
        ('win_to_bet_ratio_capped','float64', 'clip(0, 99th pct)',
         'Outlier-capped version used in visualisations only'),
    ], columns=['Feature', 'Type', 'Formula', 'Purpose'])
    st.dataframe(eng, use_container_width=True, hide_index=True)

    # ── Sample verification ───────────────────────────────────────────────────
    st.markdown('## Cleaned Dataset Sample')
    show_cols = [
        'game', 'game_type', 'rtp', 'house_edge', 'volatility',
        'min_bet', 'max_win', 'win_to_bet_ratio', 'max_multiplier',
        'free_spins_feature', 'bonus_buy_available',
    ]
    st.dataframe(df[show_cols].head(20), use_container_width=True)

    # ── Quality check ─────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        nulls = df[show_cols].isnull().sum()
        nulls = nulls[nulls > 0]
        if len(nulls):
            st.warning(f'Remaining nulls in shown columns: {nulls.to_dict()}')
        else:
            st.success('✅ No missing values in key columns after cleaning.')
    with col2:
        st.metric('house_edge range',
                  f"{df['house_edge'].min():.1f}% – {df['house_edge'].max():.1f}%")
        st.metric('win_to_bet_ratio range',
                  f"{df['win_to_bet_ratio'].min():.0f}x – {df['win_to_bet_ratio'].max():,.0f}x")
