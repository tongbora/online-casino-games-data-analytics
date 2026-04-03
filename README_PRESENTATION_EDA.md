# 🎤 Presentation Guide — Exploratory Data Analysis (EDA)

Project: **The House Always Wins?**  
Audience: **Data Analytics Experts**  
Goal: Present a rigorous, data-driven EDA story from raw data to actionable insights.

---

## 1) Presentation Flow (Recommended)

Use this sequence for a clear and expert-friendly narrative:

1. **Problem Framing**
   - Research question: *Does the data support “The House Always Wins”?*
   - Define business/statistical objective: estimate and explain casino structural advantage.

2. **Dataset Context**
   - Source, scale (sample vs full data), key fields.
   - Clarify data grain: one row = one game configuration/specification.

3. **Data Understanding (EDA 1.1)**
   - Shape, schema, missingness, cardinality, summary stats.
   - Highlight suspicious fields and potential leakage/confounding risks.

4. **Data Cleaning & Feature Engineering (EDA 1.2)**
   - Explain each cleaning action and impact.
   - Show engineered features and why they improve interpretability.

5. **Univariate Analysis (EDA 1.3)**
   - Distributions for RTP, house edge, volatility, min bet, max multiplier.
   - Emphasize skewness, outliers, and practical interpretation.

6. **Bivariate/Multivariate Analysis (EDA 1.4)**
   - Compare house edge by game type/provider/volatility.
   - Correlation matrix and trend analysis over release years.

7. **Visual Synthesis (EDA 1.5)**
   - Show only charts that answer the research question.
   - Tie each visual to one analytical claim.

8. **Insights, Limits, and Next Steps (EDA 1.6)**
   - Present 3–5 strongest findings.
   - State assumptions, data limits, and future analysis plan.

---

## 2) Core EDA Formulas You Should Explain

### A) Return to Player (RTP)

$$
\text{RTP}(\%) = \frac{\text{Total Payout}}{\text{Total Bet}} \times 100
$$

Interpretation: expected long-run payback percentage to players.

### B) House Edge

$$
\text{House Edge}(\%) = 100 - \text{RTP}(\%)
$$

Interpretation: expected long-run casino advantage per dollar wagered.

### C) Win-to-Bet Ratio (engineered)

$$
\text{Win-to-Bet Ratio} = \frac{\text{Max Win}}{\text{Min Bet}}
$$

Interpretation: potential upside relative to entry cost.

### D) Capped Ratio (99th percentile cap)

$$
\text{Ratio}_{\text{capped}} = \min(\text{Ratio}, Q_{0.99})
$$

Interpretation: controls extreme outliers for stable visualization.

### E) Group Mean (used in comparisons)

$$
\bar{x}_g = \frac{1}{n_g}\sum_{i=1}^{n_g} x_i
$$

Used for: mean house edge by game type/provider/volatility group.

---

## 3) Speaker Notes (What to Say)

- “Our key metric is **house edge**, computed as $100 - RTP$.”
- “Even if volatility changes the player experience, it does not necessarily change expected value.”
- “We separate **mathematical expectation** from **session-level variance**.”
- “Outlier handling is visual-only for interpretability; raw values are preserved for metric computation when appropriate.”
- “Our conclusions are about game specifications, not individual player behavior trajectories.”

---

## 4) Expert Questions You May Be Asked (with Suggested Answers)

### Q1. Why EDA first, not predictive modeling?
**A:** The primary objective is explanatory: validate a market claim and identify structural patterns. EDA establishes data quality, signal strength, and assumptions before any modeling.

### Q2. How do missing values affect your conclusions?
**A:** We report missingness by variable, remove/retain fields with explicit rules, and explain impact. For example, heavily missing fields are excluded from core claims to avoid biased interpretation.

### Q3. Why cap at the 99th percentile?
**A:** To prevent a small number of extreme values from dominating visual scale. The cap is for chart readability, not to alter business conclusions.

### Q4. Did you test statistical significance between groups?
**A:** Current scope is EDA and effect interpretation. For formal inference, we can add hypothesis tests (e.g., ANOVA/Kruskal-Wallis) and confidence intervals in the next phase.

### Q5. Could provider differences be confounded by game mix?
**A:** Yes. Provider-level means can be confounded by game-type composition. A stratified comparison or multivariate model is a recommended next step.

### Q6. How robust are findings across sample vs full dataset?
**A:** We validate directional consistency on sample and full data when available; if discrepancies appear, full dataset takes precedence for final claims.

### Q7. Is RTP enough to describe risk for players?
**A:** No. RTP captures expected return, while volatility captures dispersion/variance of outcomes. Both are needed to explain practical player experience.

### Q8. Why is “bonus feature effect” considered negligible?
**A:** Observed RTP differences are very small in magnitude. We interpret this as limited practical impact under current data granularity.

### Q9. What are the main threats to validity?
**A:** Non-transactional data grain, missing jackpot details, and absence of player-level session behavior are key limitations.

### Q10. What is your next analytical step?
**A:** Add transaction-level data, perform stratified/inferential analysis, and estimate uncertainty intervals around key metrics.

---

## 5) Slide-by-Slide Structure (Quick Template)

1. Title + Research Question  
2. Data Source + Scope + Constraints  
3. Data Understanding (shape, types, missingness)  
4. Cleaning & Feature Engineering  
5. Univariate Findings  
6. Bivariate/Multivariate Findings  
7. Key Visual Summary  
8. Final Conclusion  
9. Limitations  
10. Q&A

---

## 6) One-Minute Conclusion Script

“Based on exploratory analysis, the data supports the claim that the house has a persistent structural advantage. The mean house edge is positive across major segments, while differences across game types and providers indicate where this advantage varies in magnitude. Volatility mainly changes risk experience rather than expected return. Our conclusions are robust for specification-level data, with clear next steps involving player-level transactions and inferential testing.”

---

## 7) Optional Appendix Topics (if experts ask deeper)

- Distribution diagnostics (skew, kurtosis, tails)
- Robust statistics (median/IQR vs mean/std)
- Stratified provider comparisons by game type
- Time-based drift checks by release year
- Bootstrap confidence intervals for house edge estimates
