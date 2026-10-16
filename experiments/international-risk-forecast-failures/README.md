# International latent-risk forecast-failure experiments

This folder is an **isolated prospective experiment workspace** for
[the working paper](../../working_papers/international-risk-forecast-failures/README.md).
The older `dfm/`, `trend/`, and `output/trend_backtest_2008/` files are
**not** overwritten or silently re-used as internationally validated results.

## Stages

0. Audit candidate series and historical availability dates; record data sources and transformations.
1. Construct an ex-post full-sample DFM **for historical description only**.
2. Implement a pseudo-real-time expanding/rolling DFM fit and factor extraction with training-only scaling.
3. Implement the constrained Gaussian integrated-random-walk smoother (`d=2`) with marginal likelihood via Kalman filter; independently check its PLS penalty / variance-ratio equivalence.
4. Implement rolling-origin forecasts, frozen-vintage factor targets, conventional benchmarks and empirically calibrated intervals.
5. Lock episode windows, non-crisis controls, analysis plan and figures before full testing.
6. Audit per-country residual diagnostics, coverage, event dependence and false alarms; then write the paper.

Only stage-0 **input validation**, the design configuration, and its lightweight tests have been implemented here. **No external data have been downloaded, no new DFM has been fitted, and no international backtest has been executed.**

## Expected long-form input

One row per country, observation date and indicator:

```csv
country,observation_date,available_date,variable,value,source
MEX,2020-01-31,2020-02-07,m2,123.4,Banxico
```

The example above is **illustrative and not a real observation**. Use ISO dates `YYYY-MM-DD`; release/available dates must be auditable. For market data with a trade date, it is acceptable for observation and availability dates to coincide if justified.

At any forecast origin `t`, the eventual pipeline must select only rows for which `available_date <= t`; passing this file validator **does not** by itself certify the absence of leakage.

To audit a candidate panel (stdlib only):

```bash
python experiments/international-risk-forecast-failures/preflight.py --input path/to/panel.csv
```

To run the lightweight tests:

```bash
python -m unittest discover -s experiments/international-risk-forecast-failures/tests -v
```

`config.json` is a proposed starting configuration, not an executed study or a guarantee of complete data coverage. See the working paper's `research_protocol.md` for the two estimands and scientific protocol.

## Data integrity rules

- Preserve original source files and metadata separately; do not use published value dates as release dates.
- Duplicate `country × observation_date × variable` keys are rejected.
- Any observation becoming available before the reported observation date is rejected pending investigation.
- Do not replace missing values by a fill based on data not yet available at a historical origin.
- Time-dependent standardization and DFM parameters must be fitted to training vintages only.
- Keep synthetic test inputs out of scientific results and do not assert any crisis-detection result from this scaffold.
