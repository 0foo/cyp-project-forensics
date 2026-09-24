# Transposons the 3 kb window rule discards

> **Not lab material.** Everything in this directory was produced on 2026-09-24
> during the forensic investigation. It is kept under `reconstructed/` so it can never be
> mistaken for something the lab made. The lab's own files were read only, and nothing
> outside this directory was written to.

This is the supporting data for defect **D3** in
[`../../../docs/pipeline/detailed/04-gaps-and-provenance.md`](../../../docs/pipeline/detailed/04-gaps-and-provenance.md):
the lab's `Locate_TE.py` requires a repeat to lie *entirely* inside a gene's ±3 kb window, so
an element that reaches into the window but extends past its edge is discarded no matter how
close to the gene it begins.

| | |
|---|---|
| `find_missed_transposons.py` | The analysis, re-runnable |
| `missed_transposons.tsv` | Every association the rule discards, for the three species whose inputs survive |

---

## The rule

`evidence/te-locating-run/Locate_TE.py:31-37`:

```python
start = int(cypFields[3]) - 3000
stop  = int(cypFields[4]) + 3000
if cypFields[0] == eleFields[4] and (int(eleFields[6]) <= stop and int(eleFields[5]) >= start):
```

`eleFields[5]` and `[6]` are the repeat's query begin and end. Both are tested against the
window, so the condition is `te_end <= stop AND te_start >= start` — **containment**. A
standard overlap test would be `te_start <= stop AND te_end >= start`, with the comparisons
the other way round.

All three surviving copies of the script are identical here
(`te-locating-run/Locate_TE.py`, `lab-scripts/te-locating/Locate_TE.py`,
`lab-scripts/te-locating/Step2FindTEs.py`).

## What was measured

Three species have both a RepeatMasker `.out` and a usable annotation in the archive. For
each, the script reproduces `repeatOpp.py`'s gene filter (including its one-row-per-matching-
symbol duplication), then applies both the lab's test and a standard overlap test.

**Validation:** on *D. ananassae* the lab's test reproduces the archived
`GenesAffectedByTEs.txt` row count — 900 — exactly, so the rule is faithfully reproduced
before anything is concluded from it.

| Species | Gene rows | Kept (lab's rule) | Would overlap | Associations lost | Distinct elements |
|---|---|---|---|---|---|
| *D. ananassae* | 166 | **900** ✓ | 930 | 30 | 19 |
| *D. sechellia* | 131 | 457 | 468 | 11 | 7 |
| *D. simulans* | 121 | 504 | 521 | 17 | 12 |

## The loss is not random — it scales with element length

Measured on *D. ananassae*, over every repeat that touches a window at all:

| Element length | Kept | Dropped | % dropped |
|---|---|---|---|
| <200 bp | 787 | 11 | 1.4% |
| 200–999 bp | 82 | 3 | 3.5% |
| 1–5 kb | 29 | 11 | 27.5% |
| **≥5 kb** | **2** | **5** | **71.4%** |

Short repeats almost always fit inside a window; long ones almost never do. Since the kept
set is 69% `Simple_repeat` and `Low_complexity`, the rule quietly trades away the long
elements — the ones plausibly capable of carrying regulatory sequence — while retaining the
microsatellites.

**25 of the 38 lost associations are in the upstream flank**, the promoter side, which is
where an insertion is most likely to change expression.

## The elements being missed

Twelve of the 38 are at least 1 kb and classified as a real repeat family. "Gap" is how close
the element gets to the gene itself.

| Species | Cyp gene | Element | Class | bp | Divergence | Gap to gene |
|---|---|---|---|---|---|---|
| simulans | Cyp6d4 | ltr-1_family-49 | LTR/Gypsy | 7,410 | 0.1% | 1,598 bp |
| ananassae | Cyp313a5/a2/a3/a1 | ltr-1_family-11 | LTR/Pao | 6,339 | 0.5% | 1,446 bp |
| simulans | Cyp6d2 | rnd-1_family-184 | LINE/I | 5,280 | 0.6% | 2,748 bp |
| **simulans** | **Cyp6g1** | rnd-1_family-151 | LINE/I-Jockey | 4,321 | 3.9% | **650 bp** |
| ananassae | Cyp4g15 | rnd-1_family-490 | Unknown | 2,148 | 24.5% | 2,605 bp |
| **ananassae** | **Cyp6g1** | rnd-4_family-78 | DNA/hAT-Ac | 2,129 | 24.9% | 1,245 bp |
| ananassae | Cyp311a1 | rnd-1_family-490 | Unknown | 1,896 | 23.6% | 1,772 bp |
| ananassae | Cyp309a1/a2 | rnd-1_family-520 | RC/Helentron | 1,793 | 2.0% | 2,987 bp |
| ananassae | Cyp313b1 | rnd-1_family-575 | Unknown | 1,330 | 20.9% | 2,831 bp |
| ananassae | Cyp6v1 | rnd-1_family-490 | Unknown | 1,240 | 21.5% | 2,174 bp |
| ananassae | Cyp6a13 | rnd-1_family-490 | Unknown | 1,217 | 23.1% | 2,688 bp |
| ananassae | Cyp9b1/b2 | rnd-1_family-25 | LINE/CR1 | 1,150 | 1.6% | 2,773 bp |

22 Cyp genes are affected across the three species: Cyp18a1, Cyp28c1, Cyp309a1/a2, Cyp311a1,
Cyp313a1–a5, Cyp313b1, Cyp318a1, Cyp4c3, Cyp4d1, Cyp4d8, Cyp4g15, Cyp4p1/p2/p3, Cyp6a13,
Cyp6a19, Cyp6a2, Cyp6d2, Cyp6d4, Cyp6d5, **Cyp6g1**, Cyp6t1, Cyp6v1, Cyp9b1/b2.

## Why this matters more than the counts suggest

**Cyp6g1 is affected in two of the three species that could be tested**, and *Cyp6g1* is the
gene the entire study exists to generalise from — the *Accord* LTR insertion in its promoter
is the textbook case of a transposable element driving insecticide resistance.

- *D. simulans*: a **4,321 bp LINE/I-Jockey element at 3.9% divergence** — young, so recently
  active — ends **650 bp upstream of Cyp6g1**, squarely in the promoter. It is discarded
  because its far end sits 1,970 bp outside the window.
- *D. ananassae*: a **2,129 bp DNA/hAT-Ac element** ends **1,245 bp upstream of Cyp6g1**.
  Discarded because its far end sits 373 bp outside the window.

*Accord* itself is roughly 7 kb. An element of that size in a promoter cannot satisfy a
containment test against a 3 kb flank unless the gene is long enough to swallow it. **The
pipeline is structurally unable to detect the very insertion that motivates it**, except by
accident.

## Caveats

- Only three species could be measured; the archive holds a RepeatMasker `.out` for no others.
  The 29 finished tables cover 29 species, so this is a sample, not a census.
- For *D. sechellia* and *D. simulans* the gene filter was re-derived from their full
  annotations, since no `filtered.gff` survives for them. Their absolute counts are therefore
  a reconstruction; only *D. ananassae*'s is validated against an archived output.
- Row counts include `repeatOpp.py`'s duplication, so "associations" exceeds "distinct
  elements" — both are reported.
- Being discarded is not the same as being biologically meaningful. These are candidates the
  rule removed from consideration without recording that it had done so; that is the finding,
  not that any particular element regulates any particular gene.

## Re-running it

```bash
cd evidence/reconstructed/window-rule-analysis
python3 find_missed_transposons.py
```

Standard library only, about a minute. It reads the lab's files read-only and rewrites only
`missed_transposons.tsv` beside itself.
