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

try:
    import statsmodels.api as sm  # noqa: F401
    HAS_STATSMODELS = True
except Exception:
    HAS_STATSMODELS = False

from dashboard.config import COLORS, PALETTE, VOL_ORDER, badge, render_chart, theme


def render(df: pd.DataFrame) -> None:
    st.title('1.4  Bivariate & Multivariate')
    badge('EDA REQUIREMENT 1.4')
    st.markdown('*Compare values side by side to identify commercial drivers.*')

    # ── House edge by game type ───────────────────────────────────────────────
    st.markdown('## House Edge by Game Type')
    st.markdown('**Question:** Which game types deliver higher margin?')
    col1, col2 = st.columns([2, 1])
    with col1:
        he_summary = (df.groupby('game_type', observed=True)['house_edge']
                        .agg(['mean', 'median', 'min', 'max'])
                        .round(3).reset_index())
        he_summary.columns = ['Game Type', 'Mean HE%', 'Median HE%', 'Min', 'Max']
        he_summary = he_summary.sort_values('Mean HE%', ascending=False)
        fig = px.bar(he_summary, x='Game Type', y='Mean HE%',
                     color='Mean HE%', color_continuous_scale='Reds',
                     text='Mean HE%',
                     labels={'Game Type': 'Game Type', 'Mean HE%': 'Mean House Edge (%)'},
                     title='Mean House Edge by Game Type')
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig.update_coloraxes(showscale=False)
        render_chart(fig, height=380)
    with col2:
        he_by_type = (df.groupby('game_type', observed=True)['house_edge']
                        .agg(['mean', 'median', 'std'])
                        .round(3).reset_index())
        he_by_type.columns = ['Game Type', 'Mean HE%', 'Median HE%', 'Std']
        he_by_type = he_by_type.sort_values('Mean HE%', ascending=False)
        st.dataframe(he_by_type, width='stretch', hide_index=True)
        st.caption('Higher house edge means higher expected gross margin per $1 bet.')

    # ── RTP by volatility ─────────────────────────────────────────────────────
    st.markdown('## RTP by Risk Level')
    st.markdown('**Question:** Do risk tiers materially change margin?')
    col1, col2 = st.columns(2)
    with col1:
        rtp_mean = (df.groupby('volatility', observed=True)['rtp']
                      .mean().reindex(VOL_ORDER).reset_index())
        rtp_mean.columns = ['Volatility', 'Mean RTP%']
        fig = px.bar(rtp_mean, x='Volatility', y='Mean RTP%',
                     color='Mean RTP%', color_continuous_scale='Greens',
                     text='Mean RTP%',
                     labels={'Mean RTP%': 'Mean RTP (%)'},
                     title='Mean RTP by Volatility')
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig.update_coloraxes(showscale=False)
        render_chart(fig, height=350)
    with col2:
        rtp_vol = (df.groupby('volatility', observed=True)['rtp']
                     .agg(['mean', 'median', 'count'])
                     .round(3).reset_index())
        rtp_vol.columns = ['Volatility', 'Mean RTP%', 'Median RTP%', 'Count']
        st.dataframe(rtp_vol, width='stretch', hide_index=True)
        st.caption('RTP is similar across risk tiers, suggesting stable margin by volatility segment.')

    # ── Bonus features vs RTP ─────────────────────────────────────────────────
    st.markdown('## Bonus Features and Margin')
    st.markdown('**Question:** Do free spins or bonus buy reduce margin?')
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
            'The RTP difference is tiny (< 0.1 percentage points). Bonus features '
            'can support engagement without a major impact on expected margin.'
        )

    # ── RTP vs Max Multiplier scatter ─────────────────────────────────────────
    st.markdown('## RTP and Max Multiplier')
    st.markdown('**Question:** Do larger top-win promises require lower margin?')
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
                     trendline='ols' if HAS_STATSMODELS else None)
    render_chart(fig, height=400)
    if not HAS_STATSMODELS:
        st.caption('Trendline is off because `statsmodels` is not installed.')
    st.caption(
        'High-risk games advertise larger top wins, while RTP stays similar. '
        'This supports high-excitement positioning without giving up much margin.'
    )

    # ── Best / worst providers ────────────────────────────────────────────────
    st.markdown('## Provider Comparison')
    st.markdown('**Question:** Which providers are strongest for profitability?')
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
                     title='Lowest House Edge Providers (player-friendly benchmark)')
        fig.update_coloraxes(showscale=False)
        theme(fig).update_layout(yaxis=dict(autorange='reversed'))
        render_chart(fig, height=360)

    # ── Correlation heatmap ───────────────────────────────────────────────────
    st.markdown('## Which Numbers Move Together?')
    st.markdown('**Question:** Which values rise or fall together?')
    num_cols = ['rtp', 'house_edge', 'min_bet', 'max_win', 'max_multiplier', 'release_year']
    corr = df[num_cols].corr().round(3)
    fig = px.imshow(corr, text_auto=True,
                    color_continuous_scale='RdBu', zmin=-1, zmax=1,
                    title='How Key Numbers Move Together',
                    aspect='auto')
    render_chart(fig, height=400)
    st.caption(
        'RTP and house edge always move in opposite directions. '
        'Max multiplier has only a weak link with RTP, so bigger top wins do not '
        'automatically mean better long-run returns.'
    )

    # ── House edge trend over years ───────────────────────────────────────────
    st.markdown('## House Edge Over Time')
    st.markdown('**Question:** Are new releases improving or reducing operator margin?')
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
