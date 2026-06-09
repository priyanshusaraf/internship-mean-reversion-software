# DEVLOG

## 2026-06-10 — Doc 48 cycle: RB-CL archived · LE-GF COVID excuse falsified · second-sleeve screening proposed

- **Suite:** was red — loader silently aggregated duplicate daily rows via the intraday-resample
  path. Fixed (resample only when timestamps carry time-of-day); 182 green. `2988ad4`.
- **Inventory:** BRN1!/BRN2!, HO2!/RB2!/CL1!/CL2!, ZC legs on disk & TRUSTED. **NG1!/NG2! raw 1D
  legs ABSENT** (only ng12_spread.csv 2016–2026 + EIA xls) — NG back-adj closure stays data-blocked.
- **Prereg 48** (`rb_cl_alt_split_le_gf_subperiod_prereg.md`): frozen → adversarial audit
  INADMISSIBLE×2 (caught CL1!-for-CL2! leg substitution, vacuous excision premise, alpha undercount
  3-look→α=0.0167, PnL-derived ex-COVID window) → Revision 1+2 → ADMISSIBLE-WITH-CAVEAT → committed
  pre-data (`ea50be3`).
- **Execution (doc 48):**
  - Test A RB-CL alt split (IS 1998→2022-12, 6,131 bars, F6 β=1, f_βupdate=0.000): VR(20)=0.9008,
    p_rw=0.0798 ≥ 0.0167 → **ARCHIVED PERMANENT** (3-look alpha budget exhausted; no fourth look).
  - Test B LE-GF ex-COVID (excise 2020-01→2021-06): Sharpe 0.3508 < 0.50; placebo rank 36/67 =
    53.7th pctile < 90th → **COVID attribution FALSIFIED**; OOS weakness structural; IS anchor stands.
  - Combination gate **BLOCKED**.
- **Four-lens review:** statistical lens caught a real bug — power sim built AR(1) in LEVELS
  (realized VR≈0.047) while calibrated for increment-AR(1); claimed power 1.000 → corrected
  **0.284** (sim fixed in `run_48...py`, re-run, realized VR 0.8954 verified). "Genuine absence"
  language STRUCK from doc 48/registry — archive is "not detected," NOT demonstrated-absent (doc 45's
  30–40% power estimate vindicated). Other corrections: q-grid p=0.0639 transcription; LE-GF OOS
  actually starts 2019-05-24 (prereg prose said ~2014-08; rule followed exactly); 0.342-vs-0.233
  cross-doc Sharpe non-comparability noted. Trader lens: LE-GF MERELY-TRUE (2.7× IS→OOS compression
  now UNEXPLAINED → Track-1 harvest demoted to exploration); RB-CL/NG/combination NON-FINDING.
- **Artifacts updated:** doc 48 + four-lens block, 48_results.json (corrected power + provenance),
  HYPOTHESIS_REGISTRY (RB-CL row, header, new second-sleeve-screening row), PROJECT_STATE (full
  refresh; superseded crack-β plan collapsed into details).
- **Next high-information action:** freeze **prereg doc 49** — second-sleeve IS VR screening,
  **GC-SI first** (textbook cointegration; doubles as strongest remaining §11.8 anchor candidate:
  GC-SI failing to confirm = apparatus-recalibration signal), **PL-PA second**; frozen-β, doc-46
  protocol, sequential, cohort/α/splits frozen before any VR inspected, no argmax. Both fail →
  declare spread-MR book infeasible at current breadth.
