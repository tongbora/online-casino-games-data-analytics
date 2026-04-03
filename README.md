# 🃏 The House Always Wins? — PPIU Data Analytics EDA

> **Story Angle #2** — Analysing the relationship between RTP, house edge, volatility,
> and player odds across **1.2 million** online casino game records.

**Phnom Penh International University · Data Analytics · 2026**

---

## 📖 About

This project is a Streamlit-based **Exploratory Data Analysis (EDA)** dashboard for
an online casino games dataset hosted on **Google Drive**.

The app is designed to start quickly:

- it loads a **small bundled sample** by default for fast deployment and exploration
- it can optionally download the **full dataset** from Google Drive when requested

**Research question:**
> *Does the data support the famous saying — "The House Always Wins"?*

The analysis covers all six EDA requirements:
| # | Section |
|---|---|
| 1.1 | Data Understanding |
| 1.2 | Data Cleaning & Preparation |
| 1.3 | Univariate Analysis |
| 1.4 | Bivariate & Multivariate Analysis |
| 1.5 | Visualisations |
| 1.6 | Key Insights & Conclusion |

---

## 🚀 Quickstart

### 1. Create & activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate       # macOS / Linux
# .venv\Scripts\activate        # Windows
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Dataset

```bash
# The app already includes a fast sample dataset.
# If you want the full dataset locally, download it from Google Drive:
mkdir -p data/raw
wget -O data/raw/online_casino_games.csv \
  "https://drive.google.com/uc?export=download&id=1-YkXYX8s3zwu3jqcvGa9kpawOr14rVcP"
```

By default, the dashboard uses the bundled sample file at
`data/raw/online_casino_games_sample.csv`.

If you switch off **Use sample dataset (fastest)** in the sidebar, the app will
attempt to download the full CSV from Google Drive and store it at
`data/raw/online_casino_games.csv`.

Large data files are excluded from git — see `data/README.md`.

### 3. Launch the Streamlit dashboard

```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

### 4. (Optional) Run the Jupyter notebook

```bash
jupyter notebook notebooks/eda_template.ipynb
```

Select the **`Python (.venv) — data-analytics`** kernel when prompted.

---

## 🗂️ Project Structure

```
data-analytics/
│
├── app.py                          # Streamlit entry point (routing only)
│
├── dashboard/                      # Streamlit app package
│   ├── config.py                   # CSS, colours, Plotly theme, UI helpers
│   ├── data.py                     # Data loading & cleaning (cached)
│   └── pages/                      # One module per EDA section
│       ├── introduction.py         #  Introduction & research question
│       ├── data_understanding.py   # 1.1 Dimensions, types, missing values
│       ├── data_cleaning.py        # 1.2 Cleaning steps & feature engineering
│       ├── univariate.py           # 1.3 Single-variable distributions
│       ├── bivariate.py            # 1.4 Relationships & correlations
│       ├── visualisations.py       # 1.5 All charts in tabbed view
│       └── insights.py             # 1.6 Findings, conclusion, limitations
│
├── src/
│   └── eda/
│       └── utils.py                # Reusable helpers: load_csv, summarize_dataframe, top_categories
│
├── notebooks/
│   └── eda_template.ipynb          # Jupyter EDA template (7 structured cells)
│
├── data/
│   └── raw/
│       ├── online_casino_games_sample.csv # Small bundled sample for fast startup
│       └── online_casino_games.csv        # Full dataset (downloaded on demand, gitignored)
│
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `pandas` | Data loading, manipulation, aggregation |
| `numpy` | Numerical operations |
| `plotly` | Interactive charts in the dashboard |
| `streamlit` | Web dashboard UI |
| `matplotlib` | Static plots (notebook) |
| `seaborn` | Statistical visualisations (notebook) |
| `scikit-learn` | Trendline computation (OLS regression) |
| `pyarrow` | Fast CSV/Parquet I/O |
| `jupyter` | Notebook environment |

---

## 📊 Dashboard Pages

| Sidebar | Content |
|---|---|
| **🏠 Introduction** | Research question, dataset KPIs, story overview |
| **1.1 Data Understanding** | 20-column variable table, missing value charts, summary stats |
| **1.2 Data Cleaning** | 7 cleaning steps with justifications, engineered features |
| **1.3 Univariate Analysis** | RTP, house edge, volatility, min bet, max multiplier distributions |
| **1.4 Bivariate & Multivariate** | House edge by game type, correlation matrix, provider ranking, trend over years |
| **1.5 Visualisations Summary** | All key charts in 4 tabs (House Edge / Volatility / Game Types / Win Potential) |
| **1.6 Key Insights & Conclusion** | 5 data-backed findings, conclusion, limitations, next steps |

---

## 🔑 Key Findings (Preview)

1. **The house always wins** — average house edge is **~3.8 %** across all games.
2. **Game type matters most** — choosing the right game type has more impact than any playing strategy.
3. **Volatility ≠ better odds** — high-volatility games offer bigger multipliers but identical house edge.
4. **Bonus features are marketing** — free spins and bonus buys change RTP by < 0.1 percentage points.
5. **Marginal industry improvement** — RTPs have nudged upward since 2010, but the structural advantage remains.

---

## ⚙️ Utilities (`src/eda/utils.py`)

```python
from src.eda.utils import load_csv, summarize_dataframe, top_categories

df      = load_csv("data/raw/online_casino_games.csv", nrows=200_000)
summary = summarize_dataframe(df)          # rows, cols, dtypes, missing counts
top10   = top_categories(df, "game_type") # count + share for top N categories
```

---

## 📝 Notes

- All charts are purposeful and labelled — each contributes directly to the story.
- Cleaning decisions are documented in the **1.2 Data Cleaning** dashboard page.
- The bundled sample keeps the app responsive on Streamlit Cloud and local startup.
- Toggle **"Use sample dataset (fastest)"** in the sidebar for quick exploration; uncheck to load the full 1.2M dataset from Google Drive.
- On Streamlit Cloud, the full dataset is stored only in the app runtime filesystem and may need to be downloaded again after a restart or redeploy.
