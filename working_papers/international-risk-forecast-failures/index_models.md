# Candidate models for the country-specific financial-stress index

**Research design, not a model-selection result.** The first scientific choice is how the observable financial indicators are combined into a coherent stress index. The index construction model must be distinct from the **MLE-calibrated trend smoother** applied afterward.

## What is being compared?

Data-processing layer -> index-construction model -> same penalized/state-space trend smoother -> same forecast-error protocol. The four components have separate responsibilities. A Markov-switching model used directly for forecasting is a *forecast comparator*, not automatically an alternative to an index-construction model.

### Stage I: economical, interpretable candidates

| id | Model | Why test it? | Warning |
|---|---|---|---|
| `imf_style_equal_weight` | IMF-style standardized signed component average (the Emerging Markets Financial Stress Index is an antecedent) | Transparent benchmark; especially relevant to Mexico | Signs and membership must be economically predeclared; variance normalization fitted on training only |
| `pca_one_factor` | First principal component of a common, transformed financial indicator panel | Established St. Louis Fed benchmark; no dynamics imposed | Explains indicator variance, not necessarily risk; fix sign against training stress anchor |
| `dfm_gaussian` | Conventional one-factor Gaussian dynamic factor model | Original project baseline; models temporal dependence | Original project's 2004–2026 specification failed its recorded autocorrelation, normality and ARCH checks |

### Stage II: conditional extensions

| id | Model | Trigger to include |
|---|---|---|
| `robust_factor` | Robust covariance / M-estimated factor | One or a few extreme series disproportionately determine PCA loadings; robust estimator formally specified |
| `regime_switching_factor` | Markov-switching or time-varying-loadings factor | Strong evidence of changing loadings or correlation patterns not explained by volatility alone |
| `multi_factor` | Two interpretable factors (e.g. liquidity / market stress), instead of forced univariate risk | One factor cannot account for major distinct stress domains |

Do not silently call simple robust standardization 'robust PCA', and do not add complex models purely because they produce better-looking crisis peaks.

## Critical preprocessing changes before modeling

The original project used logged VIX, WTI, gold ETF and DXY levels. These series have different distributions and levels may trend over decades. The first pilot must distinguish volatility **levels** from price **returns/changes**, interest-rate **spreads**, currency depreciation, and macrofinancial quantities published with lags.

- Equity-market **returns** are signed so declines raise stress.
- Volatility **levels** (VIX or comparable local proxies) may rise during stress; decide whether level or innovations are the object.
- Yield **spreads** may be interpreted economically; raw yield direction is not invariant across easing and sovereign crises.
- WTI and gold **price changes** may have context-dependent stress interpretations; consider global controls instead of forcing a fixed signed weight.
- Avoid comparing national FX levels measured in different unit conventions; use changes relative to documented anchor exchange rates.
- M1/M2/reserves: monthly or lower frequency and released with a lag; never treat the reference month as the first available day.

The Federal Reserve Bank of St Louis redesigned its financial stress index to address trending levels in underlying series; this supports the need for thoughtful transformations before searching for a better factor model.

## Common-data and origin fairness

For every country, establish a *primary common indicator panel*. Fit each candidate on the same country, observation dates and available-at-origin information. An additional 'expanded country-specific data' exercise is permissible but is a **different comparison** and must be labeled separately.

Training-origin operations: choose transformations, imputation rules, scaling, loadings, signs and hyperparameters without future observations. For retrospective plots, full-sample fits may be shown but cannot establish real-time forecast performance.

All candidates must have a documented high-stress direction, factor scale convention and vintage-to-vintage alignment. A principal component can flip sign; a factor can arbitrarily change scale after refitting.

## How to compare without circularity

**Avoid comparing the raw forecast RMSE of model A's factor with the raw forecast RMSE of model B's factor.** These targets are *different latent variables* even if normalized to unit variance. An apparently easier-to-forecast index could win by suppressing relevant crisis information.

Compare three separate characteristics:

1. **Measurement plausibility:** association with prespecified, observed benchmarks (e.g. credit spreads, market drawdowns, an independently published stress index), sign coherence, stability of loadings across training windows, and sensitivity to deleting each variable.
2. **Forecast properties:** the same MLE trend forecast applied to each index, using fixed vintage filtering and calibration. Describe loss and tail behavior *within* each index, not cross-index RMSE ranks as if the outcome were identical. A stronger comparison is to score predictions against a predeclared **common external observable target** (e.g. future realized volatility, risk spread or independently defined crisis-window indicator).
3. **Statistical reliability:** Gaussian DFM residual autocorrelation, ARCH, heavy tails, interval calibration, factor instability and computation time. Count false alarms during non-crisis windows.

Define episodes and detection thresholds independently of the index output. If both PCA and DFM reflect the same 2008 event, that alone does not prove forecasting or early-warning ability.

## Sequencing

1. Finish the historically available monthly country data catalog (Mexico first).
2. Determine valid transformations; preserve release dates and actual vintages.
3. Pilot `imf_style_equal_weight`, `pca_one_factor`, `dfm_gaussian` on identical observable panels.
4. Apply the **same** constrained local-linear-trend marginal-MLE smoothing model to each pilot index; compare against random walk and factor-transition forecasts.
5. Choose extensions using train-only diagnostics. Declare the primary model-selection criteria **before** analyzing final crisis-window results.
6. Evaluate predetermined crisis and quiet windows, horizon-specific errors, calibration and false alarms. Report all prespecified candidates, including failures.

## References motivating the candidate models

- IMF, *World Economic Outlook*, April 2009, chapter 4; emerging-market financial stress index, including exchange pressure and variance-equal aggregation: https://www.elibrary.imf.org/display/book/9781589068063/ch004.xml
- St Louis Fed, *Financial Stress Index 2.0*, 2020, PCA and changes in trending series: https://www.stlouisfed.org/on-the-economy/2020/march/financial-stress-index-version-2
- Chicago Fed, *Introducing the New Adjusted NFCI*, 2017, dynamic-factor state-space method: https://www.chicagofed.org/publications/chicago-fed-letter/2017/386
- Statsmodels regime switching model documentation / implementation: https://www.statsmodels.org/stable/regime_switching.html

No new models or international experiments have been fitted as of this design update.
