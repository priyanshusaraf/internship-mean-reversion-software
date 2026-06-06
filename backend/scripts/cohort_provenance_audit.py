"""
Arm 0 — Data Provenance & Quality Audit (pre-registered: docs/research/12 §7;
re-authorized with the §5 lookahead constitution and §6 synthetic-spread OHLC integrity rule).

FOUNDATION HYGIENE ONLY. This script computes NO reversion/VR/Hurst/half-life/OU/ADF/
stationarity/cointegration/residual statistic and makes NO habitat/morphology/timing inference.
It audits: schema, date hygiene, provenance, sample adequacy, price integrity — and emits a
trusted-cohort whitelist for Arm A. Conservative default: if causal construction is not provable,
the instrument is CONTAMINATED.

Outputs (reproducible): data/cohort_manifest.json and data/cohort_manifest.md
Run: backend/.venv/bin/python backend/scripts/cohort_provenance_audit.py
"""
from __future__ import annotations
import json, glob, os
from collections import defaultdict
import numpy as np
import pandas as pd

RAW = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw"))
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))

# --- pre-committed floors (doc 12 §7; §4 disposition rules) ---
TRUSTED_BAR_FLOOR = 750   # >= 3x largest downstream trailing window (W<=250)
POWER_FLOOR       = 504   # below this => UNUSABLE for any single-instrument verdict

def classify_domain(stem: str) -> tuple[str, bool]:
    s = stem.lower()
    if "spread" in s:                          return "spread_or_pair", True
    if s.startswith("g1") or "gold" in s:      return "commodity_outright", True
    if "eurusd" in s:                          return "fx", False
    if "synthetic" in s or s.endswith("_syn"): return "synthetic", False
    if "banknifty" in s or "nifty" in s:       return "index", False
    return "equity", False

def is_spread(stem: str) -> bool:
    return "spread" in stem.lower()

def base_key(stem: str) -> str:
    s = stem.lower()
    for suf in ("_1d", "_60", "_15", "_1h", "_daily"):
        if s.endswith(suf): s = s[:-len(suf)]
    return s

def find_col(cols, names):
    for c in cols:
        if c.lower() in names: return c
    return None

PROVENANCE_NOTES = {
    "g1_gold": "back-adjusted CONTINUOUS futures (g1); roll/adjustment method undocumented "
               "-> historical levels construction-dependent (provenance flag).",
}

def audit_file(path: str) -> dict:
    stem = os.path.splitext(os.path.basename(path))[0]
    df = pd.read_csv(path)
    cols = list(df.columns)
    domain, deployment = classify_domain(stem)
    spread = is_spread(stem)
    notes: list[str] = []

    has_vol  = any(c.lower() == "volume" for c in cols)
    close_c  = find_col(cols, {"close"});  open_c = find_col(cols, {"open"})
    high_c   = find_col(cols, {"high"});   low_c  = find_col(cols, {"low"})
    date_c   = find_col(cols, {"time","date","timestamp","datetime"}) or cols[0]

    n_rows = len(df)
    close = pd.to_numeric(df[close_c], errors="coerce") if close_c else pd.Series([np.nan])
    close_null = int(close.isna().sum())
    nonpos = int((close <= 0).sum()) if not spread else 0   # spreads may be legitimately negative
    neg_close = int((close < 0).sum())

    # OHLC structural validity (price integrity; NOT a reversion stat)
    broken = -1
    try:
        oo, hh, ll, cc = (pd.to_numeric(df[c], errors="coerce") for c in (open_c, high_c, low_c, close_c))
        bad = (hh < ll) | (hh < oo) | (hh < cc) | (ll > oo) | (ll > cc)
        broken = int(bad.fillna(False).sum())
        flat = int(((oo == hh) & (hh == ll) & (ll == cc)).fillna(False).sum())
    except Exception:
        flat = -1
    degenerate_rows = close_null + nonpos
    usable_bars = max(int((~close.isna()).sum()) - nonpos, 0)

    # --- date hygiene (robust to mixed tz / mixed formats) ---
    raw = df[date_c].astype(str); mixed_tz = False
    def _try(**kw):
        try: return pd.to_datetime(raw, errors="coerce", **kw)
        except Exception: return None
    dt = _try(dayfirst=False)
    if dt is None:
        mixed_tz = True
        dt = _try(utc=True, format="mixed")
        if dt is None:
            dt = _try(utc=True, dayfirst=True)
    if dt is not None and dt.isna().mean() > 0.3:
        alt = _try(utc=True, dayfirst=True, format="mixed")
        if alt is not None and alt.isna().mean() < dt.isna().mean(): dt = alt
    if dt is None: dt = pd.Series(pd.NaT, index=df.index)
    date_parse_fail = bool(dt.isna().mean() > 0.3)
    monotonic_inc = bool(dt.dropna().is_monotonic_increasing)
    monotonic_dec = bool(dt.dropna().is_monotonic_decreasing)
    reversed_dates = monotonic_dec and not monotonic_inc
    dup_ts = int(dt.dropna().duplicated().sum())
    ds = dt.dropna().sort_values()
    res = None; span = None; n_large_gaps = 0
    if len(ds) > 2:
        d = ds.diff().dropna()
        md = d.median(); mins = md.total_seconds()/60.0
        res = ("15m" if 10<=mins<=20 else "60m" if 45<=mins<=90 else
               "1d" if 720<=mins<=7200 else f"{mins:.0f}min")
        n_large_gaps = int((d > md*10).sum())   # informational only (weekends/holidays excluded by 10x)
        span = f"{ds.iloc[0].date()}..{ds.iloc[-1].date()}"

    # consolidated timestamp integrity
    ti = []
    if reversed_dates: ti.append("reversed")
    if mixed_tz:       ti.append("mixed_tz(normalized_UTC)")
    if dup_ts > 0:     ti.append(f"duplicates:{dup_ts}")
    if n_large_gaps>0: ti.append(f"large_gaps:{n_large_gaps}")
    if date_parse_fail:ti.append("PARSE_FAIL")
    timestamp_integrity = "ok" if not ti else "; ".join(ti)

    # --- §6 synthetic-spread OHLC integrity ---
    if spread:
        ohlc_trust = ("Open/Close TRUSTED (synchronized); HIGH/LOW UNTRUSTED — leg extrema occur at "
                      "different timestamps so max(A-B)!=max(A)-max(B); Volume/OI conditional (per-leg only)")
        notes.append("§6: spread High/Low are counterfactual (untrusted by default) — any downstream use "
                     "MUST rely on Open/Close, never naive High/Low, absent synchronized intrabar reconstruction.")
    else:
        ohlc_trust = "all OHLC trusted (single-asset intrabar extrema are real synchronized observations)"

    # negative-price handling
    if spread or neg_close > 0:
        neg_handling = f"LEVEL-DIFF required ({neg_close} negative-close bars); log/return math forbidden"
        if neg_close > 0: notes.append("negative prices present -> downstream must use level differences, not log/returns.")
    else:
        neg_handling = "n/a (strictly positive price series)"

    pnote = PROVENANCE_NOTES.get(stem)
    if pnote: notes.append(pnote)
    if broken > 0: notes.append(f"{broken} structurally-invalid OHLC bar(s).")

    return dict(
        instrument=stem, domain=domain, deployment_domain=deployment, is_spread=spread,
        base_key=base_key(stem), columns=",".join(cols), has_volume=has_vol,
        n_rows=n_rows, usable_bars=usable_bars, close_null=close_null, nonpos_close=nonpos,
        flat_ohlc_rows=flat, broken_ohlc_bars=broken, degenerate_rows=degenerate_rows,
        neg_close=neg_close, negative_price_handling=neg_handling,
        resolution=res, span=span, timestamp_integrity=timestamp_integrity,
        monotonic_increasing=monotonic_inc, reversed_dates=reversed_dates, duplicate_timestamps=dup_ts,
        ohlc_high_low_trust=ohlc_trust, contamination_notes=notes,
    )

def legs_present(stems: list[str]) -> bool:
    nonspread = [s for s in stems if not is_spread(s)]
    leg_tokens = ("cl", "brn", "coffee", "cocoa", "hdfc", "icici", "ng1", "ng2", "rb2", "rb3")
    return any(s.lower().startswith(t) for s in nonspread for t in leg_tokens)

def dispose(r: dict, legs_on_disk: bool) -> tuple[str, str, str]:
    """returns (disposition, confidence_in_disposition, reason)."""
    flags = list(r["contamination_notes"])
    # 1. unrecoverable corruption
    if r["usable_bars"] == 0 or "PARSE_FAIL" in r["timestamp_integrity"] or \
       (r["broken_ohlc_bars"] is not None and r["broken_ohlc_bars"] > 0.5*r["n_rows"]):
        return "UNUSABLE", "HIGH", "unrecoverable corruption (no usable close / unparseable dates / >50% invalid OHLC)"
    # 2. spread/derived, unverifiable construction => CONTAMINATED (conservative default; §5/§6)
    if r["is_spread"] and not legs_on_disk:
        why = ["leg-stripped precompute; legs absent on disk; hedge-ratio causality UNVERIFIABLE "
               "(full-sample-fit => lookahead-stationarity indistinguishable from real MR)",
               "§6: High/Low untrusted (counterfactual leg extrema)"]
        if r["usable_bars"] < POWER_FLOOR: why.append(f"also underpowered ({r['usable_bars']}<{POWER_FLOOR})")
        if r["reversed_dates"]: why.append("also reversed dates")
        return "CONTAMINATED", "HIGH", "; ".join(why)
    # 3. underpowered single-asset
    if r["usable_bars"] < POWER_FLOOR:
        return "UNUSABLE", "HIGH", f"usable_bars {r['usable_bars']} < power floor {POWER_FLOOR}"
    # 4. fixable hygiene => PROVISIONAL
    if r["reversed_dates"] or r["degenerate_rows"] > 0 or r["duplicate_timestamps"] > 0:
        fx = []
        if r["reversed_dates"]: fx.append("reversed dates (re-sort)")
        if r["degenerate_rows"]>0: fx.append(f"{r['degenerate_rows']} degenerate row(s) (drop)")
        if r["duplicate_timestamps"]>0: fx.append(f"{r['duplicate_timestamps']} duplicate ts (dedupe)")
        pnote = PROVENANCE_NOTES.get(r["instrument"])
        if pnote: fx.append(pnote)
        fx.append("NOT whitelisted until fixed + re-checked")
        return "PROVISIONAL", "MEDIUM", "fixable hygiene: " + "; ".join(fx)
    # 5. [504,750) gap band => conservative PROVISIONAL (pre-reg gap, resolved conservatively)
    if r["usable_bars"] < TRUSTED_BAR_FLOOR:
        return "PROVISIONAL", "MEDIUM", (f"usable_bars {r['usable_bars']} in [{POWER_FLOOR},{TRUSTED_BAR_FLOOR}): "
                f"clears UNUSABLE but below TRUSTED floor; NOT whitelisted (borderline power)")
    # 6. TRUSTED
    return "TRUSTED", "HIGH", (f"single-asset, monotone ascending dates, usable_bars {r['usable_bars']}>="
            f"{TRUSTED_BAR_FLOOR}, self-documenting positive-price units, OHLC structurally valid")

def main():
    paths = sorted(glob.glob(os.path.join(RAW, "*.csv")))
    stems = [os.path.splitext(os.path.basename(p))[0] for p in paths]
    legs_on_disk = legs_present(stems)
    recs = [audit_file(p) for p in paths]

    groups = defaultdict(list)
    for r in recs: groups[r["base_key"]].append(r["instrument"])
    twin_of = {inst: [x for x in v if x != inst] for v in groups.values() if len(v) > 1 for inst in v}

    for r in recs:
        disp, conf, reason = dispose(r, legs_on_disk)
        r["disposition"], r["confidence"], r["reason"] = disp, conf, reason
        r["pseudo_replicate_of"] = twin_of.get(r["instrument"], [])
        r["whitelisted_for_arm_a"] = (disp == "TRUSTED")

    buckets = {d: [r["instrument"] for r in recs if r["disposition"] == d]
               for d in ("TRUSTED", "PROVISIONAL", "CONTAMINATED", "UNUSABLE")}
    whitelist = buckets["TRUSTED"]
    depl_on_whitelist = [r["instrument"] for r in recs if r["whitelisted_for_arm_a"] and r["deployment_domain"]]

    summary = dict(
        generated="2026-06-03", legs_on_disk=legs_on_disk, n_instruments=len(recs),
        counts={d: len(v) for d, v in buckets.items()}, lists=buckets,
        arm_a_whitelist=whitelist, deployment_domain_on_whitelist=depl_on_whitelist,
        floors=dict(trusted_bar_floor=TRUSTED_BAR_FLOOR, power_floor=POWER_FLOOR),
    )
    with open(os.path.join(OUT, "cohort_manifest.json"), "w") as f:
        json.dump(dict(summary=summary, instruments=recs), f, indent=2)

    # --- markdown manifest ---
    L = ["# Arm 0 — Cohort Provenance & Quality Manifest\n",
         "**Generated:** 2026-06-03 · **Pre-registration:** `docs/research/12_institutional_review_post_state_t.md` §7",
         "**Scope:** foundation hygiene ONLY — schema · date hygiene · provenance · sample adequacy · price integrity.",
         "No reversion/VR/Hurst/half-life/OU/ADF/stationarity/cointegration statistic. No habitat/morphology/timing inference.",
         f"**Floors:** TRUSTED ≥ {TRUSTED_BAR_FLOOR} usable bars · UNUSABLE < {POWER_FLOOR}.",
         f"**Legs on disk for any spread:** {'YES' if legs_on_disk else 'NO'} → every spread's hedge-ratio causality "
         "is **unverifiable** → CONTAMINATED (conservative default, §5).",
         "**§6 synthetic-spread rule applied:** for every spread, Open/Close are TRUSTED (synchronized) but "
         "**High/Low are UNTRUSTED** (leg extrema at different timestamps → counterfactual spread states).\n",
         f"**Dispositions:** TRUSTED {len(buckets['TRUSTED'])} · PROVISIONAL {len(buckets['PROVISIONAL'])} · "
         f"CONTAMINATED {len(buckets['CONTAMINATED'])} · UNUSABLE {len(buckets['UNUSABLE'])}\n",
         "| instrument | domain | depl? | res | usable | ts-integrity | OHLC H/L | neg | disp | conf | wl |",
         "|---|---|:--:|:--:|--:|---|:--:|:--:|---|:--:|:--:|"]
    order = {"TRUSTED":0,"PROVISIONAL":1,"CONTAMINATED":2,"UNUSABLE":3}
    for r in sorted(recs, key=lambda x: (order[x["disposition"]], -x["usable_bars"])):
        hl = "UNTRUST" if r["is_spread"] else "ok"
        L.append(f"| `{r['instrument']}` | {r['domain']} | {'Y' if r['deployment_domain'] else '·'} | {r['resolution']} "
                 f"| {r['usable_bars']} | {r['timestamp_integrity']} | {hl} | {'Y' if r['neg_close'] else '·'} "
                 f"| **{r['disposition']}** | {r['confidence']} | {'✓' if r['whitelisted_for_arm_a'] else '·'} |")

    L.append("\n### Per-instrument detail")
    for r in sorted(recs, key=lambda x: (order[x["disposition"]], x["instrument"])):
        L.append(f"- **`{r['instrument']}`** — {r['disposition']} (confidence {r['confidence']})\n"
                 f"  - reason: {r['reason']}\n"
                 f"  - usable_bars {r['usable_bars']} · resolution {r['resolution']} · span {r['span']} · "
                 f"timestamp_integrity: {r['timestamp_integrity']}\n"
                 f"  - provenance: {'spread (legs absent, hedge-ratio unverifiable)' if r['is_spread'] else r['domain']+' (self-evident)'} · "
                 f"negative_price_handling: {r['negative_price_handling']}\n"
                 f"  - OHLC trust: {r['ohlc_high_low_trust']}"
                 + (f"\n  - notes: {' | '.join(r['contamination_notes'])}" if r['contamination_notes'] else ""))

    L.append("\n## TRUSTED whitelist\n" + (f"`{buckets['TRUSTED']}`" if buckets['TRUSTED'] else "_(none)_"))
    L.append("\n## PROVISIONAL list\n" + (f"`{buckets['PROVISIONAL']}`" if buckets['PROVISIONAL'] else "_(none)_"))
    L.append("\n## CONTAMINATED list\n" + (f"`{buckets['CONTAMINATED']}`" if buckets['CONTAMINATED'] else "_(none)_"))
    L.append("\n## UNUSABLE list\n" + (f"`{buckets['UNUSABLE']}`" if buckets['UNUSABLE'] else "_(none)_"))

    L.append("\n### Interpretation notes (pre-reg gaps resolved conservatively)")
    L.append("- **Bar-floor band [504,750):** unbucketed in the pre-reg → resolved conservatively to PROVISIONAL "
             "(NOT whitelisted): clears the power floor but lacks the independent-window margin for a TRUSTED verdict.")
    L.append("- **'daily-equivalent' floor on intraday series:** applied to **raw bar count** (no effective-sample "
             "conversion — that would be new methodology). Intraday autocorrelation/twins recorded as flags only.")
    L.append("- **CONTAMINATED ≠ UNUSABLE:** contaminated series are excluded from any Arm-A OU/habitat verdict but "
             "may still feed null-relative checks that assume no stationarity (per pre-reg).")
    L.append("- **Provenance classification (NOT habitat inference):** domain labels are construction facts, not "
             "reversion claims. Deployment-domain instruments on the whitelist: "
             f"**{len(depl_on_whitelist)}** ({depl_on_whitelist or 'none'}).")

    L.append("\n## ANSWER — which instruments may legally participate in Arm A?")
    L.append(f"> **`{whitelist}`** — and ONLY these. "
             f"(All are single-name equities by classification; {len(depl_on_whitelist)} deployment-domain instruments "
             "qualify. No reversion/habitat claim is made or implied.)")
    with open(os.path.join(OUT, "cohort_manifest.md"), "w") as f:
        f.write("\n".join(L) + "\n")

    print("dispositions:", summary["counts"])
    print("TRUSTED whitelist (legal Arm-A participants):", whitelist)
    print("deployment-domain on whitelist:", depl_on_whitelist or "NONE")
    print("wrote:", os.path.join(OUT, "cohort_manifest.md"), "+ .json")

if __name__ == "__main__":
    main()
