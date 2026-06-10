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

## 2026-06-10b (autonomous tick) — Doc 49 executed; four-lens review INVALIDATED the terminal labels

- **Executed prereg 49:** GC-SI speed-gate fail (level-spread IS VR(20)=1.0106, p_rw=0.6418);
  PL-PA halted at flat-bar gate (PL2! 12.39% post-trim, pervasive 1998–2007). Runner labeled
  GC-SI "clean kill" and cohort "EXHAUSTED → book infeasible."
- **Four-lens review (adversarial + statistical, independent) — both INADMISSIBLE-AS-EVIDENCE:**
  1. **Frozen-tree bypass:** power 0.176 (ref VR=0.90) < 0.30 mandates INCONCLUSIVE-UNDERPOWERED +
     §11.8 report; the speed-gate branch hardcoded SPEED_GATE_KILL (runner JSON itself said
     UNDERPOWERED/11_8_trigger=true). Branch fixed in run_49 script.
  2. **Construction-induced kill (decisive):** gold/silver ratio drifted 39.9→83.1 over IS; frozen
     level-β=39.48 inherits the drift as trend (64.6% of Var(spread) = linear trend) → VR≈1 was
     near-guaranteed by construction. Log-ratio same windows: VR=0.947 IS / 0.797 OOS. GC-SI result
     carries NO market evidence either way. §11.8 not validly exercised.
- **Corrected labels (doc 49 + JSON + registry + PROJECT_STATE):** GC-SI = INCONCLUSIVE-UNDERPOWERED
  / CONSTRUCTION-INADMISSIBLE; PL-PA = data-source verdict, pair untested; cohort =
  COHORT-UNRESOLVED-UNDERPOWERED; "book infeasible at current breadth" STRUCK.
- **CONTAMINATION DISCLOSURE:** the audit's diagnostic peek at GC-SI log-ratio VR (favorable) means
  any future GC-SI log-spread prereg is NOT blind — must disclose + alpha-price the look.
- **BLOCKED → RESEARCHER DECISION:** how to alpha-price the contaminated peek in the GC-SI
  log-spread re-test prereg (the only named live path to the second sleeve). Not auto-frozen.

## 2026-06-10c — Doc 50: GC-SI log-ratio → INCONCLUSIVE-UNDERPOWERED; peek exposed as window-specific

- User said "continue" → researcher-delegate adjudication of the contaminated-peek alpha problem:
  log-ratio β=1 definitional (no presample, kills doc-49 wrong-object defect, recovers full series);
  α=0.0167 (3-look family incl. the peek); audit added: PASS leaf = PEEK-CONDITIONED (IS is ~64%
  peeked rows; Bonferroni can't price run-selection) + MANDATORY disjoint unpeeked 1998-2005 check.
- **Result (frozen tree followed exactly, incl. universal underpowered branch):** speed-gate
  p_rw=0.468; power 0.228 → INCONCLUSIVE-UNDERPOWERED. Substance: full-IS VR(20)=0.985 (near-RW);
  **unpeeked 1998-2005 slice VR=1.16 p=0.93 — TRENDS**; only the peeked windows are favorable
  (2005-2018: 0.947; OOS: 0.773 p=0.018, non-promotable). The disjoint check caught the peek as
  window-specific selection — the audit mandate earned its keep.
- Registry/PROJECT_STATE updated; reopen = pre-1998 data depth (re-run frozen spec, no redesign).
- **RESEARCHER DECISION (new):** (a) acquire pre-1998 GC/SI history (power unlock), (b) accept
  single-sleeve status → LE-GF economics prereg as primary path, (c) new platinum data for PL-PA.
