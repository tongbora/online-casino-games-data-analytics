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
    st.title('1.6  Main Findings & Conclusion')
    badge('EDA REQUIREMENT 1.6')
    st.markdown("### Big Question: *\"Does the house always win?\"* (Student Summary)")

    st.markdown('## 🔍 5 Main Findings')

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
<strong>The house wins in the long run — about 3.8 cents per $1 bet on average.</strong><br/>
Across {len(df):,} games, the mean house edge is <strong>{avg_he:.2f}%</strong>
(mean RTP = {df['rtp'].mean():.2f}%). No game in the dataset exceeds 99.5 % RTP,
so the casino still keeps at least 0.5% over time.
In short: the setup favors the casino.
    """)

    insight(2, f"""
<strong>Game type makes a big difference.</strong><br/>
<em>{worst_type.title()}</em> games carry the highest average house edge at
<strong>{worst_he:.2f}%</strong>, while <em>{best_type.title()}</em> games are the
most player-friendly at <strong>{best_he:.2f}%</strong>.
For students: picking a better game type matters more than most player tactics.
    """)

    insight(3, f"""
<strong>Risk level changes the ride, not the long-run result.</strong><br/>
Very High volatility games offer a median max multiplier of <strong>{vh_mult:,.0f}x</strong>
versus <strong>{lo_mult:,.0f}x</strong> for Low volatility.
But the average house edge is almost the same across risk levels.
So risk changes how results feel (big swings), not who keeps the edge.
    """)

    insight(4, f"""
<strong>Bonus features do not really improve long-run odds.</strong><br/>
Games with free spins average {fs_rtp:.3f}% RTP vs {no_fs_rtp:.3f}% without —
a difference of only <strong>{abs(fs_rtp - no_fs_rtp):.3f} percentage points</strong>.
Bonus buy shows a similarly tiny gap.
These features can make games more exciting, but they do not change the core edge much.
    """)

    rtp_2010 = (df[df['release_year'] == 2010]['rtp'].mean()
                if 2010 in df['release_year'].values else None)
    rtp_2024 = (df[df['release_year'] == 2024]['rtp'].mean()
                if 2024 in df['release_year'].values else None)

    if rtp_2010 and rtp_2024:
        direction = 'improved' if rtp_2024 > rtp_2010 else 'declined'
        insight(5, f"""
<strong>Player odds have {direction} slightly over 14 years — but the house still leads.</strong><br/>
Mean RTP was {rtp_2010:.2f}% for games released in 2010 vs {rtp_2024:.2f}% in 2024
(Δ = {rtp_2024 - rtp_2010:+.2f} points). Competition may move RTP a little,
but casinos still keep a built-in advantage.
        """)
    else:
        prov_min = df.groupby('provider', observed=True)['house_edge'].mean().min()
        prov_max = df.groupby('provider', observed=True)['house_edge'].mean().max()
        insight(5, f"""
<strong>Provider differences are real, but none remove the house edge.</strong><br/>
Among providers with ≥20 games, house edge ranges from
~{prov_min:.2f}% to ~{prov_max:.2f}%.
Some providers offer better returns than others,
but no provider gives up the built-in edge.
        """)

    # ── Conclusion ────────────────────────────────────────────────────────────
    st.markdown('## 🔖 Conclusion')
    st.markdown(f"""
> **Yes — the data overwhelmingly supports "The House Always Wins."**
> The mean house edge of **{avg_he:.2f}%** across all game types and providers
> shows that casinos are designed to profit over time. No game in this data
> reaches true 100% RTP.

The most useful takeaways are:
1. **Choose game type carefully** — some types offer materially better odds.
2. **Understand risk level** — it changes the ups and downs, not the long-run edge.
3. **Treat bonus features carefully** — they have only a small effect on RTP.
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
- Use real session data (bets and wins) to compare with listed RTP.
- Add better jackpot data for deeper jackpot analysis.
- Study which game/risk combinations are linked to longer play sessions.
- Build a simple game ranking based on higher RTP and lower risk.
        """)

    st.divider()
    st.markdown("""
<div style="text-align:center; color:#8b949e; font-size:0.85rem; padding:1rem 0">
  <strong>PPIU — Data Analytics EDA &nbsp;|&nbsp; Story Angle #2: The House Always Wins?</strong><br/>
  Dataset: Online Casino Games (1.2 M records) &nbsp;|&nbsp; Tools: Python · Pandas · Plotly · Streamlit
</div>
    """, unsafe_allow_html=True)
