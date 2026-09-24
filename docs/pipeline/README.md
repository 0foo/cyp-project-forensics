# Pipeline documentation

This directory reconstructs **the pipeline as a whole** — the path a *Drosophila* genome
took from a raw FASTA file to a statistical verdict about transposable elements and Cyp
genes.

It is an account of what happened, not a manual. Where a stage was implemented by a script,
this documentation says what the stage consumed, what it produced, and what it guaranteed to
the next stage. Line-by-line coverage of the scripts themselves is in
[`docs/scripts/`](../scripts/).

## The two tiers

**[`simple/`](simple/) — read this first.** Three short documents with flow charts. Enough
to understand what the pipeline is for, what the stages are, and what a single genome's
journey through it looks like. No code, no file formats.

| Doc | Covers |
|---|---|
| [01-what-it-does.md](simple/01-what-it-does.md) | The research question and the whole pipeline on one flow chart |
| [02-the-pipeline-in-six-stages.md](simple/02-the-pipeline-in-six-stages.md) | Each stage in plain language, with its own small flow chart — including stage 0, where two people's scripts diverge |
| [03-following-one-species.md](simple/03-following-one-species.md) | One real species end to end, with the real filenames and real numbers |

**[`detailed/`](detailed/) — the reference.** For someone who has to establish exactly what
a stage did, what format it emitted, or why a number came out the way it did.

| Doc | Covers |
|---|---|
| [01-architecture.md](detailed/01-architecture.md) | Why the pipeline is shaped this way; the two eras it was built in; where the halves join |
| [02-stage-reference.md](detailed/02-stage-reference.md) | Every stage: exact commands, parameters, runtimes, outputs, failure modes |
| [03-data-contracts.md](detailed/03-data-contracts.md) | Every file format passed between stages, with real examples from this repository |
| [04-gaps-and-provenance.md](detailed/04-gaps-and-provenance.md) | What is missing, what is broken, what is unresolved — and the sources for all of it |

## Where the facts come from

Three kinds of source, and this documentation keeps them distinct:

- **The lab's code, in [`../../evidence/`](../../evidence/)** — `lab-scripts/`,
  `te-locating-run/`, `analysis-scripts/`. Statements sourced here are checkable against the
  files.
- **Real data in this repository** — the 29 completed species outputs and the *D. ananassae*
  worked example under `evidence/te-locating-run/`. Numbers quoted in these documents were
  measured from those files.
- **The archive photographs**, transcribed in [`docs/ocr/`](../ocr/). For several stages
  these are the only record that survives. Anything sourced from them is marked with the
  transcription document it came from, e.g. *(OCR doc 02)*.

A fourth kind appears occasionally: **reproduced**, where a step was re-run from a path-only
copy outside the repository and its output diffed against the lab's own. Those passages say
so and give the result.

Where a stage exists only in the photographs and no code survives, the documentation says so
rather than describing it as though it were available.
