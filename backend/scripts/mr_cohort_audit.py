"""
Arm 0 (extension) — Provenance & Quality Audit for the LEG cohort in
~/Downloads/mean-reversion-data  (deep TradingView exports: outright legs, not pre-made spreads).

Same constitution as cohort_provenance_audit.py: FOUNDATION HYGIENE ONLY — schema, date hygiene,
provenance, sample adequacy, price integrity. NO reversion/VR/OU/stationarity statistic, NO habitat
inference. Conservative defaults. These are LEGS we will construct spreads FROM (per the canonical
spread protocol), so disposition judges the LEG's trustworthiness, and a separate constructible-
spread map reports which causal spreads the available legs permit.

Outputs (reproducible): data/mr_cohort_manifest.json + .md
Run: backend/.venv/bin/python backend/scripts/mr_cohort_audit.py
"""
from __future__ import annotations
import json, glob, os, re
from collections import defaultdict
import numpy as np
import pandas as pd

SRC = os.path.expanduser("~/Downloads/mean-reversion-data")
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))

TRUSTED_BAR_FLOOR = 750
POWER_FLOOR       = 504

def parse_name(fname: str):
    """'COMEX_DL_GC1!, 1D (1).csv' -> (instrument='COMEX_DL_GC1!', tf='1D', dup=True)."""
    stem = fname[:-4]  # drop .csv
    m = re.match(r"^(.*),\s*([0-9]+|1D|1W)(\s*\((\d+)\))?$", stem)
    if not m:
        return stem, "?", False
    inst, tf, _, dup = m.groups()
    return inst.strip(), tf.strip(), bool(dup)

def classify(inst: str):
    s = inst.upper()
    is_fut = bool(re.search(r"[12]!$", s))
    leg = re.search(r"([A-Z]+)([12])!$", s)
    base, mon = (leg.group(1), leg.group(2)) if leg else (None, None)
    if s.startswith("TVC_"):                          typ = "composite_index"
    elif is_fut:                                      typ = "futures_continuous"
    elif s.startswith(("BSE_DLY_", "NSE_DLY_", "BATS_")): typ = "cash_equity"
    elif s.startswith(("OANDA_", "FX_IDC_")) or "USD" in s or "EUR" in s or "JPY" in s or "CHF" in s or "DXY" in s:
        typ = "fx"
    else:                                             typ = "broker_cfd_spot"
    deployment = typ in ("futures_continuous", "cash_equity") or any(
        k in s for k in ("COCOA","COFFEE","COTTON","WTI","BRENT","BRN","NATGAS","ZC","HG","PA","GC","SI","SOY"))
    return typ, base, mon, deployment

def audit(path: str):
    fname = os.path.basename(path)
    inst, tf, dup = parse_name(fname)
    typ, base, mon, deployment = classify(inst)
    df = pd.read_csv(path)
    close = pd.to_numeric(df.get("close"), errors="coerce")
    n = len(df)
    usable = int(close.notna().sum())
    neg = int((close < 0).sum())
    # flat O=H=L=C bars (composite annual-splice fingerprint)
    try:
        o,h,l,c = (pd.to_numeric(df[k],errors="coerce") for k in ("open","high","low","close"))
        flat = int(((o==h)&(h==l)&(l==c)).fillna(False).sum())
        broken = int(((h<l)|(h<o)|(h<c)|(l>o)|(l>c)).fillna(False).sum())
    except Exception:
        flat, broken = -1, -1
    # dates
    raw = df["time"].astype(str)
    dt = pd.to_datetime(raw, errors="coerce", utc=True, format="mixed")
    parse_fail = bool(dt.isna().mean() > 0.3)
    mono = bool(dt.dropna().is_monotonic_increasing)
    ds = dt.dropna().sort_values()
    span = f"{ds.iloc[0].date()}..{ds.iloc[-1].date()}" if len(ds) > 1 else None
    # composite splice detection: genuine-daily era = where spacing settles to <= ~7 days
    daily_era_start = None; usable_daily_bars = usable
    if typ == "composite_index" and len(ds) > 10:
        d = ds.diff().dt.days
        big = d > 7
        if big.any():
            last_big_idx = np.where(big.values)[0].max()
            daily_era_start = str(ds.iloc[min(last_big_idx+1, len(ds)-1)].date())
            usable_daily_bars = int((ds >= ds.iloc[min(last_big_idx+1, len(ds)-1)]).sum())
    return dict(file=fname, instrument=inst, tf=tf, duplicate=dup, type=typ, base=base, month=mon,
                deployment_domain=deployment, bars=n, usable_bars=usable, neg_close=neg,
                flat_ohlc=flat, broken_ohlc=broken, span=span, monotonic=mono, parse_fail=parse_fail,
                daily_era_start=daily_era_start, usable_daily_bars=usable_daily_bars)

def dispose(r):
    flags = []
    if r["type"] == "futures_continuous":
        flags.append("TradingView continuous (1!/2!) — verify roll/back-adjustment before differencing; "
                     "calendar legality requires 1!&2! aligned & same roll")
    if r["type"] == "composite_index":
        flags.append("TVC composite — spliced/synthetic; early history is low-frequency proxy "
                     f"(flat O=H=L=C bars={r['flat_ohlc']}); usable only from daily-era start "
                     f"{r['daily_era_start']} (~{r['usable_daily_bars']} genuine-daily bars)")
    if r["duplicate"]: flags.append("duplicate export ((n)) — dedupe")
    if r["neg_close"] > 0: flags.append(f"{r['neg_close']} negative closes — level-diff math")
    if not r["monotonic"]: flags.append("non-monotone dates — re-sort")
    # disposition (legs)
    if r["usable_bars"] == 0 or r["parse_fail"]:
        return "UNUSABLE", "HIGH", "unrecoverable (no close / unparseable dates)", flags
    eff = r["usable_daily_bars"] if r["type"] == "composite_index" else r["usable_bars"]
    if r["tf"] == "1D" and eff < POWER_FLOOR:
        return "UNUSABLE", "HIGH", f"genuine-daily bars {eff} < power floor {POWER_FLOOR}", flags
    if r["type"] == "composite_index":
        return "PROVISIONAL", "MEDIUM", f"composite: trim to daily era ({r['daily_era_start']}, {eff} bars) before use", flags
    if r["duplicate"] or not r["monotonic"]:
        return "PROVISIONAL", "MEDIUM", "fixable hygiene (dedupe/re-sort); usable after fix", flags
    if r["tf"] == "1D" and r["usable_bars"] < TRUSTED_BAR_FLOOR:
        return "PROVISIONAL", "MEDIUM", f"daily bars {r['usable_bars']} in [{POWER_FLOOR},{TRUSTED_BAR_FLOOR}): below TRUSTED floor", flags
    # intraday: judged on raw bars vs floors (note: not daily-equivalent)
    if r["tf"] != "1D" and r["usable_bars"] < POWER_FLOOR:
        return "UNUSABLE", "HIGH", f"bars {r['usable_bars']} < {POWER_FLOOR}", flags
    return "TRUSTED", "HIGH", f"real {r['type']} leg, {r['usable_bars']} bars, monotone, clean OHLC", flags

# --- constructible-spread catalog (checked against available TRUSTED/PROVISIONAL daily legs) ---
SPREADS = [
    ("USD/INR calendar",      "calendar β=1",       ["CME_MINI_DL_MIR1!","CME_MINI_DL_MIR2!"], "cleanest causal spread at depth (same contract, adjacent months)"),
    ("HDFC–ICICI pair",       "pair, rolling β",    ["BSE_DLY_HDFCBANK","BSE_DLY_ICICIBANK"],  "canonical MR habitat; deep real cash legs; lagged rolling β"),
    ("Gold–Silver",           "intercommodity, β",  ["COMEX_DL_GC2!","COMEX_DL_SI2!"],         "metals substitution; both 2nd-month continuous"),
    ("Gold–Copper",           "intercommodity, β",  ["COMEX_DL_GC2!","COMEX_DL_HG1!"],         "macro vs industrial metal"),
    ("Platinum–Palladium",    "intercommodity, β",  ["TVC_PLATINUM","NYMEX_DL_PA1!"],          "PGM substitution; platinum is TVC composite (trim)"),
    ("WTI–Brent",             "intercommodity, β",  ["CFI_WTI","ICEEUR_DLY_BRN1!"],            "KNOWN ~2010 structural break; mixed sources/sessions"),
    ("TCS–INFY (IT pair)",    "pair, rolling β",    ["BSE_DLY_TCS","NSE_DLY_INFY"],            "Indian IT cointegration candidate; cross-venue BSE/NSE"),
]

def main():
    paths = sorted(glob.glob(os.path.join(SRC, "*.csv")))
    recs = [audit(p) for p in paths]
    for r in recs:
        r["disposition"], r["confidence"], r["reason"], r["flags"] = dispose(r)

    daily = {r["instrument"]: r for r in recs if r["tf"] == "1D"}
    def leg_ok(sym):
        r = daily.get(sym)
        return r is not None and r["disposition"] in ("TRUSTED", "PROVISIONAL")
    def leg_depth(sym):
        r = daily.get(sym)
        return (r["usable_daily_bars"] if r and r["type"]=="composite_index" else (r["usable_bars"] if r else 0))
    spread_map = []
    for name, method, legs, note in SPREADS:
        ok = all(leg_ok(s) for s in legs)
        depth = min((leg_depth(s) for s in legs), default=0)
        spread_map.append(dict(name=name, method=method, legs=legs, constructible=ok,
                               min_daily_bars=depth, note=note,
                               missing=[s for s in legs if not leg_ok(s)]))

    counts = {d: sum(1 for r in recs if r["disposition"] == d) for d in ("TRUSTED","PROVISIONAL","CONTAMINATED","UNUSABLE")}
    summary = dict(generated="2026-06-03", source=SRC, n_files=len(recs), counts=counts,
                   constructible_spreads=[s for s in spread_map if s["constructible"]],
                   blocked_spreads=[s for s in spread_map if not s["constructible"]])
    with open(os.path.join(OUT, "mr_cohort_manifest.json"), "w") as f:
        json.dump(dict(summary=summary, spread_map=spread_map, instruments=recs), f, indent=2)

    L = ["# MR Cohort — Provenance & Quality Manifest (deep leg cohort)\n",
         "**Generated:** 2026-06-03 · **Source:** `~/Downloads/mean-reversion-data` · **Pre-reg:** doc 12 §7 (Arm 0 extension)",
         "**Scope:** foundation hygiene ONLY (schema/dates/provenance/depth/price-integrity). No reversion/VR/OU statistic. Conservative defaults.",
         f"**Floors:** TRUSTED ≥ {TRUSTED_BAR_FLOOR} daily bars · UNUSABLE < {POWER_FLOOR}. These are LEGS; spread trust depends on construction (canonical spread protocol).\n",
         f"**Dispositions (all timeframes):** TRUSTED {counts['TRUSTED']} · PROVISIONAL {counts['PROVISIONAL']} · UNUSABLE {counts['UNUSABLE']}\n",
         "## Constructible causal spreads (legs available at daily depth)",
         "| spread | method | min daily bars | constructible | note |",
         "|---|---|--:|:--:|---|"]
    for s in spread_map:
        L.append(f"| {s['name']} | {s['method']} | {s['min_daily_bars']} | {'✓' if s['constructible'] else '✗ '+','.join(s['missing'])} | {s['note']} |")
    L.append("\n## Daily legs by disposition")
    order = {"TRUSTED":0,"PROVISIONAL":1,"UNUSABLE":2,"CONTAMINATED":3}
    for r in sorted([r for r in recs if r["tf"]=="1D"], key=lambda x:(order[x["disposition"]], -x["usable_bars"])):
        eff = f" (daily-era {r['daily_era_start']}, {r['usable_daily_bars']}b)" if r["type"]=="composite_index" else ""
        L.append(f"- **`{r['instrument']}`** [{r['type']}] — {r['disposition']} · {r['usable_bars']} bars · {r['span']}{eff}"
                 + (f"\n  - flags: {' | '.join(r['flags'])}" if r['flags'] else ""))
    L.append("\n## Intraday availability (60m/15m) — bars per instrument")
    intr = defaultdict(dict)
    for r in recs:
        if r["tf"] in ("60","15"): intr[r["instrument"]][r["tf"]] = r["usable_bars"]
    for inst in sorted(intr): L.append(f"- `{inst}`: " + ", ".join(f"{tf}m={n}" for tf,n in sorted(intr[inst].items())))
    L.append("\n## Provenance flags (binding for construction)")
    L.append("- **TVC composites** (SILVER/DXY/PLATINUM/US10Y): spliced; early history is annual/low-freq proxy (flat OHLC). Use ONLY from the detected daily-era start; never treat pre-daily-era bars as observations.")
    L.append("- **TradingView 1!/2! continuous**: verify roll & back-adjustment; build calendars only from aligned 1!&2! with identical roll; difference Open/Close (synchronized), never naive High/Low (§6).")
    L.append("- **WTI–Brent** has a documented ~2010 structural break — any cointegration must be post-2011 or break-aware.")
    L.append("- **Cross-venue legs** (BSE cash vs NSE cash; broker CFD vs ICE): session/holiday/timezone mismatch → inner-join on synchronized timestamps only.")
    L.append("- **Dedupe** the `(n)` files before use (BRN1! 15/60, EURUSD 15/60/1D).")
    with open(os.path.join(OUT, "mr_cohort_manifest.md"), "w") as f:
        f.write("\n".join(L) + "\n")

    print("files:", len(recs), "| dispositions:", counts)
    print("constructible spreads:", [s["name"] for s in spread_map if s["constructible"]])
    print("blocked:", [(s["name"], s["missing"]) for s in spread_map if not s["constructible"]])
    print("wrote data/mr_cohort_manifest.md + .json")

if __name__ == "__main__":
    main()
