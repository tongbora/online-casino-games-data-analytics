"""
dashboard/pages/bivariate.py
─────────────────────────────
Page: 1.4 Bivariate & Multivariate Analysis
Relationships between variables supporting the "House Always Wins?" narrative.
(EDA Requirement 1.4)
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from dashboard.config import COLORS, PALETTE, VOL_ORDER, badge, render_chart, theme


def render(df: pd.DataFrame) -> None:
    st.title('1.4  Bivariate & Multivariate Analysis')
    badge('EDA REQUIREMENT 1.4')
    st.markdown('*Relationships between variables that support the narrative.*')

    # ── House edge by game type ───────────────────────────────────────────────
    st.markdown('## House Edge by Game Type')
    col1, col2 = st.columns([2, 1])
    with col1:
        fig = px.box(df, x='game_type', y='house_edge',
                     color='game_type', color_discrete_sequence=PALETTE,
                     labels={'game_type': 'Game Type', 'house_edge': 'House Edge (%)'},
                     title='House Edge Distribution by Game Type')
        fig.update_layout(showlegend=False)
        render_chart(fig, height=380)
    with col2:
        he_by_type = (df.groupby('game_type', observed=True)['house_edge']
                        .agg(['mean', 'median', 'std'])
                        .round(3).reset_index())
        he_by_type.columns = ['Game Type', 'Mean HE%', 'Median HE%', 'Std']
        he_by_type = he_by_type.sort_values('Mean HE%', ascending=False)
        st.dataframe(he_by_type, width='stretch', hide_index=True)
        st.caption('Higher mean house edge = casino keeps more per $1 bet.')

    # ── RTP by volatility ─────────────────────────────────────────────────────
    st.markdown('## RTP vs Volatility')
    col1, col2 = st.columns(2)
    with col1:
        fig = px.violin(df, x='volatility', y='rtp',
                        color='volatility', box=True,
                        category_orders={'volatility': VOL_ORDER},
                        color_discrete_sequence=PALETTE,
                        labels={'rtp': 'RTP (%)', 'volatility': 'Volatility'},
                        title='RTP Distribution by Volatility (Violin + Box)')
        render_chart(fig, height=350)
    with col2:
        rtp_vol = (df.groupby('volatility', observed=True)['rtp']
                     .agg(['mean', 'median', 'count'])
                     .round(3).reset_index())
        rtp_vol.columns = ['Volatility', 'Mean RTP%', 'Median RTP%', 'Count']
        fig = px.bar(rtp_vol, x='Volatility', y='Mean RTP%',
                     color='Mean RTP%', color_continuous_scale='RdYlGn',
                     category_orders={'Volatility': VOL_ORDER},
                     range_color=[94, 98], text='Mean RTP%',
                     title='Mean RTP by Volatility Level')
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig.update_coloraxes(showscale=False)
        render_chart(fig, height=350)

    # ── Bonus features vs RTP ─────────────────────────────────────────────────
    st.markdown('## Do Bonus Features Improve Player Odds?')
    col1, col2 = st.columns(2)
    with col1:
        bonus_compare = pd.DataFrame({
            'Group': ['No Free Spins', 'Has Free Spins', 'No Bonus Buy', 'Has Bonus Buy'],
            'Mean RTP (%)': [
                df[~df['free_spins_feature']]['rtp'].mean(),
                df[df['free_spins_feature']]['rtp'].mean(),
                df[~df['bonus_buy_available']]['rtp'].mean(),
                df[df['bonus_buy_available']]['rtp'].mean(),
            ],
        }).round(3)
        fig = px.bar(bonus_compare, x='Group', y='Mean RTP (%)',
                     color='Mean RTP (%)', color_continuous_scale='RdYlGn',
                     range_color=[95, 98], text='Mean RTP (%)',
                     title='Mean RTP: With vs Without Bonus Features')
        fig.update_traces(texttemplate='%{text:.3f}%', textposition='outside')
        fig.update_coloraxes(showscale=False)
        render_chart(fig, height=330)
    with col2:
        st.dataframe(bonus_compare, width='stretch', hide_index=True)
        st.caption(
            'The difference is < 0.1 pp. Bonus features are marketing tools, '
            'not genuine RTP improvements.'
        )

    # ── RTP vs Max Multiplier scatter ─────────────────────────────────────────
    st.markdown('## RTP vs Max Multiplier — The Risk-Reward Trade-off')
    sdf = df[df['max_multiplier'] <= df['max_multiplier'].quantile(0.99)].sample(
        min(5000, len(df)), random_state=42)
    fig = px.scatter(sdf, x='rtp', y='max_multiplier',
                     color='volatility',
                     category_orders={'volatility': VOL_ORDER},
                     color_discrete_sequence=PALETTE,
                     opacity=0.55,
                     labels={'rtp': 'RTP (%)', 'max_multiplier': 'Max Multiplier (x)',
                             'volatility': 'Volatility'},
                     title='RTP vs Max Multiplier (sample 5,000, coloured by volatility)',
                     trendline='ols')
    render_chart(fig, height=400)
    st.caption(
        'High-volatility games offer bigger multipliers but similar RTP — '
        'you can win big occasionally, the house edge stays the same.'
    )

    # ── Best / worst providers ────────────────────────────────────────────────
    st.markdown('## Provider Analysis — Who Favours the House Most?')
    prov_he = (df.groupby('provider', observed=True)['house_edge']
                 .agg(['mean', 'count']).reset_index()
                 .rename(columns={'mean': 'Avg House Edge', 'count': 'Games'})
                 .query('Games >= 20')
                 .sort_values('Avg House Edge', ascending=False))

    col1, col2 = st.columns(2)
    with col1:
        top10_worst = prov_he.head(10).round(3)
        fig = px.bar(top10_worst, x='Avg House Edge', y='provider', orientation='h',
                     color='Avg House Edge', color_continuous_scale='Reds',
                     labels={'provider': 'Provider', 'Avg House Edge': 'Avg House Edge (%)'},
                     title='Highest House Edge Providers (≥20 games)')
        fig.update_coloraxes(showscale=False)
        theme(fig).update_layout(yaxis=dict(autorange='reversed'))
        render_chart(fig, height=360)
    with col2:
        top10_best = prov_he.tail(10).sort_values('Avg House Edge').round(3)
        fig = px.bar(top10_best, x='Avg House Edge', y='provider', orientation='h',
                     color='Avg House Edge', color_continuous_scale='Greens',
                     labels={'provider': 'Provider', 'Avg House Edge': 'Avg House Edge (%)'},
                     title='Lowest House Edge Providers (most player-friendly)')
        fig.update_coloraxes(showscale=False)
        theme(fig).update_layout(yaxis=dict(autorange='reversed'))
        render_chart(fig, height=360)

    # ── Correlation heatmap ───────────────────────────────────────────────────
    st.markdown('## Correlation Matrix — Numeric Variables')
    num_cols = ['rtp', 'house_edge', 'min_bet', 'max_win', 'max_multiplier', 'release_year']
    corr = df[num_cols].corr().round(3)
    fig = px.imshow(corr, text_auto=True,
                    color_continuous_scale='RdBu', zmin=-1, zmax=1,
                    title='Correlation Matrix of Key Numeric Variables',
                    aspect='auto')
    render_chart(fig, height=400)
    st.caption(
        '`rtp` and `house_edge` are perfectly negatively correlated (−1.0) by definition. '
        '`max_multiplier` shows weak correlation with RTP, confirming large potential '
        'wins do not improve long-run player odds.'
    )

    # ── House edge trend over years ───────────────────────────────────────────
    st.markdown('## Has the House Edge Changed Over Time?')
    trend = (df[df['release_year'] >= 2010]
             .groupby('release_year', observed=True)['house_edge']
             .agg(['mean', 'median', 'std']).reset_index())
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trend['release_year'], y=trend['mean'],
        mode='lines+markers', name='Mean House Edge',
        line=dict(color=COLORS['red'], width=2.5)))
    fig.add_trace(go.Scatter(
        x=trend['release_year'], y=trend['median'],
        mode='lines+markers', name='Median House Edge',
        line=dict(color=COLORS['primary'], width=2, dash='dash')))
    fig.add_trace(go.Scatter(
        x=trend['release_year'], y=trend['mean'] + trend['std'],
        mode='lines', showlegend=False,
        line=dict(color=COLORS['red'], width=0)))
    fig.add_trace(go.Scatter(
        x=trend['release_year'], y=trend['mean'] - trend['std'],
        mode='lines', name='±1 Std Dev', fill='tonexty',
        fillcolor='rgba(248,81,73,0.15)',
        line=dict(color=COLORS['red'], width=0)))
    theme(fig).update_layout(
        title='House Edge Trend by Release Year',
        xaxis_title='Release Year', yaxis_title='House Edge (%)')
    render_chart(fig, height=400)
