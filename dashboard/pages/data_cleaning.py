"""
dashboard/pages/data_cleaning.py
─────────────────────────────────
Page: 1.2  Data Cleaning & Preparation
Displays all cleaning steps, their justifications,
and the engineered features. (EDA Requirement 1.2)
"""

import pandas as pd
import streamlit as st

from dashboard.config import badge


def render(df: pd.DataFrame, cleaning_log: list) -> None:
    st.title('1.2  Data Cleaning')
    badge('EDA REQUIREMENT 1.2')

    st.markdown("""
## Overview

The data was already in decent shape. The main tasks were to remove low-quality
parts, clean incomplete rows, and add a few useful columns for this story.
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
    st.markdown('## Added Columns')
    eng = pd.DataFrame([
        ('house_edge',             'float64', '100 − rtp',
            'Shows how much the casino keeps from each $1 bet'),
        ('win_to_bet_ratio',       'float64', 'max_win / min_bet',
            'Compares top possible win with the minimum bet'),
        ('win_to_bet_ratio_capped','float64', 'clip(0, 99th pct)',
            'Same value, but limited so charts are easier to read'),
    ], columns=['Feature', 'Type', 'Formula', 'Purpose'])
    st.dataframe(eng, width='stretch', hide_index=True)

    # ── Sample verification ───────────────────────────────────────────────────
    st.markdown('## Sample of the Clean Data')
    show_cols = [
        'game', 'game_type', 'rtp', 'house_edge', 'volatility',
        'min_bet', 'max_win', 'win_to_bet_ratio', 'max_multiplier',
        'free_spins_feature', 'bonus_buy_available',
    ]
    st.dataframe(df[show_cols].head(20), width='stretch')

    # ── Quality check ─────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        nulls = df[show_cols].isnull().sum()
        nulls = nulls[nulls > 0]
        if len(nulls):
            st.warning(f'Still missing values in shown columns: {nulls.to_dict()}')
        else:
            st.success('✅ No missing values in key columns after cleaning.')
    with col2:
        st.metric('house_edge range',
                  f"{df['house_edge'].min():.1f}% – {df['house_edge'].max():.1f}%")
        st.metric('win_to_bet_ratio range',
                  f"{df['win_to_bet_ratio'].min():.0f}x – {df['win_to_bet_ratio'].max():,.0f}x")
