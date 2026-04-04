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
    'blue': '#58a6ff',
    'green': '#3fb950',
    'red': '#f85149',
    'purple': '#bc8cff',
    'orange': '#ffa657',
}
PALETTE = ['#58a6ff', '#f0e68c', '#3fb950', '#f85149', '#bc8cff', '#ffa657', '#79c0ff', '#56d364']

VOL_ORDER = ['Low', 'Medium', 'High', 'Very High']

# ── Page sections (sidebar labels) ───────────────────────────────────────────
SECTIONS = [
    'Introduction',
    '1.1  Data Understanding',
    '1.2  Data Cleaning',
    '1.3  Univariate Analysis',
    '1.4  Bivariate & Multivariate',
    '1.5  Visualisations Summary',
    '1.6  Key Insights & Conclusion',
    'About the Authors',
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
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

:root {
    --app-bg: var(--background-color);
    --blue: #58a6ff;
    --app-bg-accent: color-mix(in srgb, var(--primary-color) 6%, var(--background-color));
    --app-text: var(--text-color);
    --sidebar-bg: color-mix(in srgb, var(--secondary-background-color) 94%, var(--background-color) 6%);
    --sidebar-bg-end: color-mix(in srgb, var(--secondary-background-color) 86%, var(--background-color) 14%);
    --sidebar-border: color-mix(in srgb, var(--text-color) 16%, transparent);
    --sidebar-text: var(--text-color);
    --sidebar-item-bg: color-mix(in srgb, var(--secondary-background-color) 76%, transparent);
    --sidebar-item-hover: color-mix(in srgb, var(--primary-color) 14%, var(--secondary-background-color) 86%);
    --sidebar-item-active: color-mix(in srgb, var(--primary-color) 24%, var(--secondary-background-color) 76%);
    --card-bg: color-mix(in srgb, var(--secondary-background-color) 90%, white 10%);
    --card-border: color-mix(in srgb, var(--text-color) 14%, transparent);
    --muted-text: color-mix(in srgb, var(--text-color) 58%, transparent);
    --metric-value: var(--text-color);
    --h1: color-mix(in srgb, var(--primary-color) 72%, var(--text-color) 28%);
    --h2: color-mix(in srgb, var(--primary-color) 60%, var(--text-color) 40%);
    --h2-border: color-mix(in srgb, var(--text-color) 14%, transparent);
    --h3: color-mix(in srgb, var(--primary-color) 48%, var(--text-color) 52%);
    --insight-bg: color-mix(in srgb, var(--secondary-background-color) 92%, var(--background-color) 8%);
    --insight-text: var(--text-color);
    --insight-border: var(--primary-color);
    --badge-bg: color-mix(in srgb, var(--secondary-background-color) 88%, var(--background-color) 12%);
    --badge-border: var(--primary-color);
    --badge-text: color-mix(in srgb, var(--primary-color) 75%, var(--text-color) 25%);
    --cleaning-bg: color-mix(in srgb, var(--secondary-background-color) 94%, var(--background-color) 6%);
    --cleaning-border: color-mix(in srgb, var(--text-color) 14%, transparent);
    --shadow: 0 10px 30px color-mix(in srgb, var(--text-color) 12%, transparent);
    --soft-shadow: 0 4px 14px color-mix(in srgb, var(--text-color) 8%, transparent);
}

.stApp {
    background:
        radial-gradient(circle at top right, color-mix(in srgb, var(--primary-color) 10%, transparent) 0, transparent 26%),
        radial-gradient(circle at left center, color-mix(in srgb, var(--primary-color) 8%, transparent) 0, transparent 20%),
        linear-gradient(180deg, var(--app-bg-accent), var(--app-bg));
    color: var(--app-text);
}

header[data-testid="stHeader"] {
    background: transparent;
}

main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2.2rem;
    max-width: 1400px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--sidebar-bg), var(--sidebar-bg-end));
    border-right: 1px solid var(--sidebar-border);
    box-shadow: var(--soft-shadow);
    backdrop-filter: blur(6px);
}

[data-testid="stSidebar"] * {
    color: var(--sidebar-text) !important;
}

div[data-testid="metric-container"] {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 1rem 1.05rem;
    box-shadow: var(--shadow);
}

div[data-testid="metric-container"] label {
    color: var(--muted-text) !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--metric-value) !important;
    font-size: 1.85rem !important;
    font-weight: 700 !important;
}

div[data-testid="stDataFrame"] {
    border: 1px solid var(--card-border);
    border-radius: 14px;
    overflow: hidden;
    box-shadow: var(--soft-shadow);
}

div[data-testid="stDataFrame"] * {
    font-size: 0.95rem;
}

.team-section {
    margin-top: 1rem;
}

.team-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 0.9rem;
    margin-top: 0.75rem;
}

.team-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 18px;
    padding: 1rem 1.05rem;
    box-shadow: var(--shadow);
    display: grid;
    grid-template-columns: 112px 1fr;
    align-items: center;
    gap: 0.9rem;
    position: relative;
    overflow: hidden;
}

.team-avatar {
    width: 96px;
    height: 96px;
    border-radius: 50%;
    margin: 0;
    display: grid;
    place-items: center;
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: 0.03em;
    color: #ffffff;
    background: linear-gradient(135deg, var(--primary-color), var(--blue));
    box-shadow: 0 8px 16px color-mix(in srgb, var(--primary-color) 20%, transparent);
}

.team-photo {
    width: 96px;
    height: 96px;
    border-radius: 50%;
    object-fit: contain;
    object-position: center;
    background: color-mix(in srgb, var(--secondary-background-color) 88%, var(--background-color) 12%);
    margin: 0;
    display: block;
    border: 2px solid var(--blue, #58a6ff);
    box-shadow: 0 8px 16px color-mix(in srgb, var(--primary-color) 18%, transparent);
}

.team-photo-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.team-photo-wrap::before {
    content: '';
    position: absolute;
    width: 110px;
    height: 110px;
    border-radius: 50%;
    border: 2px solid transparent;
    border-left-color: var(--blue, #58a6ff);
    border-top-color: var(--blue, #58a6ff);
    border-bottom-color: var(--blue, #58a6ff);
    opacity: 0.95;
    pointer-events: none;
}

.team-content {
    min-width: 0;
}

.team-name {
    font-size: 1.7rem;
    font-weight: 800;
    margin: 0;
    line-height: 1.05;
    color: var(--text-color);
}

.team-role {
    margin: 0.2rem 0 0.5rem;
    color: var(--blue, #58a6ff);
    font-size: 0.95rem;
    font-weight: 700;
}

.team-bio {
    margin: 0;
    color: var(--muted-text);
    line-height: 1.5;
    font-size: 0.92rem;
}

@media (max-width: 720px) {
    .team-card {
        grid-template-columns: 1fr;
        text-align: center;
    }

    .team-name {
        font-size: 1.4rem;
    }

    .team-role {
        margin-bottom: 0.4rem;
    }
}

h1, h2, h3, h4, h5, h6 {
    letter-spacing: -0.02em;
}

h1 {
    color: var(--h1);
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 0.35rem;
}

h2 {
    color: var(--h2);
    border-bottom: 1px solid var(--h2-border);
    padding-bottom: 0.4rem;
    margin-top: 1.5rem;
}

h3 {
    color: var(--h3);
}

p, li {
    line-height: 1.65;
}

a {
    color: color-mix(in srgb, var(--primary-color) 72%, var(--text-color) 28%);
    text-decoration-thickness: 1px;
    text-underline-offset: 0.15em;
}

a:hover {
    color: var(--primary-color);
}

.insight-box {
    background: var(--insight-bg);
    border-left: 4px solid var(--insight-border);
    border-radius: 0 14px 14px 0;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    box-shadow: var(--shadow);
}

.insight-box p {
    color: var(--insight-text);
    margin: 0;
    font-size: 0.95rem;
    line-height: 1.6;
}

.insight-number {
    color: var(--insight-border);
    font-weight: 700;
    font-size: 1.1rem;
}

.section-badge {
    display: inline-block;
    background: var(--badge-bg);
    border: 1px solid var(--badge-border);
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    font-size: 0.75rem;
    color: var(--badge-text);
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.cleaning-step {
    background: var(--cleaning-bg);
    border: 1px solid var(--cleaning-border);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin: 0.4rem 0;
    font-size: 0.9rem;
    color: var(--app-text);
}

button[kind="primary"], button[kind="secondary"] {
    border-radius: 999px !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label,
[data-testid="stSidebar"] label {
    border-radius: 10px;
}

[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
    background: var(--sidebar-item-bg);
    border: 1px solid color-mix(in srgb, var(--sidebar-border) 70%, transparent);
    padding: 0.28rem 0.5rem;
    transition: background 0.18s ease, border-color 0.18s ease;
}

[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
    background: var(--sidebar-item-hover);
    border-color: color-mix(in srgb, var(--primary-color) 36%, var(--sidebar-border) 64%);
}

[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:has(input:checked) {
    background: var(--sidebar-item-active);
    border-color: color-mix(in srgb, var(--primary-color) 55%, var(--sidebar-border) 45%);
    box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--primary-color) 26%, transparent);
}

[data-testid="stSidebar"] .stRadio [role="radiogroup"] {
    gap: 0.15rem;
}

[data-testid="stCaptionContainer"], [data-testid="stText"] {
    color: var(--muted-text);
}

section[data-testid="stVerticalBlock"] {
    gap: 0.35rem;
}
</style>
        """,
        unsafe_allow_html=True,
    )


# ── Plotly theme helpers ──────────────────────────────────────────────────────
def theme(fig, height: int | None = None):
    """Apply a Plotly theme that follows the active Streamlit light/dark mode."""
    def _parse_rgb(value: str):
        value = (value or '').strip().lower()
        if value.startswith('#') and len(value) in {4, 7}:
            if len(value) == 4:
                return (
                    int(value[1] * 2, 16),
                    int(value[2] * 2, 16),
                    int(value[3] * 2, 16),
                )
            return (int(value[1:3], 16), int(value[3:5], 16), int(value[5:7], 16))
        if value.startswith('rgb(') and value.endswith(')'):
            parts = [p.strip() for p in value[4:-1].split(',')]
            if len(parts) == 3 and all(part.isdigit() for part in parts):
                return tuple(int(part) for part in parts)
        return None

    def _luminance(rgb):
        r, g, b = rgb
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    base = (st.get_option('theme.base') or '').lower()
    if base in {'light', 'dark'}:
        is_light = base == 'light'
    else:
        bg_rgb = _parse_rgb(st.get_option('theme.backgroundColor') or '')
        text_rgb = _parse_rgb(st.get_option('theme.textColor') or '')
        if bg_rgb is not None:
            is_light = _luminance(bg_rgb) >= 128
        elif text_rgb is not None:
            is_light = _luminance(text_rgb) < 128
        else:
            is_light = True
    kw = dict(height=height) if height else {}
    fig.update_layout(
        template='plotly_white' if is_light else 'plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif', color='#18212f' if is_light else '#c9d1d9'),
        margin=dict(t=44, b=34, l=10, r=10),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor='#dbe2ee' if is_light else '#30363d',
            borderwidth=0,
        ),
        colorway=PALETTE,
        xaxis=dict(
            gridcolor='rgba(148,163,184,0.18)' if is_light else 'rgba(110,118,129,0.18)',
            zerolinecolor='rgba(148,163,184,0.22)' if is_light else 'rgba(110,118,129,0.18)',
            linecolor='rgba(148,163,184,0.28)' if is_light else 'rgba(110,118,129,0.28)',
        ),
        yaxis=dict(
            gridcolor='rgba(148,163,184,0.18)' if is_light else 'rgba(110,118,129,0.18)',
            zerolinecolor='rgba(148,163,184,0.22)' if is_light else 'rgba(110,118,129,0.18)',
            linecolor='rgba(148,163,184,0.28)' if is_light else 'rgba(110,118,129,0.28)',
        ),
        **kw,
    )
    return fig


def render_chart(fig, height: int | None = None) -> None:
    """Apply theme and render a Plotly chart at full container width."""
    st.plotly_chart(theme(fig, height), width='stretch')


# ── UI component helpers ──────────────────────────────────────────────────────
def insight(n: int, html: str) -> None:
    """Render a highlighted insight block with a numbered label."""
    st.markdown(
        f"""
<div class="insight-box">
  <span class="insight-number">#{n}</span>
  <p>{html}</p>
</div>""",
        unsafe_allow_html=True,
    )


def badge(text: str) -> None:
    """Render a small section badge label."""
    st.markdown(f'<div class="section-badge">{text}</div>', unsafe_allow_html=True)
