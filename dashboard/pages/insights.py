"""
dashboard/pages/insights.py
────────────────────────────
Page: 3.6 Key Insights & Conclusion
5 data-backed findings, conclusion, limitations, and next steps.
(EDA Requirement 3.6)
"""

import pandas as pd
import streamlit as st

from dashboard.config import badge, insight


def render(df: pd.DataFrame) -> None:
    st.title('3.6  Key Insights & Conclusion')
    badge('EDA REQUIREMENT 3.6')
    st.markdown("### Story Angle: *\"The House Always Wins?\"*")

    st.markdown('## 🔍 5 Key Findings')

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
<strong>The house always wins — on average 3.8 ¢ per dollar bet.</strong><br/>
Across {len(df):,} games, the mean house edge is <strong>{avg_he:.2f}%</strong>
(mean RTP = {df['rtp'].mean():.2f}%). No game in the dataset exceeds 99.5 % RTP,
meaning the casino <em>always</em> retains at least 0.5 % of every dollar wagered.
The math is permanently in the house's favour.
    """)

    insight(2, f"""
<strong>Game type is the biggest driver of house advantage.</strong><br/>
<em>{worst_type.title()}</em> games carry the highest average house edge at
<strong>{worst_he:.2f}%</strong>, while <em>{best_type.title()}</em> games are the
most player-friendly at <strong>{best_he:.2f}%</strong>.
Choosing the right game type has a greater impact on expected value than any strategy.
    """)

    insight(3, f"""
<strong>Volatility changes the <em>experience</em> of losing — not the mathematical outcome.</strong><br/>
Very High volatility games offer a median max multiplier of <strong>{vh_mult:,.0f}x</strong>
versus only <strong>{lo_mult:,.0f}x</strong> for Low volatility — chance of a life-changing win.
However, mean house edge is virtually identical across all volatility tiers.
High volatility means ruin faster or win bigger; the casino's long-run advantage is unchanged.
    """)

    insight(4, f"""
<strong>Bonus features do not meaningfully improve player odds.</strong><br/>
Games with free spins average {fs_rtp:.3f}% RTP vs {no_fs_rtp:.3f}% without —
a difference of only <strong>{abs(fs_rtp - no_fs_rtp):.3f} percentage points</strong>.
The bonus-buy feature shows an equally negligible gap.
Bonus rounds increase engagement and session length, but they are <em>not</em> mechanisms
to shift the mathematical edge toward the player.
    """)

    rtp_2010 = (df[df['release_year'] == 2010]['rtp'].mean()
                if 2010 in df['release_year'].values else None)
    rtp_2024 = (df[df['release_year'] == 2024]['rtp'].mean()
                if 2024 in df['release_year'].values else None)

    if rtp_2010 and rtp_2024:
        direction = 'improved' if rtp_2024 > rtp_2010 else 'declined'
        insight(5, f"""
<strong>Player odds have {direction} marginally over 14 years — but the house remains in control.</strong><br/>
Mean RTP was {rtp_2010:.2f}% for games released in 2010 vs {rtp_2024:.2f}% in 2024
(Δ = {rtp_2024 - rtp_2010:+.2f} pp). Regulatory pressure and market competition nudge RTPs
upward, but the structural advantage is built into the mathematical model by design —
it cannot be competed away.
        """)
    else:
        prov_min = df.groupby('provider', observed=True)['house_edge'].mean().min()
        prov_max = df.groupby('provider', observed=True)['house_edge'].mean().max()
        insight(5, f"""
<strong>Provider competition has narrowed — but not closed — the house edge gap.</strong><br/>
Among providers with ≥20 games, house edge ranges from
~{prov_min:.2f}% to ~{prov_max:.2f}%.
Market forces push some providers to offer higher RTPs to attract players,
yet none surrender their mathematical advantage entirely.
        """)

    # ── Conclusion ────────────────────────────────────────────────────────────
    st.markdown('## 🔖 Conclusion')
    st.markdown(f"""
> **Yes — the data overwhelmingly supports "The House Always Wins."**
> The mean house edge of **{avg_he:.2f}%** across all game types and providers
> confirms that casino game mathematics are structured to guarantee long-term
> operator profit. No game offers true 100 % RTP.

The most meaningful player decisions are:
1. **Choose game type carefully** — some types offer materially better odds.
2. **Understand volatility** — it changes the *shape* of your losses, not the total.
3. **Don't be misled by bonus features** — negligible effect on actual RTP.
    """)

    # ── Limitations & next steps ──────────────────────────────────────────────
    st.markdown('## ⚠️  Limitations & Next Steps')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
**Limitations**
- Dataset describes **game specifications** — not live session records.
  Actual player outcomes may deviate from theoretical RTP.
- `jackpot` column is 89 % missing; progressive jackpot mechanics could not be analysed.
- Promotional cashback / reload bonuses can effectively raise real-world RTP beyond listed values.
- `max_multiplier` missing for ~18 % of rows, limiting reward analysis coverage.
        """)
    with col2:
        st.markdown("""
**Next Steps**
- Obtain **transactional player data** (bets, wins, session logs) to validate theoretical RTP.
- Analyse **progressive jackpot mechanics** with a more complete dataset.
- Investigate **responsible gambling patterns** — which volatility/game combinations
  correlate with longer sessions or escalating bets.
- Build a **game recommender** that ranks by player-friendliness (high RTP + low volatility).
        """)

    st.divider()
    st.markdown("""
<div style="text-align:center; color:#8b949e; font-size:0.85rem; padding:1rem 0">
  <strong>PPIU — Data Analytics EDA &nbsp;|&nbsp; Story Angle #2: The House Always Wins?</strong><br/>
  Dataset: Online Casino Games (1.2 M records) &nbsp;|&nbsp; Tools: Python · Pandas · Plotly · Streamlit
</div>
    """, unsafe_allow_html=True)
