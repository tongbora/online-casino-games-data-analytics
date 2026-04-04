"""
dashboard/pages/insights.py
────────────────────────────
Page: 1.6 Key Insights & Conclusion
5 data-backed findings, conclusion, limitations, and next steps.
(EDA Requirement 1.6)
"""

import pandas as pd
import streamlit as st
import textwrap

from dashboard.config import badge


def render(df: pd.DataFrame) -> None:
    st.title('1.6  Key Insights & Conclusion')
    badge('EDA REQUIREMENT 1.6')

    avg_he = df['house_edge'].mean()
    fs_he = df[df['free_spins_feature']]['house_edge'].mean()
    no_fs_he = df[~df['free_spins_feature']]['house_edge'].mean()
    fs_he_gap = fs_he - no_fs_he

    game_type_he = df.groupby('game_type', observed=True)['house_edge'].mean().sort_values(ascending=False)
    top_type = game_type_he.index[0].title()
    top_type_he = game_type_he.iloc[0]
    low_type = game_type_he.index[-1].title()
    low_type_he = game_type_he.iloc[-1]
    top_vs_low_gap = ((top_type_he - low_type_he) / low_type_he * 100) if low_type_he else 0.0

    provider_he = df.groupby('provider', observed=True)['house_edge'].agg(['mean', 'count'])
    provider_he = provider_he[provider_he['count'] >= 20]['mean'].sort_values(ascending=False)
    if len(provider_he) >= 2:
        top_provider = provider_he.index[0]
        top_provider_he = provider_he.iloc[0]
        low_provider = provider_he.index[-1]
        low_provider_he = provider_he.iloc[-1]
    else:
        top_provider = 'Top Provider'
        low_provider = 'Lower Provider'
        top_provider_he = avg_he
        low_provider_he = avg_he

    def card_html(index: str, title: str, body: str) -> str:
        return textwrap.dedent(
            f"""
            <div style="display:grid; grid-template-columns:64px 1fr; gap:0.55rem; min-height:84px; background:var(--card-bg); border:1px solid var(--card-border); margin-bottom:0.5rem;">
              <div style="display:flex; align-items:center; justify-content:center; background:color-mix(in srgb, var(--secondary-background-color) 30%, var(--text-color) 70%); color:var(--primary-color); font-weight:800; font-size:1.4rem; letter-spacing:0.02em;">{index}</div>
              <div style="padding:0.5rem 0.62rem;">
                <p style="margin:0; font-size:1.05rem; font-weight:800; color:var(--h2); line-height:1.25;">{title}</p>
                <p style="margin:0.22rem 0 0 0; color:var(--muted-text); font-size:0.97rem; line-height:1.28;">{body}</p>
              </div>
            </div>
            """
        ).strip()

    st.markdown(
        textwrap.dedent(
            """
            <div style="border-left:6px solid color-mix(in srgb, var(--primary-color) 35%, var(--text-color) 65%); border-top:6px solid color-mix(in srgb, var(--primary-color) 35%, var(--text-color) 65%); border-bottom:6px solid color-mix(in srgb, var(--primary-color) 20%, var(--text-color) 80%); border-right:1px solid var(--card-border); background:color-mix(in srgb, var(--secondary-background-color) 94%, var(--background-color) 6%); padding:1rem 1rem 0.95rem 1rem;">
                            <p style="margin:0; font-size:1.15rem; color:var(--muted-text);">What the data tells casino owners about maximising profit</p>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )

    st.markdown(
        card_html(
            '01',
            'The house edge is a guaranteed revenue stream',
            f'At <strong>{avg_he:.2f}%</strong> average edge, every $100 wagered generates about <strong>${avg_he:.2f}</strong> in expected profit regardless of individual game outcomes.',
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        card_html(
            '02',
            'Game selection directly determines profit margin',
            f'Highest-edge type <strong>{top_type}</strong> averages <strong>{top_type_he:.2f}%</strong> vs <strong>{low_type}</strong> at <strong>{low_type_he:.2f}%</strong>. Prioritising stronger categories can lift edge by about <strong>{top_vs_low_gap:.0f}%</strong>.',
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        card_html(
            '03',
            'Bonus features are a profit multiplier, not a cost',
            f'Games with Free Spins and Bonus Buy features show roughly <strong>{fs_he_gap:.1f}%</strong> higher house edge, while still supporting player engagement.',
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        card_html(
            '04',
            'Provider selection controls baseline profitability',
            f'<strong>{top_provider}</strong> averages <strong>{top_provider_he:.2f}%</strong> house edge vs <strong>{low_provider}</strong> at <strong>{low_provider_he:.2f}%</strong>. Selecting stronger provider mixes compounds annual revenue gains.',
        ),
        unsafe_allow_html=True,
    )
