# Research protocol — international latent-risk forecast failures

**Status: prospective design; neither protocol nor event set is preregistered. No results are claimed.**

## 1. Two questions, two estimands

**A. Ex-post historical description:** Fit a common dynamic factor model (DFM) and scaling on an entire country's sample. Describe when a forecast of the historical latent index departs from that same retrospectively defined index. This is a reconstruction of historical relationships, **not a real-time detector**. Call full-sample smoothing of the factor, if used, ex-post two-sided smoothing, not a vintage forecast.

**B. Pseudo-real-time forecasting:** For each origin `t`, perform all fitting, scaling, sign identification, tuning, variance calibration, and prediction using only observations **available by t**. Forecast `h` months ahead and later score against a factor estimated under a *fixed vintage measurement model*, updated with newly observed indicators through `t+h` (filtered, not full-sample smoothed). This target is model-defined, not a directly observed latent truth. Any re-estimation that changes factor scale/sign requires a deterministic anchoring rule and a common reference convention.

**Primary scientific analysis:** B; A for descriptive figures and interpretation. Report A and B separately and never treat A as evidence of genuine out-of-sample warning capability.

## 2. Latent factor

For country `c`, indicators `X_{c,t}` obey `X_{c,t}=Lambda_c f_{c,t}+u_{c,t}`, with a specified factor transition and idiosyncratic dynamics.

- Estimate loadings, states and transformations only on the training vintage for B.
- Factor scale and sign are unidentified without conventions. Anchor sign against a pre-declared stress indicator (e.g. equity volatility or a financial-stress spread) **using training data only**; impose unit training-factor variance. A global sign chosen with future data is not allowed in B.
- Factor estimates have uncertainty; do not call them observed realized economic risk or claim one unit has identical meaning across countries.
- The original US pipeline uses VIX, WTI, GLD and DXY; these are not a universal panel for other countries. Choose coherent *types* of local financial indicators before choosing exact proxies.
- The original DFM selected a Gaussian one-factor AR(2) specification with AR(1) idiosyncratic errors, but all three classes of saved residual diagnostics failed. It is a benchmark, not a validated universal model.

## 3. Primary smoothing: state-space likelihood

For an extracted factor `f_t`, the *restricted* Gaussian trend model is

```text
f_t            = tau_t + eps_t,       eps_t ~ iid N(0, r)
Delta^d tau_t  = eta_t,               eta_t ~ iid N(0, q)
lambda         = r / q
```

This recovers the usual quadratic penalized trend *conditional on appropriate initial-state treatment and model assumptions*. Specify the treatment of the unpenalized polynomial nullspace (diffuse initial conditions). Estimate positive `q,r` by the **marginal Gaussian likelihood** from a Kalman filter, *not* by maximizing the joint likelihood over each `tau_t` without integrating it out. MLE is conventional; REML or diffuse/restricted likelihood is a useful sensitivity check if the initial-state parameters create finite-sample issues.

With `d=2` this is a constrained integrated-random-walk local-linear trend: level and slope are initialized diffusely, and only slope-change innovations are free. The generic 'local linear trend' implementation may also have a distinct level shock, so its smoothing solution need not equal this exact PLS penalty unless that variance is constrained to zero. Confirm the actual implementation before asserting equivalence. A nonzero estimated drift of the dth difference changes the model and must be declared.

**Other comparison methods:** fixed `S=1` (polynomial extrapolation), pre-specified fixed smoothing, validation/rolling horizon-matched forecast CV, and (when meaningful) GCV. Keep estimation of the factor separate from selection of the smoother.

**Forecast alternatives:** random walk, drift / simple autoregression, and a parsimonious factor-transition-model forecast. Compare all methods on the same origins, targets and horizons. Do not assume polynomial extrapolation is a uniquely appropriate forecast of a financial-stress factor.

## 4. DFM diagnostics and intervals

- Log residual autocorrelation, conditional heteroskedasticity, heavy tails, factor stability and convergence, *by country and vintage*.
- A diagnostic rejection does not automatically make a factor useless for historical description, but it undercuts Gaussian tail-probability or '99.9% confidence' claims.
- Compare the baseline Gaussian DFM to robust/heteroskedastic or state-space alternatives *only where identifiable and supported by sufficient observations*.
- For forecast exceedances, use rolling or split-calibration empirical quantiles (or a demonstrated volatility model), plus nominal 90%, 95%, and 99% coverage checks; account for factor extraction uncertainty where possible.
- A high squared error can arise from wrong factor dynamics, wrong trend extrapolation, measurement changes, variance shifts, or genuine structural breaks. Conduct attribution and model comparison, not automatic crisis classification.

## 5. Panel and source policy

**Suggested first pilot:** monthly, United States, Mexico, United Kingdom, Japan, euro-area aggregate; extend to Canada/Switzerland if a common panel is feasible. Frequencies must be harmonized by defensible aggregation and point-in-time release dates. Monetary aggregates and reserves are usually lower-frequency and often released with delays, so they should not be mistaken for same-day information.

Candidate common classes:
- country equity-market return and realized volatility (local)
- nominal/effective FX changes (local; euro-area definition stated)
- short sovereign rate and yield-curve spread (local)
- credit or bank stress proxy (when coverage supports it)
- global oil/gold market variables as *shared controls*, not assumed country-specific stress measures

Macro-financial extensions: M1/M2 and reserve holdings, with publication lags and comparability documented. Gold reserves are not the market gold price.

**Sources to audit (do not assume a specific series is already available):**
- Banco de Mexico SIE API: https://www.banxico.org.mx/SieAPIRest/swagger/index.html
- Banco de Mexico monetary aggregates (CF807): https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarCuadroAnalitico&idCuadro=CF807&locale=en
- Banco de Mexico international reserves (CF456): https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarCuadro&idCuadro=CF456&locale=en
- IMF data: https://data.imf.org/
- OECD Data Explorer: https://data-explorer.oecd.org/

Each delivered row must record **observation_date**, **available_date**, **source**, **country**, **variable** and **value**. At forecast origin `t`, include an observation only if `available_date <= t`. Respect data revisions and vintages when those can be recovered. Missing release metadata mean the series cannot support a strict real-time claim unless a conservative rule and sensitivity test are declared.

## 6. Events and controls

Candidate events for *prospective selection* (do not choose based on resulting errors): 2008–2009 global crisis; 2011–2012 euro-area debt crisis; 2015 CHF policy break; 2016 Brexit referendum; 2020 pandemic shock; 2022 inflation/rate tightening and UK gilt turmoil; March 2023 banking turbulence. Mexican cases: 2008, 2020 and 2023; 1994–1995 as a separate historical-data extension because the US 2004-onward proxy set does not span that crisis.

For documented Mexican event chronology see Banxico:
https://www.banxico.org.mx/TablasWeb/informes-trimestrales/enero-marzo-2023/03BE2D8C-56CB-4D35-B9C3-707EBD648D02.html

**Controls:** time periods without pre-declared crises; matched country × time-of-year × volatility conditions where defensible; alternative event windows; global/common-shock sensitivity; negative controls and false-alarm rates. Do not retrospectively pick crises because the model displayed large errors.

## 7. Forecast failures and metrics

For an origin `t`, horizon `h`, define `e[c,t,h] = f_target[c,t+h|vintage(t)] - f_forecast[c,t+h|t]`. Report absolute and squared loss, MAE, RMSE, and horizon-stratified standardized scores `z=e/sigma_hat[c,t,h]`; sigma_hat must be estimated without test outcomes and include any modeled uncertainty contributions.

- Predictive accuracy: matched RMSE/MAE compared with random-walk, AR, factor-dynamics and fixed-smoothing baselines.
- Reliability: empirical exceedance frequency at pre-declared thresholds, interval coverage, calibration plots, average interval score (if available).
- Regime sensitivity: crisis-vs-quiet differences with uncertainty clustered by event and country; avoid interpreting many serially correlated months as independent samples.
- Detection utility (secondary): pre-event lead, false-positive count, sensitivity and specificity only if a predefined *alarm rule* is operational at the relevant date.
- Robustness: number of factors, indicator subsets, likelihood vs forecast CV, horizon, observation-vintage conventions, rolling vs expanding history, failure types and release-lag assumptions.

A large difference between realized and forecasted **latent factors** is not automatically evidence of a failed **trend estimator**; distinguish innovations, measurement errors, factor uncertainty and forecast-model misspecification.

## 8. Decision gates before running a large experiment

1. Create and audit a data catalog for comparable US/Mexico/UK/Japan/euro-area indicators; require source, transformations, calendar and release dates.
2. Check the factor-model parameterization and convergence on historical training windows; decide and document cross-country scale anchors.
3. Unit-test a one-country synthetic or small real panel for absence of future-data use, exact forecasting horizon and likelihood optimization.
4. Freeze event definitions, country coverage, baseline list and primary metrics.
5. Run a small historical pilot, then the full cross-country experiment. Do not report pilot-selected comparisons as independent confirmation.
6. Write results into the manuscript only after code, outputs and diagnostic audits exist.

## 9. Work ownership and overlap

This paper concerns application and forecast-failure evidence. The mathematical properties and numerical minimization of the smoothing objective belong to the separate Trend-Estimation working papers. Any reused method should be cited; do not repackage the theoretical paper as a new independent contribution. Confirm authorship with the original latent-risk project collaborators.
