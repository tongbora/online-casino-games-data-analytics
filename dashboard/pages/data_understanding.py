"""
dashboard/pages/data_understanding.py
──────────────────────────────────────
Page: 1.1  Data Understanding
Covers dataset dimensions, variable descriptions, missing values,
and summary statistics. (EDA Requirement 1.1)
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.config import COLORS, PALETTE, badge, render_chart


# ── Variable reference table ──────────────────────────────────────────────────
VAR_DESC = [
    ('casino',               'object',  'Casino platform name'),
    ('game',                 'object',  'Name of the game'),
    ('provider',             'object',  'Company that made the game'),
    ('rtp',                  'float64', 'Percent of bets paid back to players over time ⭐'),
    ('volatility',           'object',  'Risk level: Low / Medium / High / Very High ⭐'),
    ('jackpot',              'float64', 'Jackpot amount (mostly empty, removed later)'),
    ('country_availability', 'object',  'Countries where the game is available'),
    ('min_bet',              'float64', 'Minimum bet amount ⭐'),
    ('max_win',              'float64', 'Maximum possible win amount ⭐'),
    ('game_type',            'object',  'Main type: slot, poker, table, live, crash, bingo, scratch ⭐'),
    ('game_category',        'object',  'More specific category (example: Video Slot)'),
    ('license_jurisdiction', 'object',  'License authority'),
    ('release_year',         'int64',   'Year the game was released'),
    ('currency',             'object',  'Accepted currencies'),
    ('mobile_compatible',    'bool',    'Whether the game runs on mobile'),
    ('free_spins_feature',   'bool',    'Whether free spins are available ⭐'),
    ('bonus_buy_available',  'bool',    'Whether players can buy into a bonus round ⭐'),
    ('max_multiplier',       'float64', 'Maximum win multiplier ⭐'),
    ('languages',            'object',  'Supported languages'),
    ('last_updated',         'object',  'Last update date for the game record'),
]


def render(df: pd.DataFrame, df_raw: pd.DataFrame) -> None:
    st.title('1.1  Understand the Data')
    badge('EDA REQUIREMENT 1.1')

    # ── Dimensions ────────────────────────────────────────────────────────────
    st.markdown('## What Is in This Dataset?')
    c1, c2, c3, c4 = st.columns(4)
    c1.metric('Rows loaded',       f"{len(df_raw):,}")
    c2.metric('Columns',           f"{df_raw.shape[1]}")
    c3.metric('Numeric columns',   f"{df_raw.select_dtypes('number').shape[1]}")
    c4.metric('Text columns',      f"{df_raw.select_dtypes('object').shape[1]}")

    # ── Variable descriptions ─────────────────────────────────────────────────
    st.markdown('### Simple Column Guide')
    var_df = pd.DataFrame(VAR_DESC, columns=['Column', 'Type', 'Description'])
    st.dataframe(var_df, width='stretch', hide_index=True,
                 column_config={'Column': st.column_config.TextColumn(width='medium')})
    st.caption('⭐ = most important columns used in this dashboard')

    # ── Missing values ────────────────────────────────────────────────────────
    st.markdown('## Missing Data Check')
    col_l, col_r = st.columns(2)

    with col_l:
        missing     = df_raw.isnull().sum().sort_values(ascending=False)
        missing_pct = (missing / len(df_raw) * 100).round(2)
        mv_df = pd.DataFrame({'Missing Count': missing, 'Missing %': missing_pct})
        mv_df = mv_df[mv_df['Missing Count'] > 0]

        if len(mv_df):
            st.dataframe(mv_df, width='stretch')
            fig = px.bar(
                mv_df.reset_index(), x='index', y='Missing %',
                color='Missing %', color_continuous_scale='Reds',
                labels={'index': 'Column'},
                title='Missing Values (%)',
            )
            fig.update_coloraxes(showscale=False)
            render_chart(fig, height=300)
        else:
            st.success('No missing values found.')

    with col_r:
        dups = df_raw.duplicated().sum()
        st.metric('Duplicate rows', f"{dups:,}")
        if dups == 0:
            st.success('✅ No duplicate rows found.')
        else:
            st.warning(f'⚠️ {dups} duplicate rows found.')

        dtype_fig = px.pie(
            names=['Categorical (object)', 'Numeric (float/int)', 'Boolean'],
            values=[7, 5, 3],
            color_discrete_sequence=[COLORS['blue'], COLORS['primary'], COLORS['green']],
            hole=0.5, title='Column Type Breakdown',
        )
        render_chart(dtype_fig, height=280)

    # ── Summary statistics ────────────────────────────────────────────────────
    st.markdown('## Quick Number Summary')
    key_cols = ['rtp', 'min_bet', 'max_win', 'max_multiplier']
    stats = df_raw[key_cols].describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95]).T
    stats.index.name = 'Variable'
    stats = stats.rename(columns={'50%': 'median', 'count': 'n'})
    st.dataframe(stats.round(2), width='stretch')

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('### House Edge (100 − RTP)')
        he_table = pd.DataFrame({
            'Metric': ['Min', '5th Pct', 'Median', 'Mean', '95th Pct', 'Max'],
            'House Edge (%)': [
                100 - df_raw['rtp'].max(),
                100 - df_raw['rtp'].quantile(0.95),
                100 - df_raw['rtp'].median(),
                100 - df_raw['rtp'].mean(),
                100 - df_raw['rtp'].quantile(0.05),
                100 - df_raw['rtp'].min(),
            ],
        })
        st.dataframe(he_table.round(3), width='stretch', hide_index=True)

    with col2:
        st.markdown('### Number of Games by Type')
        gt = df_raw['game_type'].value_counts().reset_index()
        gt.columns = ['Game Type', 'Count']
        gt['% Share'] = (gt['Count'] / gt['Count'].sum() * 100).round(1)
        st.dataframe(gt, width='stretch', hide_index=True)
