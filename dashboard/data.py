"""
dashboard/data.py
─────────────────
Data loading and cleaning logic for the EDA dashboard.
Both functions are cached so Streamlit only runs them once per session.
"""

from pathlib import Path
import os
import sys

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))
from src.eda.utils import load_csv

SAMPLE_CSV_PATH = ROOT / 'data' / 'raw' / 'online_casino_games_sample.csv'
CSV_PATH        = Path('/tmp/data/online_casino_games_dataset_v2.csv')
KAGGLE_DATASET  = 'igormerlinicomposer/online-casino-games-dataset-1-2m-records'  # ← your dataset slug
KAGGLE_FILENAME = 'online9_casino_games_dataset_v2.csv'                               # ← filename inside the zip
SAMPLE_ROWS     = 50_000


def _ensure_local_csv(use_sample: bool = True) -> Path:
    """Return sample CSV when enabled, otherwise fetch full CSV from Kaggle."""
    if use_sample:
        if SAMPLE_CSV_PATH.exists():
            return SAMPLE_CSV_PATH
        st.error('❌ Sample dataset is missing from data/raw/online_casino_games_sample.csv.')
        st.stop()

    if CSV_PATH.exists():
        return CSV_PATH

    # Set credentials from Streamlit secrets
    try:
        os.environ['KAGGLE_USERNAME'] = st.secrets['kaggle']['username']
        os.environ['KAGGLE_KEY'] = st.secrets['kaggle']['key']
    except Exception:
        st.error('❌ Missing Kaggle secrets. Add [kaggle].username and [kaggle].key in Streamlit secrets.')
        st.stop()

    try:
        import kaggle
    except Exception:
        st.error('❌ Kaggle package is not installed. Add `kaggle` to requirements.txt.')
        st.stop()

    kaggle.api.authenticate()

    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    kaggle.api.dataset_download_files(
        KAGGLE_DATASET,
        path=str(CSV_PATH.parent),
        unzip=True,
        quiet=True,
    )

    if not CSV_PATH.exists():
        st.error('❌ Download did not produce the expected CSV file.')
        st.stop()

    return CSV_PATH


@st.cache_data(show_spinner='⏳ Loading dataset…')
def load_raw(nrows: int | None = None, use_sample: bool = True) -> pd.DataFrame:
    """Load the raw CSV with optional row limit."""
    csv_path = _ensure_local_csv(use_sample=use_sample)
    return load_csv(csv_path, nrows=nrows)


@st.cache_data(show_spinner='⚙️ Cleaning data…')
def load_clean(nrows: int | None = None, use_sample: bool = True) -> tuple[pd.DataFrame, list[tuple]]:
    """
    Return the cleaned DataFrame and a log of cleaning steps.

    Cleaning steps
    --------------
    1. Drop `jackpot`  (89 % missing)
    2. Drop rows with null `max_multiplier`
    3. Engineer `house_edge`           = 100 − rtp
    4. Engineer `win_to_bet_ratio`     = max_win / min_bet
    5. Cap `win_to_bet_ratio` at 99th percentile
    6. Make `volatility` an ordered Categorical
    7. Parse `last_updated` as datetime
    """
    df = load_raw(nrows, use_sample=use_sample)
    log: list[tuple[str, str, str]] = []     # (action, justification, icon)

    # 1 ── drop jackpot
    n_missing = df['jackpot'].isna().sum()
    pct = n_missing / len(df) * 100
    df = df.drop(columns=['jackpot'], errors='ignore')
    log.append(('Dropped `jackpot` column',
                 f'{pct:.1f}% missing ({n_missing:,} / {len(df)+n_missing:,} rows). Not usable.',
                 '🗑️'))

    # 2 ── drop null max_multiplier
    before = len(df)
    df = df.dropna(subset=['max_multiplier'])
    dropped = before - len(df)
    log.append(('Dropped rows with null `max_multiplier`',
                 f'{dropped:,} rows removed ({dropped/before*100:.1f}%). Required for reward analysis.',
                 '🗑️'))

    # 3 ── house_edge
    df['house_edge'] = (100 - df['rtp']).round(4)
    log.append(('Engineered `house_edge`',
                 '`house_edge = 100 − rtp`.  Direct measure of casino advantage per bet.',
                 '⚙️'))

    # 4 ── win_to_bet_ratio
    df['win_to_bet_ratio'] = (df['max_win'] / df['min_bet']).round(2)
    log.append(('Engineered `win_to_bet_ratio`',
                 '`max_win / min_bet`.  Maximum potential upside relative to entry cost.',
                 '⚙️'))

    # 5 ── cap outliers
    cap = df['win_to_bet_ratio'].quantile(0.99)
    df['win_to_bet_ratio_capped'] = df['win_to_bet_ratio'].clip(upper=cap)
    log.append(('Capped `win_to_bet_ratio` at 99th pct',
                 f'Values above {cap:,.0f}x capped for visualisation only.',
                 '✂️'))

    # 6 ── ordered volatility
    vol_order = ['Low', 'Medium', 'High', 'Very High']
    df['volatility'] = pd.Categorical(df['volatility'],
                                      categories=vol_order, ordered=True)
    log.append(('Ordered `volatility` as ordinal',
                 'Set Low < Medium < High < Very High for correct axis ordering.',
                 '🔄'))

    # 7 ── parse dates
    df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce')
    df['update_year']  = df['last_updated'].dt.year
    log.append(('Parsed `last_updated` as datetime',
                 'Extracted `update_year` for trend charts.',
                 '📅'))

    return df, log