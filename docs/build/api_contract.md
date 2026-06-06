# API & Data Contract — Observatory v2 (FROZEN spine)

**Status:** DRAFT → freeze on owner sign-off. Once frozen, this is the single source of truth
that lets `backend-api`, `backtest-engine`, and `frontend-architect` work in parallel without
diverging. Changes after freeze require an explicit freeze-break note (CLAUDE.md §6).

**Companion docs:** `MASTER_DIRECTIVE_STRATEGY_BACKTEST_INTERFACE.md` (§3 strategy, §4 backtester),
`DIRECTIVE_OBSERVATORY_COCKPIT_FRONTEND.md` (panels). Read with both.

**Governing invariants (restated; non-negotiable):**
- **No statistic re-implemented in JS.** Every number (μ*, z, VR, half-life, habitat score,
  surrogate cloud) is produced by the existing frozen Python engines. Frontend renders only.
- **Causal firewall.** Any causal computation consumes only data with `timestamp ≤ as_of`.
  Forward data is never an input to a causal number; it is returned only as explicitly
  `evaluation_only` overlays.
- **Habitat is surrogate-relative.** Every habitat response carries its null distribution; a
  bare score is a contract violation. Never self-ranked against the instrument's own history.

---

## 0. DECISIONS MADE (reversible at freeze — flag any you want changed)

These are the load-bearing forks. Chosen for minimal/additive/reuse-first (CLAUDE.md §7) and to
not break the existing `/api/v1/market/*` workbench (§13 Workflow F — regression safety).

- **D1 — `dataset` reuses the existing instrument store.** A "dataset" IS a stored instrument in
  the existing DuckDB store; `dataset_id` == `instrument_id`. No parallel store is built. The new
  surface adds ingestion-with-mapping + quality + analysis on top of `store`/`loader`/`analytics`.
  *Alternative rejected:* a fresh parallel dataset store (duplicate persistence, divergence risk).
- **D2 — New clean surface `/api/v2/*`, existing `/api/v1/market/*` untouched.** The Observatory v2
  frontend talks to `/api/v2`. The legacy workbench keeps working unchanged. Both call the same
  engines under the hood.
  *Alternative rejected:* extend `/api/v1/market/*` (overloads a router with two contracts).
- **D3 — Habitat surrogate cloud requires a thin engine wrapper.** `calibrate_habitat_score.py`
  computes `real_mvr` + `null_mvrs[]` internally but returns only the scalar. We add
  `habitat_score_full(x, seed) -> {score, real_mvr, null_mvrs, vr_curve}` **reusing the identical
  VR/null code with the frozen constants unchanged** (`VR_QS=[5,10,20]`, `NS_NULL=2000`,
  `SEED_*`). This is a wrapper, not a reimplementation. The frozen `habitat_score()` stays as-is.
- **D4 — `as_of` is the single causal cursor convention, and is NEVER a no-op.** `as_of` = inclusive
  upper time bound on the data the engine may see (reuses the `≤ end` firewall in `/diagnostics`).
  **`as_of` omitted/null ≡ `as_of = last bar` — the cap is ALWAYS applied; the firewall can never be
  silently disabled.** A separate `[window_start, window_end]` selects the *scoring* window for
  habitat; `as_of` still caps what is loadable. See §5.

### 0.1 Mitigations folded in after adversarial review (pre-freeze)

The first draft was returned INADMISSIBLE-TO-FREEZE by `amr-adversarial` for two firewall holes and a
non-functional anti-p-hacking mechanism. The following are now binding in this contract:
- **M1 (§4.1):** z's σ is defined precisely as a **causal** quantity + a future-injection bit-identity
  acceptance test. (Closes: forward-vol leaking into interior-bar z.)
- **M2 (§5, D4):** `as_of` null ≡ last-bar; cap always applied. (Closes: optional-`as_of` = no firewall.)
- **M3 (§4.2, §9):** `habitat_score` and `habitat_score_full` MUST share **one** null-generating code
  path; bit-identity test required. (Closes: a second null loop drifting from the frozen calibration.)
- **M4 (§7):** minimal pre-reg pin store specified now; Verification is required for any verdict path;
  non-frozen params force an EXPLORATORY watermark in provenance. (Closes: decorative 409.)
- **M5 (§4.2):** frontend may not derive any scalar from `null_min_vr[]`.
- **M6 (§3, §1):** construction-admissibility (`beta_mode`, `roll_masked`) carried on every dataset;
  rolling-β spreads are blocked at the API. (Closes: inadmissible-β construction entering analysis.)

---

## 1. Dataset model

A dataset is a parsed, validated OHLCV series persisted in the session store.

```jsonc
Dataset {
  "dataset_id":   "string",        // == instrument_id; filename-stem upper, or user-set
  "name":         "string",        // display name
  "source_file":  "string",        // original uploaded filename
  "frequency":    "daily" | "intraday" | "unknown",  // inferred from median timestamp delta
  "row_count":    int,
  "date_range":   { "start": "YYYY-MM-DD", "end": "YYYY-MM-DD" },
  "columns":      ["open","high","low","close","volume"],   // post-mapping canonical columns
  "column_map":   {                // the mapping actually used to parse the source
                    "timestamp": "string",   // source column chosen as timestamp
                    "close":     "string",
                    "open":      "string | null",
                    "high":      "string | null",
                    "low":       "string | null",
                    "volume":    "string | null"
                  },
  "date_format":  "auto" | "unix" | "iso" | "dd-mm-yyyy",   // override applied
  "timezone":     "string | null", // e.g. "UTC"; null = naive
  "is_spread":    bool,            // constructed via frozen-β spread (future)
  "construction": {                // M6 — admissibility of how the series was built
    "beta_mode":  "none" | "definitional" | "frozen-ols" | "rolling-INADMISSIBLE",
    "roll_masked": bool            // continuous-contract roll seams masked (k=8.0) — null if N/A
  },
  "created_at":   "ISO-8601"
}
```

**M6 (binding):** any analysis endpoint **rejects with 422** a dataset whose
`construction.beta_mode == "rolling-INADMISSIBLE"` (`"rolling-β is inadmissible for a gating read"`;
CLAUDE.md §6.3, kill-ledger). Non-spread datasets carry `beta_mode:"none"`. Spread construction
(future endpoint) must set `definitional` (β=1) or `frozen-ols` (pre-sample-OLS-then-frozen).

The parsed series is fetched separately (see `GET /api/v2/datasets/{id}/series`), not embedded
in the metadata object.

---

## 2. Endpoints — ingestion & datasets

### `POST /api/v2/datasets`
Upload a CSV + explicit column mapping → parse → persist → return dataset metadata + quality.

`multipart/form-data`: `file` (the CSV), plus a JSON `mapping` part:
```jsonc
mapping {
  "name":        "string | null",   // default: filename stem uppercased
  "column_map":  { "timestamp":"...", "close":"...", "open":null, "high":null, "low":null, "volume":null },
  "date_format": "auto" | "unix" | "iso" | "dd-mm-yyyy",   // default "auto"
  "timezone":    "string | null"
}
```
- If `column_map` is omitted, the server auto-detects (existing loader aliases) and echoes back the
  mapping it used, so the UI can show/override it.
- `date_format:"auto"` → try unix epoch, then ISO8601, then dayfirst dd-mm-yyyy (existing loader order).
- **Response 200:** `{ "dataset": Dataset, "quality": QualityReport }` (see §3).
- **Response 422:** `{ "detail": "string" }` — unparseable / missing required close / empty.

### `GET /api/v2/datasets`
List loaded datasets. **Response 200:** `{ "datasets": Dataset[] }`.

### `GET /api/v2/datasets/{id}`
**Response 200:** `Dataset`. **404** if unknown id.

### `GET /api/v2/datasets/{id}/series?as_of=&start=&end=`
Parsed OHLCV bars for charting. Optional `as_of` (causal cap), `start`/`end` (view range).
**Response 200:**
```jsonc
{
  "dataset_id": "string",
  "as_of": "YYYY-MM-DD | null",
  "bars": [ { "time":"YYYY-MM-DD", "open":f, "high":f, "low":f, "close":f, "volume":f } ],
  "forward_bars": [ ... ]   // bars with time > as_of, when as_of set; marked evaluation_only
}
```
- When `as_of` is set: `bars` = data ≤ as_of (causal), `forward_bars` = data > as_of
  (`evaluation_only`; never an input to any causal computation). When `as_of` is null,
  `forward_bars` is `[]`.

### `GET /api/v2/datasets/{id}/quality`
Re-run the data-quality report on demand. **Response 200:** `QualityReport` (§3).

---

## 3. QualityReport

Mandatory on ingest; nothing proceeds on a silently broken series.

```jsonc
QualityReport {
  "row_count":    int,
  "date_range":   { "start":"YYYY-MM-DD", "end":"YYYY-MM-DD" },
  "frequency":    "daily" | "intraday" | "unknown",
  "median_delta_days": float,         // basis for frequency inference
  "gaps": [                           // calendar gaps materially larger than the modal delta
    { "from":"YYYY-MM-DD", "to":"YYYY-MM-DD", "missing_bars": int }
  ],
  "n_gaps":            int,
  "duplicate_timestamps": int,        // dupes seen pre-resample
  "non_positive_prices": {
    "count": int,
    "examples": [ { "time":"YYYY-MM-DD", "close": f } ],
    "suggested_excision": { "from":"YYYY-MM-DD", "to":"YYYY-MM-DD" } | null  // CL Apr-2020 case
  },
  "nan_rows_dropped": int,
  "back_adjustment_seams": [ { "time":"YYYY-MM-DD", "jump": f } ],  // best-effort; may be []
  "warnings": [ "string" ]            // human-readable flags surfaced in the UI
}
```
- `non_positive_prices.count > 0` → UI flags it and offers the excision window; it does **not**
  silently drop. (Spread/relative-value series legitimately go negative — flag, don't reject.)

---

## 4. Endpoints — analysis (engine wrappers)

Both wrap existing frozen engines. Causal by construction; `as_of` enforced server-side.

### `POST /api/v2/analysis/equilibrium`
Wraps `analytics.compute_kalman_mu_star` (causal 2-state Kalman, CLAUDE.md §6.3 frozen).

**Request:**
```jsonc
{
  "dataset_id": "string",
  "as_of":      "YYYY-MM-DD | null",   // causal cap; engine sees only data ≤ as_of
  "start":      "YYYY-MM-DD | null",   // optional view trim (still ≤ as_of)
  "end":        "YYYY-MM-DD | null",
  "params":     { "snr": 1e-8, "kappa": 0.05, "warmup": 60 }  // optional; default = FROZEN constants
}
```
**Response 200:**
```jsonc
{
  "dataset_id": "string",
  "as_of": "YYYY-MM-DD | null",
  "params": { "snr": f, "kappa": f, "warmup": int },
  "series": [
    {
      "time":      "YYYY-MM-DD",
      "close":     f,
      "mu_star":   f,    // mu_star_kalman (posterior equilibrium)
      "velocity":  f,    // kalman_velocity
      "innovation":f,    // epsilon_kalman (research residual)
      "z":         f|null,  // M1 — see z definition below; null until warmup σ defined
      "gain":      f,
      "state_var": f
    }
  ],
  "z_sigma_basis": "causal_expanding_innovation_std",   // the ONLY permitted basis (M1)
  "provenance": Provenance   // §6
}
```
- `mu_star`, `velocity`, `innovation` come verbatim from the engine. `z` and its σ are computed in
  Python (backend), never JS.
- **M1 — z is strictly causal. Binding definition:** `z[t] = (close[t] − mu_star[t]) / σ[t]` where
  **`σ[t] = std( epsilon_kalman[t'] for t' ≤ t )`** — a **causal expanding** std over the innovation
  series up to and including bar `t` only (min 2 obs; `z=null` before that). σ[t] may use **only** past
  innovations; it may NOT be a single std over the whole returned array (that would scale interior-bar
  z by future volatility — the leak this clause closes). `z_sigma_basis` is fixed to
  `"causal_expanding_innovation_std"`; no other basis is permitted by this contract.
- **M1 acceptance test (gates the slice):** future-injection bit-identity — appending any rows with
  `time > as_of` to the input and recomputing must leave every `z[t]` for `t ≤ as_of`
  **bit-identical**. A diff is a firewall failure.
- Default params = the frozen constants (§6.3). Non-frozen params are allowed only in Research mode,
  force `mode:"research"` + an EXPLORATORY watermark in provenance, and are **rejected (409)** in
  Verification mode if they deviate from the pinned pre-reg (§7).

### `POST /api/v2/analysis/habitat`
Wraps `habitat_score_full` (D3) — the surrogate-relative MR habitat score over a window.

**Request:**
```jsonc
{
  "dataset_id":   "string",
  "window":       { "start":"YYYY-MM-DD", "end":"YYYY-MM-DD" },  // the scored window
  "as_of":        "YYYY-MM-DD | null",   // causal cap; window.end must be ≤ as_of when as_of set
  "deseason":     false,                 // raw (default) vs deseasonalized
  "params":       { "vr_qs":[5,10,20], "ns_null":2000, "seed":20260606 }  // optional; default FROZEN
}
```
**Response 200:**
```jsonc
{
  "dataset_id": "string",
  "window": { "start":"...", "end":"..." },
  "deseason": false,
  "score":   f,            // 0-100, surrogate-relative; null if window too short / non-finite
  "real_min_vr": f,        // realized min-VR over q∈vr_qs
  "vr_curve": [ { "q":5,"vr":f }, { "q":10,"vr":f }, { "q":20,"vr":f } ],
  "surrogate_distribution": {            // the cloud the UI MUST render — never omitted
    "null_min_vr": [ f, ... ],           // per-surrogate min-VR (RW + MA(1) nulls)
    "n": int,
    "p10": f, "p50": f, "p90": f,
    "frac_ge_real": f                    // == score/100
  },
  "calibration_badge": { "ou": 71.3, "rw": 49.2, "trend": 17.2, "status": "validated_non_inverting" },
  "raw_vs_deseason": {                   // present when both are computed; drives contamination flag
    "raw_score": f | null,
    "deseason_score": f | null,
    "verdict_changed": bool | null       // true → UI shows contamination warning (BRN lesson)
  } | null,
  "data_warning": "string | null",       // e.g. non-positive prices → VR on log undefined
  "provenance": Provenance
}
```
- `surrogate_distribution` is **mandatory**. A response without it is a contract violation.
- **M3 — single null-generating code path (binding).** `habitat_score_full` and the frozen
  `habitat_score` MUST NOT contain two copies of the null loop. Refactor so the null construction
  (RW + MA(1), vol-matched) runs **once**: `habitat_score_full(x, seed)` computes
  `{score, real_min_vr, null_min_vr, vr_curve}`; `habitat_score(x, seed)` returns
  `habitat_score_full(...).score`. Frozen constants (`VR_QS=[5,10,20]`, `NS_NULL=2000`, seeds)
  unchanged. **Acceptance tests (gate the slice):** (a) `habitat_score_full(x,seed).score ==
  habitat_score(x,seed)` bit-identical; (b) re-running `calibrate_habitat_score` *through the wrapper*
  reproduces the frozen badge (OU≈71.3 / RW≈49.2 / trend≈17.2). A drift means the badge lies — block.
- **M5 — backend owns every scalar.** `null_min_vr[]` is shipped **for rendering the cloud only**. The
  frontend MUST NOT derive any statistic from it (no re-percentiling, no own `frac_ge_real`, no
  re-binning into a score). `p10/p50/p90/frac_ge_real` are authoritative and backend-computed. A JS
  scalar derived from `null_min_vr[]` is a no-JS-math violation.
- Non-positive series: `data_warning` set, `score` may be null (log-VR undefined) — surfaced, not hidden.

---

## 5. The `as_of` causal-cursor convention (binding)

- `as_of` is an **inclusive upper bound** on timestamps any causal computation may consume.
- **M2 — `as_of` is never a no-op.** Omitted/null `as_of` is resolved server-side to the **last bar**
  of the series before any engine runs; the `timestamp ≤ as_of` slice is therefore **always** applied.
  There is no code path on an analysis endpoint where the engine sees rows it then treats as future.
  (This is the fix for the `store.get_ohlcv(end=…)` "no bound when end is falsy" hole — the resolver
  guarantees `end` is always truthy for causal reads.)
- On every analysis endpoint, the server slices the series to `timestamp ≤ as_of` **before** the
  engine runs. The engine never receives forward rows.
- `start`/`end`/`window` select what is **displayed or scored**; they never widen past `as_of`.
  If `window.end > as_of`, the request is **422** (`"window extends past as_of"`).
- Forward data (`timestamp > as_of`) is returned **only** under `forward_bars` /
  `evaluation_only` overlays, never inside a causal series array.
- **Firewall acceptance test (gates the slice):** for any endpoint, appending rows with
  `time > as_of` to the dataset and recomputing must not change any causal output at `t ≤ as_of`
  (bit-identical). Applies to `mu_star`, `velocity`, `innovation`, `z`, and `score`.

---

## 6. Provenance (on every analysis result)

```jsonc
Provenance {
  "dataset_id":  "string",
  "dataset_hash":"string",     // hash of the parsed series (reproducibility)
  "as_of":       "YYYY-MM-DD | null",
  "params":      { ... },      // the exact parameter set used
  "mode":        "research" | "verification",
  "prereg_id":   "string | null",   // set in verification mode (the pin used)
  "exploratory_watermark": bool,    // M4 — true if any param deviates from frozen default
  "engine":      "string",     // e.g. "compute_kalman_mu_star" / "habitat_score_full"
  "engine_version": "string",  // git short-sha or module version
  "computed_at": "ISO-8601"
}
```

---

## 7. Research vs Verification mode (anti-p-hacking) — M4

Requests carry `"mode": "research" | "verification"` (default `"research"`).

- **research:** params free. Provenance marks `mode:"research"`; any param differing from the frozen
  default sets `provenance.exploratory_watermark: true` and the result is labelled "EXPLORATORY —
  not a verdict" in the UI. A watermarked result can never be promoted to a verdict.
- **verification:** params are **not taken from the request body** — they are loaded from a
  **pinned pre-reg** identified by `"prereg_id"` (required when `mode:"verification"`). The server
  ignores any params in the body and uses the pinned set; if the body's params deviate from the pin,
  it **409s** rather than silently overriding (catches accidental post-hoc tuning).

**Pre-reg pin store (specified now so Verification is not decorative):** a server-side, append-only
store `data/build/prereg_pins/<prereg_id>.json`, each pin containing
`{ prereg_id, dataset_id, endpoint, params, as_of|window, criteria, frozen_at, source_doc }`, written
once and thereafter immutable (a re-pin under the same id is a 409). `POST /api/v2/prereg/pins`
creates one; `GET /api/v2/prereg/pins/{id}` reads it. **Binding:** any result intended as a verdict
MUST be produced in `verification` mode against a pin; `research`-mode and watermarked results are
exploratory only. localStorage never holds Verification params (Directive §2.7).

---

## 8. Conventions

- **Dates:** `YYYY-MM-DD` strings in all payloads (day-level store). Timestamps: ISO-8601.
- **Floats:** JSON numbers; non-finite (NaN/Inf) serialized as `null`, never `NaN`.
- **Errors:** `{ "detail": "string" }`. 404 unknown id · 422 bad data/parse/window · 409 verification
  param violation.
- **Caching:** results cache key = `(dataset_hash, endpoint, params, as_of, window, deseason)`.
  Habitat is computed **on demand** for the selected window only — never eager per-bar across the
  series (T2.5 performance lesson).
- **CORS / base URL:** unchanged from existing app (`localhost:3000-3002`, `:8000`).

---

## 9. Engine reuse map (what wraps what — no new math)

| Endpoint                        | Engine (existing)                                  | New code |
|---------------------------------|----------------------------------------------------|----------|
| `POST /datasets`, `/quality`    | `loader.load_ohlcv` + new `quality_report()`       | quality computation (read-only over parsed frame) |
| `GET  /datasets*`, `/series`    | `store.*`                                           | v2 serialization only |
| `POST /analysis/equilibrium`    | `analytics.compute_kalman_mu_star`                  | z & σ in Python; serialization |
| `POST /analysis/habitat`        | `calibrate_habitat_score` → `habitat_score_full` (D3) | distribution-returning wrapper (same math, frozen consts) |

**No statistic is implemented in TypeScript.** The only new numerical code is (a) the quality
report (descriptive counts/gaps over the parsed frame), (b) z = (close−μ*)/σ in Python, and
(c) the habitat wrapper that returns arrays the engine already computes internally.

---

## 10. Step-2 vertical slice acceptance (what this contract must enable)

1. Upload one CSV → column-map step (auto-detect unix/ISO/dd-mm-yyyy + override) → ingest →
   `QualityReport` shown (flags gaps, dupes, non-positive — the CL Apr-2020 case).
2. Price chart with a draggable **as-of cursor** (hide-forward).
3. Overlay Kalman **μ\*** + **z** from `POST /analysis/equilibrium`, causal to the cursor.
4. Select a date range → `POST /analysis/habitat` → habitat **score + surrogate cloud** +
   **raw-vs-deseason** toggle.

**Acceptance tests that gate the slice (from the mitigations):**
- **Firewall bit-identity (M1, M2):** appending rows `time > as_of` changes no causal output at
  `t ≤ as_of` (`mu_star`, `velocity`, `innovation`, `z`, `score`).
- **Habitat single-path (M3):** `habitat_score_full(x,seed).score == habitat_score(x,seed)`
  bit-identical; calibration badge reproduced through the wrapper (OU≈71.3/RW≈49.2/trend≈17.2).
- **No-JS-math (M5):** no statistic derived in TypeScript from `null_min_vr[]` or any array.
- **Construction gate (M6):** a `rolling-INADMISSIBLE` dataset is 422-rejected by analysis endpoints.

Sign-off by `amr-rigor-qa` (firewall enforced · surrogate cloud shown · no JS math · provenance
present · the four acceptance tests above) before the slice is "done."
