# When Do Smoothed Financial Risk Indicators Fail to Forecast?

**Status:** research design and manuscript scaffold; no new international experiment has been run.
**Potential venue:** Boletín SMCCA (subject to scope and editorial review).
**Parent project:** `Estimation-of-latent-risk-in-the-U.S.-market-using-representative-variables`.
**Date initiated:** 2026-10-16.

## Scientific question

Across countries and financial episodes, when do forecasts obtained by extrapolating the smoothed trend of an estimated financial-stress factor fail, relative to conventional statistical forecasts? Do unusually large forecast errors carry information about regimes beyond time-varying volatility?

This is an **application and failure-analysis paper**, not a new article about the mathematical theory of smoothing, the numerical minimizer search, or an automatically validated crisis-warning system.

## Research artifacts

- [manuscript/main.tex](manuscript/main.tex) — compilable, results-free initial article draft.
- [research_protocol.md](research_protocol.md) — estimand, competing experiments, MLE method, controls, failure definitions, and preregistration decisions.
- [data_catalog.csv](data_catalog.csv) — candidate data families; sources and releases still require auditing.
- [../../experiments/international-risk-forecast-failures/README.md](../../experiments/international-risk-forecast-failures/README.md) — new, isolated experiment pipeline and input audit.
- [../../experiments/international-risk-forecast-failures/config.json](../../experiments/international-risk-forecast-failures/config.json) — prospective pilot configuration, **not executed**.

## Separation from other projects

- This repository contains the latent-risk index, country indicators, event analysis, and experiments.
- The separate `Trend-Estimation` repository remains the source for theoretical and numerical smoothing research. Do not copy its results here as evidence of international risk detection.
- Existing `dfm/`, `trend/`, `output/`, posters, and the historical 2008 backtest are **not changed** by this scaffold.

## What the original 2008 outputs show, and what they do not

`output/trend_backtest_2008/latent_factor_backtest_2008_stats.json` reports validation RMSE approximately 1.922 and June–December 2008 test RMSE approximately 30.103 for a long-horizon polynomial forecast. These are old descriptive results, **not** a replicated or prospective crisis detector.

Three cautions in the original implementation:
1. DFM parameters and input standardization were estimated through March 2026, then the factor was used in a pre-2008 forecasting exercise. This is retrospective information usage, unsuitable for a real-time performance claim.
2. The smoothness selected by the grid (`s=0.999`, validation MSE 3.694) is worse than a reported refined local minimum (`s≈0.7437`, validation MSE 3.525).
3. The selected Gaussian DFM did not pass its saved residual diagnostics. Exceedance claims based on simple normal bands require recalibration.

The new work distinguishes full-sample **retrospective description** from honest **pseudo-real-time forecasting**. Neither estimand should silently substitute for the other.

## Authorship and publication

The original project poster credits Heriberto Espino Montelongo, Owen Paredes Conde, and Pedro José García Guevara. Confirm author contributions and agreement before submission. The manuscript deliberately leaves its final author line pending.

The Boletín SMCCA states that scientific articles must be original and not simultaneously under consideration elsewhere; its official publication and policy page is https://www.smcca.org.mx/publicaciones.html. No claims of acceptance or a guaranteed deadline are made.

## Next technical milestone

Identify a feasible common monthly indicator panel for Mexico and at least three comparison markets, with actual publication or availability timestamps. Only after the panel audit should the DFM/likelihood estimation and historical-origin backtesting be implemented and executed.
