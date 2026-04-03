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
    st.title('1.5  Key Visualisations Summary')
    badge('EDA REQUIREMENT 1.5')
    st.markdown('*All key charts in one place — clear, labelled, and tied to the story.*')

    tab1, tab2, tab3, tab4 = st.tabs(
        ['🏦 House Edge', '🎲 Volatility & Risk', '🎮 Game Types', '💰 Win Potential']
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
                         title='Avg House Edge by Game Type')
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
            fig = px.violin(df, x='volatility', y='house_edge',
                            color='volatility', box=True,
                            category_orders={'volatility': VOL_ORDER},
                            color_discrete_sequence=PALETTE,
                            title='House Edge by Volatility',
                            labels={'house_edge': 'House Edge (%)'})
            render_chart(fig, height=320)
        with col2:
            fig = px.density_heatmap(df, x='volatility', y='game_type',
                                     z='house_edge', histfunc='avg',
                                     color_continuous_scale='YlOrRd',
                                     category_orders={'volatility': VOL_ORDER},
                                     title='Avg House Edge: Volatility × Game Type',
                                     labels={'house_edge': 'Avg House Edge (%)'})
            render_chart(fig, height=320)

        sdf = df[df['max_multiplier'] <= df['max_multiplier'].quantile(0.98)].sample(
            min(3000, len(df)), random_state=42)
        fig = px.scatter(sdf, x='house_edge', y='max_multiplier',
                         color='volatility', opacity=0.5,
                         category_orders={'volatility': VOL_ORDER},
                         color_discrete_sequence=PALETTE,
                         labels={'house_edge': 'House Edge (%)',
                                 'max_multiplier': 'Max Multiplier (x)'},
                         title='House Edge vs Max Multiplier (coloured by volatility)')
        render_chart(fig, height=360)

    # ── Tab 3: Game Types ─────────────────────────────────────────────────────
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            gt_cnt = df['game_type'].value_counts().reset_index()
            gt_cnt.columns = ['Game Type', 'Count']
            fig = px.pie(gt_cnt, names='Game Type', values='Count',
                         color_discrete_sequence=PALETTE, hole=0.45,
                         title='Game Type Share of Library')
            fig.update_traces(textinfo='label+percent')
            render_chart(fig, height=320)
        with col2:
            fig = px.treemap(df, path=['game_type', 'game_category'],
                             title='Game Category Hierarchy (Treemap)',
                             color_discrete_sequence=PALETTE)
            render_chart(fig, height=320)

        cat_he = (df.groupby('game_category', observed=True)['house_edge']
                    .agg(['mean', 'count']).reset_index()
                    .query('count >= 100')
                    .sort_values('mean', ascending=False).head(15))
        cat_he.columns = ['Category', 'Avg HE%', 'Count']
        fig = px.bar(cat_he, x='Category', y='Avg HE%',
                     color='Avg HE%', color_continuous_scale='Reds',
                     text='Avg HE%',
                     title='Top 15 Categories by Avg House Edge (≥100 games)')
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
                               title='Win-to-Bet Ratio Distribution (97th pct cap)')
            render_chart(fig, height=300)
        with col2:
            wbr_vol = (df.groupby('volatility', observed=True)['win_to_bet_ratio']
                         .median().reset_index())
            wbr_vol.columns = ['Volatility', 'Median Win-to-Bet Ratio']
            fig = px.bar(wbr_vol, x='Volatility', y='Median Win-to-Bet Ratio',
                         color='Median Win-to-Bet Ratio', color_continuous_scale='Greens',
                         category_orders={'Volatility': VOL_ORDER},
                         title='Median Win-to-Bet Ratio by Volatility')
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
                     title='Impact of Bonus Features on Mean RTP')
        fig.update_traces(texttemplate='%{text:.3f}%', textposition='outside')
        fig.update_coloraxes(showscale=False)
        render_chart(fig, height=320)
