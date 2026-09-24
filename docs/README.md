# Documentation

This is the written output of the investigation: what the lab's pipeline did, how that was
established, and what could not be established.

None of it is a manual. The pipeline is not here and is not meant to be run from here — a
cleaned, runnable version lives in the separate `cyp-te-pipeline` repository. What is here is
a reconstruction: read out of the lab's code, measured from the lab's data, transcribed from
photographs, and in a few places verified by re-running a step and diffing the result against
what the lab produced.

## Start here

- **The pipeline in one page** →
  [`pipeline/simple/01-what-it-does.md`](pipeline/simple/01-what-it-does.md). The research
  question and the whole chain on one flow chart.
- **What is wrong with it** →
  [`pipeline/detailed/04-gaps-and-provenance.md`](pipeline/detailed/04-gaps-and-provenance.md).
  Read this before quoting any number this pipeline produced.
- **What physically exists** → [`../evidence/README.md`](../evidence/README.md).

## How this is organised

| Directory | What it holds |
|---|---|
| [`pipeline/`](pipeline/) | **The main account.** The pipeline as a whole — the path a genome took from raw FASTA to statistical verdict. A `simple/` tier for orientation and a `detailed/` tier for reference |
| [`scripts/`](scripts/) | Individual scripts read line by line, with their defects called out in place |
| [`diagrams/`](diagrams/) | Mermaid flow charts, extracted so they can be read on their own |
| [`ocr/`](ocr/) | Transcriptions of the seventeen archive photographs. Cited throughout as *(OCR doc 04)* and so on |
| [`commands.md`](commands.md) | Every command the lab is known to have run, and every command run during the investigation to check it |
| [`superseded/`](superseded/) | Earlier, less complete reconstructions. Kept because the record of how the understanding developed is itself evidence |

## How claims are sourced

Four kinds of statement appear here, and they are kept distinct:

- **Read from the lab's code.** Line references like `ReVamp_Final.py:152` point at files in
  [`../evidence/`](../evidence/) and are checkable.
- **Measured from the lab's data.** Counts and percentages were computed from the files in
  `evidence/te-locating-run/` and `evidence/lab-data/`, read-only.
- **Transcribed from a photograph.** Marked with the transcription it came from, e.g.
  *(OCR doc 02)*. Several stages of the pipeline exist *only* in the photographs.
- **Reproduced.** A few claims were established by copying a script outside the repository,
  changing only its paths, running it, and diffing the output against the lab's own. Those
  say so and give the diff.

Where behaviour is inferred rather than established, the text says so.

## What the investigation found, in five lines

- The chain behind the `change_<SPECIES>_final_final.gff` files is fully reconstructed and
  verified — re-running it on *D. arizonae* reproduces the lab's file line for line.
- Two people wrote two incompatible versions of the gene-renaming step. The 29 finished
  species tables are a mix of both, and one version silently drops about 7% of orthologous
  genes.
- About 69% of what the pipeline counts as "TE burden" is simple repeats and low-complexity
  sequence, not transposable elements. Nothing filters on repeat class.
- The TE-to-gene window is a containment test, not an overlap test, so a transposon must fit
  entirely inside it: 71% of elements ≥5 kb that reach a window are discarded, including long
  elements in the *Cyp6g1* promoter in two species. *Cyp6g1* and its ~7 kb *Accord* insertion
  are the case the study generalises from.
- Parts of the chain are gone for good: the `config.py` behind the orthogroup steps, the
  original `Dmel_output.tsv`, and a page of the lab log recording per-species family counts.

## A note on stage numbering

The main account in [`pipeline/`](pipeline/) numbers the stages **0 through 6**, counting
input preparation as stage 0. The older documents in
[`superseded/simple/`](superseded/simple/) number four stages instead, and their numbers do
not line up. Where the two disagree, `pipeline/` is the one to trust.
