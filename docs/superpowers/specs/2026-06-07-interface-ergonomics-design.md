# Interface Ergonomics + Global Instrument Sync — Design Spec

**Date:** 2026-06-07
**Status:** Approved (brainstorm) — pending spec review → implementation plan
**Scope class:** Interface / UX only. Touches no frozen analytics engine, no temporal firewall, no research conclusion.

---

## 0. Motivation

Operator-reported friction with the workstation UI:

1. Backtest price chart is non-interactive — can't zoom into a value; the scrubber is the only control.
2. Font/text contrast is too low to read comfortably; operator wants to choose the text color.
3. Chart/data panels are rigid frames; operator wants them adjustable.
4. Instrument selection is siloed per view; operator wants picking an instrument *anywhere* to update *everywhere*, unless a view is explicitly held constant.
5. (Answered inline, not a build item) Observatory's purpose was unclear — it is the raw-data → causal-understanding → habitat-scoring entry point that precedes backtesting.

## 1. Constitutional framing

This is pure interface work. The **one invariant in the blast radius is the causal firewall** (§6.1): as-of clamps the analysis-window end and future bars render greyed. It is **preserved** because the new chart zoom is view-only magnification of already-causal bars — zoom neither reveals nor computes anything beyond as-of. No change to: frozen Kalman μ\* engine, habitat scorer, deseasonalizer, surrogate machinery, or any research verdict.

**Build ownership:** implementation routes through `frontend-architect` (sole UI + integration owner) with `backend-api` for the §4b endpoint shim. This document is the spec only.

---

## 2. Feature 1 — Interactive zoom + scrubber-as-minimap

### Current behavior
- `PricePane` (backtest), observatory `PriceChart`, and `ChartWorkspace` set `handleScroll: false`, `handleScale: false`. Charts are display-only.
- `TimelineScrubber` (backtest) owns the **analysis window** via two drag handles; on release it commits the window to the store and triggers a habitat/causal recompute.
- The scrubber's window is a *computation input*, not merely a view — this is the semantic the redesign must protect.

### Target behavior (operator decision: "zoom = view only, scrubber reflects it")
- Charts become freely zoomable/pannable (`handleScroll: true`, `handleScale: true`).
- A **new viewport-band layer** is added to `TimelineScrubber`, visually distinct from the two analysis-window handles. It reflects the chart's current visible range.
- **Bidirectional sync:**
  - Chart pan/zoom → `timeScale().subscribeVisibleLogicalRangeChange` fires → map visible logical (bar-index) range to dates → update the viewport band.
  - Dragging the viewport band → map band date-range to a logical range → `timeScale().setVisibleLogicalRange(...)` to pan/zoom the chart.
- **Decoupling guarantee:** zoom/pan and the viewport band **never** trigger a habitat/causal recompute. Only the analysis-window handles do, exactly as today. View state and computed-window state are separate.
- **Fit/reset button**: re-`fitContent()` to frame the full causal series.

### Key technical notes
- lightweight-charts addresses time in **logical (bar index)** units for visible-range APIs; the scrubber addresses time in **dates/indices into the bar array**. Conversion goes through the bars' time array (index ↔ time) — already available to both components.
- Observatory's `PriceChart` already cross-syncs its price and z subpanes via `subscribeVisibleLogicalRangeChange`; the viewport-band wiring composes with that existing sync.
- Two distinct state objects per chart view: `viewportRange` (free, view-only) and `analysisWindow` (committed, drives compute). They must not be conflated in code.

### Acceptance
- Mouse wheel / pinch zooms the chart; drag pans it; the scrubber band tracks live.
- Dragging the band pans/zooms the chart.
- Zooming produces **zero** network calls to habitat/equilibrium.
- Moving an analysis-window handle still recomputes (unchanged).
- Future (post as-of) bars stay greyed under all zoom levels — firewall intact.

---

## 3. Feature 2 — Readable fonts + user-chosen text color

### Current behavior
- Palette `C` in `components/observatory/ui.tsx` hardcodes text tokens: `text: #3d4d5e` (very dim), `textBright: #8fa3b8`, `textDim: #2d3a4a`.
- Some components bypass `C` and hardcode text hexes inline.
- Only `fontScale` is user-adjustable (UIStore → `--amr-scale` CSS var → `.font-data-scaled`), persisted in `amr-ui-v1`.

### Target behavior (operator decision: "brighten defaults + custom color picker")
- Convert the **three text tokens** in `C` from literal hex → `var(--amr-text)`, `var(--amr-text-bright)`, `var(--amr-text-dim)`.
- Define those vars in `globals.css :root` with **brightened defaults** (readable out of the box, even with no setting touched). Non-text tokens (accent/warn/danger/good/bg/border) stay literal.
- Settings ▸ Appearance gains a **text-color control**: presets (dim / normal / bright) + custom hex picker. Writing it sets the CSS vars at the document root, mirroring the existing `--amr-scale` plumbing in `AppNav`. Persisted in `amr-ui-v1` (UIStore slice).
- **Sweep:** components that hardcode text hexes directly must be migrated onto the tokens or they won't respond to the setting. This sweep is the bulk of the effort here.

### Default brightening (provisional, tune during build)
```
--amr-text         #3d4d5e → ~#8b9bb0
--amr-text-bright  #8fa3b8 → ~#c2d0de
--amr-text-dim     #2d3a4a → ~#5e6f80
```

### Acceptance
- With no setting changed, baseline text is comfortably readable on the dark background.
- Settings color picker / presets change primary text color live and persist across reload.
- No hardcoded text hex remains in the hot paths (grep clean for the migrated tokens).
- Numeric/data colors and semantic colors (warn/danger/good) unaffected.

---

## 4. Feature 3 — Resizable panels (all pages)

### Current behavior
- Workstation uses a **custom** `DragHandle` (mouse events) for left/right panel widths + chart split.
- Backtest is a **rigid** 4-quadrant grid (inline-style fixed percentages: Q1 Price 55×62, Q3 PnL 45×62, Q2 Scrubber 55×38, Q4 Habitat 45×38).
- Workbench and Observatory use fixed-width flex columns.

### Target behavior (operator decision: "all pages, proper resizer library")
- Adopt **`react-resizable-panels`** (small, React-native, consistent with frozen-stack spirit — a thin UI lib, not infra).
- Migrate all four layouts to `PanelGroup` / `Panel` / `PanelResizeHandle`:
  - **Workstation:** replace custom DragHandles with horizontal PanelGroup (left | center | right); nested vertical group for the center chart/research split.
  - **Backtest:** horizontal PanelGroup of two vertical PanelGroups → Price/Scrubber on the left column, PnL/Habitat on the right; every divider draggable.
  - **Workbench / Observatory:** column PanelGroups for their fixed-width sidebars.
- Persist sizes via the library's `autoSaveId` (own localStorage key per page) — a UI pref, owned by `frontend-architect`.
- Charts reflow automatically: `PricePane`, `PriceChart`, `ChartWorkspace`, equity chart already use ResizeObservers.

### Acceptance
- Every page's panel dividers are draggable; sizes persist across reload.
- Charts resize cleanly (no clipping/overflow) at any panel size.
- No layout regression on initial load (sensible default sizes match current layout).

---

## 5. Feature 4 — Global instrument sync + per-view pin

### Current behavior
- `selectedInstrumentId` already lives in global `useWorkstationStore` (persisted: instrument id only).
- Workstation has the only instrument selector; Backtest and Workbench read the global and refetch on change. Observatory is orthogonal (CSV dataset, no instrument selector).

### Target behavior (operator decision: "sync on by default, per-view pin, include Observatory")
- Add a **compact instrument selector** to each view header (Backtest, Workbench, Observatory) that calls `selectInstrument(id)` → propagates to all unpinned views.
- Add a `pinned` map to the UI store: `{ workstation?, backtest?, workbench?, observatory? }`. Each view computes `effectiveInstrument = pinned[view] ?? selectedInstrumentId`.
- A **pin toggle** in each view header locks that view to its current instrument (captures current `effective` into `pinned[view]`) and makes it ignore subsequent global changes. Unpin clears it and re-joins the sync. This is the "keep chart constant" control.

### Acceptance
- Selecting an instrument in any unpinned view updates all other unpinned views.
- Pinning a view freezes its instrument while others continue syncing.
- Unpinning re-syncs to the current global selection.
- Selection + pin state persist across reload.

---

## 6. Feature 4b — Observatory participation (bridge)

### Key finding
Instruments (market-loaded) and CSV datasets share the **same DuckDB tables** (`instruments`, `ohlcv`), keyed by the **same identifier** (filename stem, uppercased). Observatory's `_get_full(conn, dataset_id)` checks membership against the instruments table — so a `selectedInstrumentId` is *already a valid `dataset_id`* for series/equilibrium/habitat.

### The one wrinkle
CSV-ingested datasets carry `v2_dataset_meta` and pass `_reject_inadmissible`; **market-loaded instruments may lack that metadata** and could be rejected.

### Target behavior + backend shim (`backend-api`)
- When Observatory is unpinned and a global instrument is selected, drive its series/equilibrium/habitat with `dataset_id = effectiveInstrument`.
- Backend (thin, no engine touch): ensure a market-loaded instrument passes admissibility — **either** backfill a minimal `v2_dataset_meta` row on load, **or** add an `…-by-instrument` adapter that constructs the request and short-circuits the inadmissibility check for known instruments. One validation test: habitat + equilibrium return successfully for a market-loaded instrument id.
- **Fallback (required):** if the selected instrument has no usable v2 series, Observatory shows a clear empty-state ("ingest a CSV for this instrument, or pick another") — it must never error/break.

### Acceptance
- Selecting an instrument (unpinned Observatory) loads its series + μ\* + habitat without a manual CSV upload.
- An instrument with no usable series shows the fallback state, not an error.
- Engines (`habitat_score_full`, `compute_kalman_mu_star`, deseasonalizer) are byte-for-byte unchanged.

---

## 7. Phasing (for the implementation plan)

| Phase | Content | Rationale |
|-------|---------|-----------|
| **P1** | Feature 2 — font brighten + color picker | Fast, isolated readability win |
| **P2** | Feature 3 — resizable panels (all pages) | Structural; precedes chart-interaction work |
| **P3** | Feature 1 — zoom + scrubber minimap | Most intricate; benefits from settled layout |
| **P4** | Feature 4 + 4b — global sync, pin, Observatory bridge | Cross-cutting + the only backend touch |

Each phase independently shippable and rigor-QA gated, matching the Observatory v2 build cadence.

---

## 8. Out of scope (YAGNI)

- No new charting library; stay on lightweight-charts.
- No theme engine beyond the three text-color CSS vars + existing font-scale (semantic colors stay fixed).
- No instrument→dataset *creation* pipeline; 4b reuses the shared DuckDB key, not a new ingest path.
- No change to backtest math, signal logic, or any research artifact.

## 9. Risks

- **R1 (P3):** logical-range ↔ date conversion edge cases (sparse/holiday gaps) could make the viewport band drift. Mitigation: convert via the actual bar time array, not assumed uniform spacing.
- **R2 (P2):** missed hardcoded text hexes leave dim patches. Mitigation: grep sweep + visual pass per page.
- **R3 (P4b):** admissibility rejection for market instruments. Mitigation: the shim + validation test above; fallback empty-state guarantees no breakage.
- **R4 (P2):** custom hex could produce unreadable combos. Mitigation: presets are the default path; custom is advanced.
