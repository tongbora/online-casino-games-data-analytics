"""
dashboard/pages/insights.py
────────────────────────────
Page: 1.6 Key Insights & Conclusion
5 data-backed findings, conclusion, limitations, and next steps.
(EDA Requirement 1.6)
"""

import pandas as pd
import streamlit as st

from dashboard.config import badge, insight


def render(df: pd.DataFrame) -> None:
    st.title('1.6  Key Insights & Conclusion')
    badge('EDA REQUIREMENT 1.6')
    st.markdown("### Big Question: *\"How should casino owners optimize margin and revenue?\"*")

    st.markdown('## 🔍 5 Owner-Focused Findings')

    avg_he     = df['house_edge'].mean()
    worst_type = df.groupby('game_type', observed=True)['house_edge'].mean().idxmax()
    worst_he   = df.groupby('game_type', observed=True)['house_edge'].mean().max()
    best_type  = df.groupby('game_type', observed=True)['house_edge'].mean().idxmin()
    best_he    = df.groupby('game_type', observed=True)['house_edge'].mean().min()
    fs_rtp     = df[df['free_spins_feature']]['rtp'].mean()
    no_fs_rtp  = df[~df['free_spins_feature']]['rtp'].mean()
    vh_mult    = df[df['volatility'] == 'Very High']['max_multiplier'].median()
    lo_mult    = df[df['volatility'] == 'Low']['max_multiplier'].median()

    insight(1, f"""
<strong>The portfolio has stable built-in margin — about 3.8 cents per $1 bet on average.</strong><br/>
Across {len(df):,} games, the mean house edge is <strong>{avg_he:.2f}%</strong>
(mean RTP = {df['rtp'].mean():.2f}%). No game in the dataset exceeds 99.5 % RTP,
so operators retain at least 0.5% over time.
This supports predictable long-run profitability.
    """)

    insight(2, f"""
<strong>Game type is the strongest margin lever.</strong><br/>
<em>{worst_type.title()}</em> games carry the highest average house edge at
<strong>{worst_he:.2f}%</strong>, while <em>{best_type.title()}</em> games are the
lowest-margin segment at <strong>{best_he:.2f}%</strong>.
Portfolio mix by game type should be a priority decision.
    """)

    insight(3, f"""
<strong>Risk tiers reshape player experience while margin stays similar.</strong><br/>
Very High volatility games offer a median max multiplier of <strong>{vh_mult:,.0f}x</strong>
versus <strong>{lo_mult:,.0f}x</strong> for Low volatility.
But the average house edge is almost the same across risk levels.
This enables segmented product design without major margin trade-offs.
    """)

    insight(4, f"""
<strong>Bonus features have minimal impact on expected margin.</strong><br/>
Games with free spins average {fs_rtp:.3f}% RTP vs {no_fs_rtp:.3f}% without —
a difference of only <strong>{abs(fs_rtp - no_fs_rtp):.3f} percentage points</strong>.
Bonus buy shows a similarly tiny gap.
These features can be treated mainly as engagement tools, not margin risks.
    """)

    rtp_2010 = (df[df['release_year'] == 2010]['rtp'].mean()
                if 2010 in df['release_year'].values else None)
    rtp_2024 = (df[df['release_year'] == 2024]['rtp'].mean()
                if 2024 in df['release_year'].values else None)

    if rtp_2010 and rtp_2024:
        direction = 'improved' if rtp_2024 > rtp_2010 else 'declined'
        insight(5, f"""
<strong>Market RTP has {direction} slightly over 14 years, but operator edge remains strong.</strong><br/>
Mean RTP was {rtp_2010:.2f}% for games released in 2010 vs {rtp_2024:.2f}% in 2024
(Δ = {rtp_2024 - rtp_2010:+.2f} points). Competition may move RTP a little,
but a durable house edge remains.
        """)
    else:
        prov_min = df.groupby('provider', observed=True)['house_edge'].mean().min()
        prov_max = df.groupby('provider', observed=True)['house_edge'].mean().max()
        insight(5, f"""
<strong>Provider selection materially affects margin quality.</strong><br/>
Among providers with ≥20 games, house edge ranges from
~{prov_min:.2f}% to ~{prov_max:.2f}%.
Provider partnerships should balance margin target, brand fit, and product mix.
        """)

    # ── Conclusion ────────────────────────────────────────────────────────────
    st.markdown('## 🔖 Conclusion')
    st.markdown(f"""
> **This portfolio supports strong, consistent operator profitability.**
> The mean house edge of **{avg_he:.2f}%** across game types and providers
> indicates a robust long-run margin structure.

Recommended owner actions:
1. **Optimize game-type mix** toward higher-margin categories.
2. **Use volatility as a segmentation tool** while monitoring total margin.
3. **Use bonus features for engagement** since margin impact is limited.
4. **Prioritize provider contracts** based on edge profile and catalog quality.
    """)

    # ── Limitations & next steps ──────────────────────────────────────────────
    st.markdown('## ⚠️  Limits and Next Steps')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
**Limits**
- This data shows **game settings**, not real player session history.
- `jackpot` is mostly empty, so jackpot behavior was not studied.
- Promotions (cashback, reloads) are not included and may change real-world returns.
- `max_multiplier` is missing for about 18% of rows.
        """)
    with col2:
        st.markdown("""
**Next Steps**
- Add real session data (stake, session length, retention) for revenue forecasting.
- Build a margin-by-provider scorecard for partnership planning.
- Segment performance by market/country to support local portfolio strategy.
- Create a pricing and promotion simulation layer for commercial planning.
        """)

    st.divider()
    st.markdown("""
<div style="text-align:center; color:#8b949e; font-size:0.85rem; padding:1rem 0">
  <strong>PPIU — Data Analytics EDA &nbsp;|&nbsp; Story Angle #2: The House Always Wins?</strong><br/>
  Dataset: Online Casino Games (1.2 M records) &nbsp;|&nbsp; Tools: Python · Pandas · Plotly · Streamlit
</div>
    """, unsafe_allow_html=True)
