"""
dashboard/config.py
───────────────────
Centralised CSS, colour tokens, Plotly theme helper,
and shared UI utility functions used across all pages.
"""

import streamlit as st

# ── Colour palette ────────────────────────────────────────────────────────────
COLORS = {
    'primary': '#f0e68c',
    'blue':    '#58a6ff',
    'green':   '#3fb950',
    'red':     '#f85149',
    'purple':  '#bc8cff',
    'orange':  '#ffa657',
}
PALETTE = ['#58a6ff', '#f0e68c', '#3fb950', '#f85149',
           '#bc8cff', '#ffa657', '#79c0ff', '#56d364']

VOL_ORDER = ['Low', 'Medium', 'High', 'Very High']

# ── Page sections (sidebar labels) ───────────────────────────────────────────
SECTIONS = [
    '  Introduction',
    '1.1  Data Understanding',
    '1.2  Data Cleaning',
    '1.3  Univariate Analysis',
    '1.4  Bivariate & Multivariate',
    '1.5  Visualisations Summary',
    '1.6  Key Insights & Conclusion',
]


# ── Streamlit page configuration ──────────────────────────────────────────────
def configure_page() -> None:
    """Call once at the top of app.py before any other st.* call."""
    st.set_page_config(
        page_title='The House Always Wins? | PPIU EDA',
        page_icon='🃏',
        layout='wide',
        initial_sidebar_state='expanded',
    )


# ── Global CSS ────────────────────────────────────────────────────────────────
def inject_css() -> None:
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0a1a 0%, #1a0a2e 50%, #0d1117 100%);
    border-right: 1px solid #2d2d5e;
}
[data-testid="stSidebar"] * { color: #c9d1d9 !important; }

div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0d1117, #161b22);
    border: 1px solid #30363d;
    border-radius: 10px; padding: 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}
div[data-testid="metric-container"] label {
    color: #8b949e !important; font-size: 0.78rem !important;
    letter-spacing: 0.05em; text-transform: uppercase;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e6edf3 !important; font-size: 1.85rem !important; font-weight: 700 !important;
}

.stApp { background: #0d1117; color: #c9d1d9; }
.block-container { padding-top: 1.5rem; max-width: 1400px; }
h1 { color: #f0e68c; font-weight: 800; }
h2 { color: #79c0ff; border-bottom: 1px solid #21262d; padding-bottom: 0.4rem; margin-top: 1.5rem; }
h3 { color: #a5d6ff; }

.insight-box {
    background: linear-gradient(135deg, #0f1923, #1c2333);
    border-left: 4px solid #f0e68c;
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.2rem; margin: 0.6rem 0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
}
.insight-box p { color: #c9d1d9; margin: 0; font-size: 0.95rem; line-height: 1.6; }
.insight-number { color: #f0e68c; font-weight: 700; font-size: 1.1rem; }

.section-badge {
    display: inline-block;
    background: linear-gradient(90deg, #21262d, #30363d);
    border: 1px solid #58a6ff; border-radius: 20px;
    padding: 0.2rem 0.8rem; font-size: 0.75rem;
    color: #58a6ff; font-weight: 600;
    letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.5rem;
}
.cleaning-step {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 8px; padding: 0.8rem 1rem; margin: 0.4rem 0;
    font-size: 0.9rem; color: #c9d1d9;
}
</style>
    """, unsafe_allow_html=True)


# ── Plotly theme helpers ──────────────────────────────────────────────────────
def theme(fig, height: int | None = None):
    """Apply dark transparent Plotly theme to a figure."""
    kw = dict(height=height) if height else {}
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(13,17,23,0.6)',
        font=dict(family='Inter, sans-serif', color='#c9d1d9'),
        margin=dict(t=40, b=30, l=10, r=10),
        legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='#30363d'),
        **kw,
    )
    return fig


def render_chart(fig, height: int | None = None) -> None:
    """Apply theme and render a Plotly chart at full container width."""
    st.plotly_chart(theme(fig, height), use_container_width=True)


# ── UI component helpers ──────────────────────────────────────────────────────
def insight(n: int, html: str) -> None:
    """Render a highlighted insight block with a numbered label."""
    st.markdown(f"""
<div class="insight-box">
  <span class="insight-number">#{n}</span>
  <p>{html}</p>
</div>""", unsafe_allow_html=True)


def badge(text: str) -> None:
    """Render a small section badge label."""
    st.markdown(f'<div class="section-badge">{text}</div>', unsafe_allow_html=True)
