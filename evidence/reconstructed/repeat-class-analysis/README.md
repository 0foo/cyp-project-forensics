# What fraction of the pipeline's "TE burden" is not a transposable element

> **Not lab material.** Produced on 2026-09-24 during the forensic investigation and kept
> under `reconstructed/` so it can never be mistaken for something the lab made. The lab's
> files were read only; nothing outside this directory was written to.

Supporting data for defect **D1** in
[`../../../docs/pipeline/detailed/04-gaps-and-provenance.md`](../../../docs/pipeline/detailed/04-gaps-and-provenance.md).

RepeatMasker is a *repeat* finder, not a TE finder. It reports microsatellites, AT-rich
stretches and satellite DNA alongside genuine transposable elements. **Nothing anywhere in the
pipeline filters on repeat class**: `Locate_TE.py` keeps every hit in the window,
`build_tfbs_te_gff.py` records the class faithfully as `repeat_class=` and then never reads it
again, and none of the three comparison scripts mentions it. So every count the study reports
as "TE burden" includes all of it.

| | |
|---|---|
| `measure_repeat_classes.py` | The analysis, re-runnable |
| `repeat_class_by_species.tsv` | Per-species composition, row and base-pair counts |

Measured across **all 27 non-empty finished tables** in
`evidence/te-locating-run/AnalysisForAll/output/` — 21,409 TE-hit rows. Two of the 29 tables
are empty files.

---

## The headline number

| Category | Rows | % of rows | Base pairs | % of bp | Median length |
|---|---|---|---|---|---|
| **Not a transposable element** | 15,018 | **70.1%** | 680,559 | 30.2% | 39 bp |
| Unclassified (`Unknown`) | 2,790 | 13.0% | 769,863 | 34.1% | 126 bp |
| Genuine transposable element | 3,601 | **16.8%** | 805,429 | 35.7% | 122 bp |

**70.1% of what this pipeline calls a TE is definitively not one.** Only 16.8% is a
classified transposable element.

The "not a TE" bucket is `Simple_repeat`, `Low_complexity`, `Satellite` and RepeatMasker's
RNA classes — categories that are not transposons by definition, not borderline calls.
`Simple_repeat` alone is **61.8%** of every row in the study: things like `(AAT)n` and
`(CA)n`, with a median length of **39 bp**.

`Unknown` is kept separate deliberately. In a *de novo* RepeatModeler library these are
usually genuine repeat families that the classifier could not name, and many are probably
real TEs — so treating them as junk would overstate the case. Counting them as TEs still
leaves only 29.9% of rows that could possibly be transposons; counting them as junk gives
83.2% not confirmed as TEs. The honest range is **70–83%**.

### Commonest classes

| Rows | % | Class | |
|---|---|---|---|
| 13,232 | 61.8% | `Simple_repeat` | not a TE |
| 2,790 | 13.0% | `Unknown` | unclassified |
| 1,763 | 8.2% | `Low_complexity` | not a TE |
| 1,177 | 5.5% | `RC/Helentron` | TE |
| 738 | 3.4% | `LTR/Gypsy` | TE |
| 323 | 1.5% | `LTR/Pao` | TE |
| 140 | 0.7% | `DNA/CMC-Transib` | TE |
| 116 | 0.5% | `RC/Helitron` | TE |

No genuine TE class reaches 6% of the data. The study's signal, if it has one, is carried by
the bottom fifth of its own table.

---

## It is bias, not noise

The documentation previously reasoned that if simple-repeat density were uniform across
species this would add noise rather than bias. **It is not uniform.**

| | |
|---|---|
| Lowest junk fraction | *D. suzukii*, **36.9%** |
| Highest junk fraction | *D. anomalata*, **90.2%** |
| Spread | **53.3 percentage points** |
| Mean / standard deviation | 71.7% / **12.6 points** |

A 53-point spread in the contaminant, across a comparison whose entire purpose is to detect a
difference in the thing being contaminated. Full per-species figures are in
`repeat_class_by_species.tsv`.

### It changes which species look TE-rich

Rank the 27 species by hits per Cyp gene as the pipeline measures it, then rank them again
counting only genuine transposable elements. The two orderings agree only weakly:

> **Spearman ρ = 0.597**

These are substantially different measurements, not the same measurement with noise on it.
The largest movements:

| Species | Rank as measured | Rank if filtered | Move |
|---|---|---|---|
| *D. mojavensis* | **1st** | 22nd | −21 |
| *D. erecta* | 22nd | 11th | +11 |
| ***D. suzukii*** | 12th | **1st** | **+11** |
| *D. aldrichi* | 4th | 13th | −9 |
| *D. mayaguana* | 9th | 18th | −9 |

The species the pipeline ranks **first** for TE burden, *D. mojavensis*, is 22nd of 27 once
junk is removed — 80.3% of its hits are not transposons. The species with the **most genuine
transposable elements per Cyp gene**, *D. suzukii*, is ranked 12th by the pipeline.

That matters because *D. suzukii* is the only species the archive ever names in an exposure
context: it appears as `exposure = high` in the config example in
`compare_te_cyp_exposure 1 1.py:586-588` and in the analysis README. The real config is one of
the files that did not survive (see G3), so the actual grouping is unknown and nothing here
should be read as a result about exposure. But the one species named as the high-exposure
exemplar is exactly the one whose real TE signal this metric suppresses.

### And it compresses the real differences

| Hits per Cyp gene | Lowest | Highest | Fold range |
|---|---|---|---|
| As measured (all repeats) | 6.2 | 27.7 | 4.4× |
| Genuine TEs only | 0.76 | 7.6 | **10.1×** |

Because junk is roughly a floor under every species, it compresses the between-species spread
by a factor of **2.3**. The pipeline is measuring a quantity with less dynamic range than the
one the study is about, in a design already short of statistical power.

---

## Effect on the statistics that were actually run

Fisher's exact test operates on a presence/absence table: does this Cyp gene have at least one
TE nearby, yes or no. That table is built from these rows.

| | |
|---|---|
| Gene/species pairs with ≥1 recorded hit | **1,423** |
| ... that still have one once non-TEs are removed | **683** |
| Would flip to "no TE" | **740 — 52.0%** |

**More than half the genes currently counted as "has a TE nearby" have no genuine transposable
element nearby at all** — their entry rests entirely on microsatellite and low-complexity
hits. (The full table also contains genes with no hits at all, which these tables do not
record; 52.0% is the fraction of the *positive* entries that would become negative, which is
the side of the table the test is sensitive to.) Every reported Fisher's exact result is
computed on a table that would be restructured by consulting a column the pipeline carries
from end to end and never reads.

The Mann-Whitney test on per-gene counts is affected the same way: the counts it ranks are, on
average, 70% microsatellite.

---

## Caveats

- Classification is RepeatMasker's own, taken at face value. `Simple_repeat`,
  `Low_complexity` and `Satellite` are not transposons by definition; that part is not a
  judgement call.
- `Unknown` is reported separately rather than assigned. Some are certainly real TEs.
- Row counts inherit `repeatOpp.py`'s duplication (defect D2), so absolute totals are inflated
  — but the duplication is applied to junk and real TEs alike, so the *proportions*, which are
  what this document is about, are unaffected.
- The 27 species were themselves produced by two different renaming scripts (G4); that affects
  which genes appear, not the repeat-class composition of the hits recorded against them.
- This measures what the pipeline recorded. It says nothing about whether the genuine TEs it
  did record are associated with exposure.

## Re-running it

```bash
cd evidence/reconstructed/repeat-class-analysis
python3 measure_repeat_classes.py
```

Standard library only, a few seconds. Reads the finished tables read-only and rewrites only
`repeat_class_by_species.tsv` beside itself.
