"""
dashboard/pages/visualisations.py
───────────────────────────────────
Page: 1.5 Key Visualisations Summary
All charts from the analysis consolidated into one tabbed view.
(EDA Requirement 1.5)
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.config import COLORS, PALETTE, VOL_ORDER, badge, render_chart, theme


def render(df: pd.DataFrame) -> None:
    st.title('1.5  All Charts in One Place')
    badge('EDA REQUIREMENT 1.5')
    st.markdown('*A quick, student-friendly chart summary of the main findings.*')

    tab1, tab2, tab3, tab4 = st.tabs(
        ['🏦 House Edge', '🎲 Risk Levels', '🎮 Game Types', '💰 Win Potential']
    )

    # ── Tab 1: House Edge ─────────────────────────────────────────────────────
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(df, x='house_edge', nbins=50,
                               color_discrete_sequence=[COLORS['red']],
                               labels={'house_edge': 'House Edge (%)'},
                               title='House Edge Distribution')
            fig.add_vline(x=df['house_edge'].mean(), line_dash='dash',
                          line_color=COLORS['primary'],
                          annotation_text=f"Mean: {df['house_edge'].mean():.2f}%")
            render_chart(fig, height=300)
        with col2:
            he_gt = (df.groupby('game_type', observed=True)['house_edge']
                       .mean().round(3).sort_values(ascending=False).reset_index())
            he_gt.columns = ['Game Type', 'Avg House Edge (%)']
            fig = px.bar(he_gt, x='Game Type', y='Avg House Edge (%)',
                         color='Avg House Edge (%)', color_continuous_scale='Reds',
                         text='Avg House Edge (%)',
                         title='Average House Edge by Game Type')
            fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
            fig.update_coloraxes(showscale=False)
            render_chart(fig, height=300)

        he_gt = (df.groupby('game_type', observed=True)['house_edge']
               .mean().round(3).sort_values(ascending=True).reset_index())
        he_gt.columns = ['Game Type', 'Avg House Edge (%)']
        fig = px.bar(he_gt, x='Avg House Edge (%)', y='Game Type', orientation='h',
                 color='Avg House Edge (%)', color_continuous_scale='Reds',
                 text='Avg House Edge (%)',
                 title='Average House Edge by Game Type',
                 labels={'Avg House Edge (%)': 'Average House Edge (%)',
                     'Game Type': 'Game Type'})
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig.update_coloraxes(showscale=False)
        fig.update_layout(yaxis=dict(autorange='reversed'))
        render_chart(fig, height=350)

    # ── Tab 2: Volatility & Risk ──────────────────────────────────────────────
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            he_vol = (df.groupby('volatility', observed=True)['house_edge'].mean()
                        .reindex(VOL_ORDER).reset_index())
            he_vol.columns = ['Volatility', 'Mean House Edge (%)']
            fig = px.bar(he_vol, x='Volatility', y='Mean House Edge (%)',
                         color='Mean House Edge (%)', color_continuous_scale='Reds',
                         text='Mean House Edge (%)',
                         title='Average House Edge by Risk Level')
            fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
            fig.update_coloraxes(showscale=False)
            render_chart(fig, height=320)
        with col2:
            he_vol_gt = (df.groupby(['volatility', 'game_type'], observed=True)['house_edge']
                           .mean().reset_index())
            pivot_table = he_vol_gt.pivot(index='game_type', columns='volatility', values='house_edge').round(2)
            pivot_table = pivot_table[[c for c in VOL_ORDER if c in pivot_table.columns]]
            st.dataframe(pivot_table, use_container_width=True)
            st.caption('Average house edge for each game type and risk level (easy comparison table)')

        he_mm = df.groupby('volatility', observed=True)['max_multiplier'].mean().reindex(VOL_ORDER).reset_index()
        he_mm.columns = ['Volatility', 'Mean Max Multiplier']
        fig = px.bar(he_mm, x='Volatility', y='Mean Max Multiplier',
                     color_discrete_sequence=[COLORS['purple']],
                     text='Mean Max Multiplier',
                     title='Average Max Multiplier by Risk Level')
        fig.update_traces(texttemplate='%{text:.0f}x', textposition='outside')
        render_chart(fig, height=360)

    # ── Tab 3: Game Types ─────────────────────────────────────────────────────
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            gt_cnt = df['game_type'].value_counts().reset_index()
            gt_cnt.columns = ['Game Type', 'Count']
            fig = px.pie(gt_cnt, names='Game Type', values='Count',
                         color_discrete_sequence=PALETTE, hole=0.45,
                         title='Game Type Share')
            fig.update_traces(textinfo='label+percent')
            render_chart(fig, height=320)
        with col2:
            gc_cnt = df['game_category'].value_counts().head(15).reset_index()
            gc_cnt.columns = ['Category', 'Count']
            fig = px.bar(gc_cnt, x='Category', y='Count',
                         color='Count', color_continuous_scale='Blues',
                         text='Count',
                         title='Top 15 Game Categories by Count')
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            fig.update_coloraxes(showscale=False)
            render_chart(fig, height=320)

        cat_he = (df.groupby('game_category', observed=True)['house_edge']
                    .agg(['mean', 'count']).reset_index()
                    .query('count >= 100')
                    .sort_values('mean', ascending=False).head(15))
        cat_he.columns = ['Category', 'Avg HE%', 'Count']
        fig = px.bar(cat_he, x='Category', y='Avg HE%',
                     color='Avg HE%', color_continuous_scale='Reds',
                     text='Avg HE%',
                     title='Top 15 Categories by Average House Edge (≥100 games)')
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig.update_coloraxes(showscale=False)
        render_chart(fig, height=360)

    # ── Tab 4: Win Potential ──────────────────────────────────────────────────
    with tab4:
        col1, col2 = st.columns(2)
        with col1:
            wbr_cap = df['win_to_bet_ratio'].quantile(0.97)
            fig = px.histogram(df[df['win_to_bet_ratio'] <= wbr_cap],
                               x='win_to_bet_ratio', nbins=50,
                               color_discrete_sequence=[COLORS['green']],
                               labels={'win_to_bet_ratio': 'Win-to-Bet Ratio (x)'},
                               title='Win-to-Bet Ratio Distribution (very large outliers trimmed for clarity)')
            render_chart(fig, height=300)
        with col2:
            wbr_vol = (df.groupby('volatility', observed=True)['win_to_bet_ratio']
                         .median().reset_index())
            wbr_vol.columns = ['Volatility', 'Median Win-to-Bet Ratio']
            fig = px.bar(wbr_vol, x='Volatility', y='Median Win-to-Bet Ratio',
                         color='Median Win-to-Bet Ratio', color_continuous_scale='Greens',
                         category_orders={'Volatility': VOL_ORDER},
                         title='Median Win-to-Bet Ratio by Risk Level')
            fig.update_coloraxes(showscale=False)
            render_chart(fig, height=300)

        bonus_rtp = pd.DataFrame({
            'Condition': ['No Free Spins', 'Has Free Spins', 'No Bonus Buy', 'Has Bonus Buy'],
            'Mean RTP (%)': [
                df[~df['free_spins_feature']]['rtp'].mean(),
                df[df['free_spins_feature']]['rtp'].mean(),
                df[~df['bonus_buy_available']]['rtp'].mean(),
                df[df['bonus_buy_available']]['rtp'].mean(),
            ],
        }).round(3)
        fig = px.bar(bonus_rtp, x='Condition', y='Mean RTP (%)',
                     color='Mean RTP (%)', color_continuous_scale='RdYlGn',
                     range_color=[95.5, 97], text='Mean RTP (%)',
                     title='Bonus Features vs Average RTP')
        fig.update_traces(texttemplate='%{text:.3f}%', textposition='outside')
        fig.update_coloraxes(showscale=False)
        render_chart(fig, height=320)
