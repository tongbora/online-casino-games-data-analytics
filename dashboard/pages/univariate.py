"""
dashboard/pages/univariate.py
──────────────────────────────
Page: 1.3 Univariate Analysis
Single-variable distributions for all key story variables.
(EDA Requirement 1.3)
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.config import COLORS, PALETTE, VOL_ORDER, badge, render_chart


def render(df: pd.DataFrame) -> None:
    st.title('1.3  One-Thing-at-a-Time View')
    badge('EDA REQUIREMENT 1.3')
    st.markdown('*Simple charts that look at one value at a time.*')

    # ── RTP ───────────────────────────────────────────────────────────────────
    st.markdown('## RTP Distribution')
    st.markdown('**Question:** What RTP value is most common?')
    col1, col2 = st.columns([2, 1])
    with col1:
        fig = px.histogram(df, x='rtp', nbins=50,
                           color_discrete_sequence=[COLORS['blue']],
                           labels={'rtp': 'RTP (%)', 'count': 'Games'},
                           title='RTP across all games')
        fig.add_vline(x=df['rtp'].mean(), line_dash='dash',
                      line_color=COLORS['primary'],
                      annotation_text=f"Mean {df['rtp'].mean():.2f}%",
                      annotation_font_color=COLORS['primary'])
        fig.add_vline(x=df['rtp'].median(), line_dash='dot',
                      line_color=COLORS['green'],
                      annotation_text=f"Median {df['rtp'].median():.2f}%",
                      annotation_font_color=COLORS['green'])
        render_chart(fig, height=320)
    with col2:
        st.metric('Mean RTP',   f"{df['rtp'].mean():.2f}%")
        st.metric('Median RTP', f"{df['rtp'].median():.2f}%")
        st.metric('Spread',     f"{df['rtp'].std():.2f}%")
        st.metric('Min RTP',    f"{df['rtp'].min():.2f}%")
        st.metric('Max RTP',    f"{df['rtp'].max():.2f}%")
        st.markdown("""
> **What this means:** Most games sit around 95–99% RTP. With an average near
> 96.2%, the casino keeps about **3.8 cents for every $1 bet**.
        """)

    # ── House Edge ────────────────────────────────────────────────────────────
    st.markdown('## House Edge Distribution (100 − RTP)')
    st.markdown('**Question:** How much does the casino keep?')
    fig = px.histogram(df, x='house_edge', nbins=50,
                       color_discrete_sequence=[COLORS['red']],
                       labels={'house_edge': 'House Edge (%)', 'count': 'Games'},
                       title='How much the casino keeps per bet (house edge = 100 − RTP)')
    fig.add_vline(x=df['house_edge'].mean(), line_dash='dash',
                  line_color=COLORS['primary'],
                  annotation_text=f"Mean {df['house_edge'].mean():.2f}%")
    render_chart(fig, height=320)

    # ── Volatility ────────────────────────────────────────────────────────────
    st.markdown('## Volatility Distribution')
    st.markdown('**Question:** How many games are in each risk group?')
    col1, col2 = st.columns([1, 2])
    with col1:
        vol_counts = df['volatility'].value_counts().reindex(VOL_ORDER).reset_index()
        vol_counts.columns = ['Volatility', 'Count']
        vol_counts['%'] = (vol_counts['Count'] / vol_counts['Count'].sum() * 100).round(1)
        st.dataframe(vol_counts, width='stretch', hide_index=True)
    with col2:
        fig = px.bar(vol_counts, x='Volatility', y='Count',
                     color='Count', color_continuous_scale='YlOrRd',
                     text='%', title='Games by Volatility Level',
                     labels={'Count': 'Number of Games'},
                     category_orders={'Volatility': VOL_ORDER})
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_coloraxes(showscale=False)
        render_chart(fig, height=300)

    # ── Min Bet ───────────────────────────────────────────────────────────────
    st.markdown('## Minimum Bet Distribution')
    st.markdown('**Question:** What minimum bet is most common?')
    col1, col2 = st.columns(2)
    with col1:
        cap99 = df['min_bet'].quantile(0.99)
        fig = px.histogram(df[df['min_bet'] <= cap99], x='min_bet', nbins=40,
                           color_discrete_sequence=[COLORS['green']],
                           labels={'min_bet': 'Minimum Bet ($)'},
                           title='Min Bet Distribution (top 1% trimmed for clarity)')
        render_chart(fig, height=280)
    with col2:
        bet_bins = pd.cut(df['min_bet'],
                          bins=[0, 0.1, 0.5, 1, 2, 999],
                          labels=['< $0.10', '$0.10 – $0.50', '$0.50 – $1', '$1 – $2', '> $2'])
        bet_dist = bet_bins.value_counts().reset_index()
        bet_dist.columns = ['Bet Range', 'Count']
        bet_dist['%'] = (bet_dist['Count'] / bet_dist['Count'].sum() * 100).round(1)
        fig = px.pie(bet_dist, names='Bet Range', values='Count',
                     color_discrete_sequence=PALETTE, hole=0.4,
                     title='Min Bet Tier Breakdown')
        fig.update_traces(textinfo='label+percent')
        render_chart(fig, height=280)

    # ── Max Multiplier ────────────────────────────────────────────────────────
    st.markdown('## Max Multiplier Distribution')
    st.markdown('**Question:** How big can top wins get?')
    col1, col2 = st.columns(2)
    with col1:
        mult_cap = df['max_multiplier'].quantile(0.95)
        fig = px.histogram(df[df['max_multiplier'] <= mult_cap],
                           x='max_multiplier', nbins=50,
                           color_discrete_sequence=[COLORS['purple']],
                           labels={'max_multiplier': 'Max Multiplier (x)'},
                           title=f'Max Multiplier ≤ 95th pct ({mult_cap:.0f}x)')
        render_chart(fig, height=280)
    with col2:
        mult_by_vol = (df.groupby('volatility', observed=True)['max_multiplier']
                         .median().reindex(VOL_ORDER).reset_index())
        mult_by_vol.columns = ['Volatility', 'Median Max Multiplier']
        fig = px.bar(mult_by_vol, x='Volatility', y='Median Max Multiplier',
                     color_discrete_sequence=[COLORS['purple']],
                     text='Median Max Multiplier',
                     labels={'Median Max Multiplier': 'Median Max Multiplier (x)'},
                     title='Median Max Multiplier by Volatility')
        fig.update_traces(texttemplate='%{text:.0f}x', textposition='outside')
        render_chart(fig, height=280)

    # ── Game Type ─────────────────────────────────────────────────────────────
    st.markdown('## Game Type Distribution')
    st.markdown('**Question:** Which game types appear most often?')
    gt = df['game_type'].value_counts().reset_index()
    gt.columns = ['Game Type', 'Count']
    gt['%'] = (gt['Count'] / gt['Count'].sum() * 100).round(1)
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(gt, x='Game Type', y='Count',
                     color='Count', color_continuous_scale='Blues',
                     text='%', title='Games per Type')
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_coloraxes(showscale=False)
        render_chart(fig, height=300)
    with col2:
        fig = px.pie(gt, names='Game Type', values='Count',
                     color_discrete_sequence=PALETTE, hole=0.45,
                     title='Game Type Share')
        fig.update_traces(textinfo='label+percent')
        render_chart(fig, height=300)
