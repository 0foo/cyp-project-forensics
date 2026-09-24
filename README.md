# cyp-project-forensics

**This repository is a forensic investigation, not a pipeline.**

A research group — the Atallah lab — spent 2025 and 2026 building a chain of scripts to ask
whether *Drosophila* species that get sprayed with insecticide carry more transposable
elements in and around their cytochrome P450 (Cyp) genes. The work produced real results.
It was never documented, never version-controlled, ran on at least three different people's
Windows machines, and was handed between them over OneDrive. By the time this repository was
started, what survived was a pile of loose Python files with hardcoded `C:/Users/User/…`
paths, some finished output tables, a 7-Zip archive or two, and seventeen phone photographs
of lab notebooks and File Explorer windows.

This repository exists to work out what that chain of scripts actually did, and to write it
down while the evidence still exists.

It is not a place to run the pipeline, fix it, or extend it.

---

## The two standing rules

**1. The lab's files are forensic artifacts.** Nothing under `evidence/` is ever modified,
fixed, regenerated or tidied — not even an obvious typo, not even a script that plainly does
not run. When something needs to be executed to test a hypothesis, a copy is made outside
the repository, only paths are changed in the copy, and output is written outside the
repository too. Defects are recorded as findings, never patched.

**2. Every claim carries its provenance.** Documentation here distinguishes what was read
out of the lab's code, what was measured from the lab's data, what was transcribed from a
photograph, what was reproduced by re-running something, and what is inference. Where a
statement is inferred, it says so.

## What has been established

The short version, with the details behind each link:

- **The full chain that produced the `change_<SPECIES>_final_final.gff` files is
  reconstructed and verified.** OrthoFinder → a HOG/orthogroup table → `ReVamp_Final.py` →
  renamed annotations. Re-running the step on *D. arizonae* reproduces the lab's own output
  line for line. See [`docs/scripts/06-final-final-gff.md`](docs/scripts/06-final-final-gff.md).
- **Two different people wrote two different gene-renaming scripts, and the finished
  per-species tables are a mix of both.** 19 species went through Duy's `ReVamp_Final.py`,
  7 through Ayush's `NEW_Step_5_…`, and the two do not agree: ReVamp silently drops about 7%
  of orthologous genes. Cross-species comparisons therefore compare tables built two
  different ways.
- **Most of what the pipeline calls a transposable element is not one.** Measured across all
  27 finished species tables: **70.1% of 21,409 rows are definitively not TEs** — 61.8% is
  `Simple_repeat`, median length 39 bp — and only 16.8% is a classified transposon. The
  contamination is not uniform (36.9% to 90.2% by species), so it biases rather than adding
  noise, and **52% of the genes counted as "has a TE nearby" have no genuine transposon near
  them** — their entry rests entirely on microsatellite hits. Nothing in the pipeline ever
  reads the repeat class. See
  [`evidence/reconstructed/repeat-class-analysis/`](evidence/reconstructed/repeat-class-analysis/).
- **The TE-to-gene rule discards the study's own motivating case.** A transposon must fit
  *entirely* inside a gene's ±3 kb window to be counted, so 71% of elements ≥5 kb that reach a
  window are thrown away — including long elements sitting in the *Cyp6g1* promoter in two
  separate species. *Cyp6g1* and its ~7 kb *Accord* insertion are the reason the project
  exists. The discarded elements are listed in
  [`evidence/reconstructed/window-rule-analysis/`](evidence/reconstructed/window-rule-analysis/).
- **Some of it is unrecoverable.** The `config.py` that drove the orthogroup steps, the
  original `Dmel_output.tsv`, a fourth page of the lab log listing per-species family counts:
  gone, and recorded as gone.

## How this repository is laid out

```
README.md        you are here
CLAUDE.md        a session-by-session record of how the investigation itself was conducted

docs/            the investigation's findings
  pipeline/        what the pipeline did, as a whole — simple tier and detailed tier
  scripts/         individual scripts, read line by line, with their defects
  diagrams/        flow charts
  ocr/             transcriptions of the seventeen archive photographs
  superseded/      earlier reconstructions, kept because they are part of the record
  commands.md      every command the lab ran, and every command run to verify it

evidence/        the artifacts themselves — read-only, never edited
  lab-scripts/     the lab's Python and shell, grouped by what it does
  lab-data/        HOG tables, renamed annotations, TE tables, gene lists, RepeatMasker output
  lab-archives/    the original 7-Zip archives, as received
  lab-environment/ shell history and directory listings from the lab's machines
  te-locating-run/ one species worked end to end, plus 29 finished species tables
  analysis-scripts/the downstream analysis code, as it arrived over OneDrive
  photographs/     the seventeen source images
  reconstructed/   files produced during this investigation — NOT lab originals
```

`evidence/README.md` is the manifest: what each artifact is, where it came from, and where
it sat before this repository reorganised it.

## Where to start

| If you want | Read |
|---|---|
| The shortest honest summary of the pipeline | [`docs/pipeline/simple/01-what-it-does.md`](docs/pipeline/simple/01-what-it-does.md) |
| What is broken and what is missing | [`docs/pipeline/detailed/04-gaps-and-provenance.md`](docs/pipeline/detailed/04-gaps-and-provenance.md) |
| The single deepest piece of the investigation | [`docs/scripts/06-final-final-gff.md`](docs/scripts/06-final-final-gff.md) |
| What physically exists and where it came from | [`evidence/README.md`](evidence/README.md) |
| Primary sources | [`docs/ocr/`](docs/ocr/) |

## Related repositories

This is deliberately not the only repository involved, and it helps to know which is which.

| Repository | What it holds |
|---|---|
| **`cyp-project-forensics`** (this one) | The investigation: evidence and findings |
| `cyp-te-pipeline` | The "happy path" — a clean, runnable version of the pipeline, built from what was learned here. **Anything about running the pipeline belongs there, not here.** |
| `repeat-modeler-automation` | The RepeatModeler/RepeatMasker worker automation, split out of this repository in September 2026. Some documentation here still describes it, because the lab's stage 1 and 2 are what it replaced |

There is also a `cyp-old-data` working directory (not published) holding the 13 GB
*D. melanogaster* `final_final` file, which is too large to commit and is itself an open
question — see [`docs/pipeline/detailed/04-gaps-and-provenance.md`](docs/pipeline/detailed/04-gaps-and-provenance.md).
