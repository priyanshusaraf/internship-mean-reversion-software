/**
 * Centered moving average — a *retrospective reference* smoother.
 *
 * value[i] averages bars [i-halfWidth .. i+halfWidth], so for any bar it USES FUTURE
 * BARS relative to that bar. It is therefore future-using and is NOT ground truth /
 * NOT "true equilibrium" — it is a retrospective reference equilibrium proxy only.
 *
 * Edge bars (within `halfWidth` of either end) have reduced support; callers that
 * require full ±halfWidth support (e.g. the LAG decomposition) MUST mask them.
 * REP uses the edge-shrunk values intentionally for its live hindsight overlay.
 *
 * Computed client-side over already-fetched prices — no backend, no causal recompute.
 */
export function centeredMA(values: number[], halfWidth: number): number[] {
  const n = values.length;
  const out = new Array<number>(n).fill(NaN);
  for (let i = 0; i < n; i++) {
    const lo = Math.max(0, i - halfWidth);
    const hi = Math.min(n - 1, i + halfWidth);
    let s = 0;
    for (let j = lo; j <= hi; j++) s += values[j];
    out[i] = s / (hi - lo + 1);
  }
  return out;
}
