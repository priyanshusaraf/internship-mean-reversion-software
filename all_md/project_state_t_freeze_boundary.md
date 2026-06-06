---
name: state-t-freeze-boundary
description: The decisive test for whether a new scoring/classification layer crosses the frozen State T detection line
metadata:
  type: project
---

The legality test for any new scoring or classification observatory under the State T freeze
(observability ≠ detection, CLAUDE.md §10):

**Substrate character (LEGAL) vs episode timing (FROZEN).**
- Classifying *instrument character* — "what process does this market resemble: OU-like / trend / exhaustion-prone" — is slow, instrument-level, descriptive. This is the Layer-4 market taxonomy (doc 04 §2.5.1). Observatory-legal.
- Classifying *temporal episodes* — "is a reversion regime igniting NOW / about to" — is episode-level, hazard-flavored, forward-leaning. This IS State T detection (doc 04 §1.2.2: tradeable form is a hazard/probability; §1.3.1: discrete-time hazard). FROZEN.

**Soft plausibility scores do NOT launder a forbidden question.** A per-bar probability that "something is igniting" is State T detection regardless of being called a score. The score *semantics* (character vs timing) decide legality, not score-vs-hard-label.

**Trend etiology is NOT innocent substrate.** The dossier's trend-etiology classifier (why the *current* trend exists: flow/inventory vs info-repricing) is fast, conditional, episode-level (doc 04 §1.4.3), and is the deferred State-T *conditioning gate* (§2.6.4). A static "OU-like vs trend-like" read is safe; "this trend is flow-exhaustion-driven right now" is the etiology gate and is NOT v0-authorized.

**Forbidden engines (named in doc 04 §1.3.1 + CLAUDE.md §10):** HMM (rejected as wrong object — models T interior as zero-width jump), deep/sequence models (data-starved, kill interpretability), RL. Taxonomy must be feature-threshold/ratio based, not latent-state.

**Why:** A 2026-06-02 audit of a proposed Market Taxonomy / Substrate Classification observatory (post-MRScore-v1). Ruled CONSISTENT-WITH-GUARDRAILS.
**How to apply:** Run this test on any future "score/classify market state" proposal before authorizing. If it answers "is T happening / igniting," stop. See [[mrscore-observatory-precedent]] for the structural template a legal version must mirror.
