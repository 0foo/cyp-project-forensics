# Superseded documentation

Two earlier passes at documenting the pipeline, kept and clearly labelled rather than
deleted.

They are here because **how the understanding developed is itself part of the record**. A
forensic reconstruction that quietly replaces its own earlier conclusions loses the ability
to say *when* something became known, and which claims were revised. Where these documents
disagree with [`../pipeline/`](../pipeline/), the current account is the one to trust — but
the disagreement is informative.

| Directory | What it is | Superseded by |
|---|---|---|
| [`first-pass-reconstruction/`](first-pass-reconstruction/) | September 2026. Written from the seventeen photographs alone, before any of the lab's code had been recovered. Explicitly marked `[VERIFY]` throughout, because at that point nothing could be checked against a file | [`../pipeline/`](../pipeline/) |
| [`simple/`](simple/) | A four-stage plain-language tier written alongside the first script-level reading. Overtaken by [`../pipeline/simple/`](../pipeline/simple/), which covers all six stages and is more accurate | [`../pipeline/simple/`](../pipeline/simple/) |

## Known inaccuracies in these documents

Recorded here so nobody has to rediscover them, and so the documents themselves can stay as
they were written.

**Both sets:**

- They describe the pipeline as something available to run in this repository. It is not; it
  never was, in the form they imply.
- They refer to `repeat-modeler-automation/`, `pipeline-scripts-output/` and
  `analysis-pipeline/` as top-level directories here. The first was split out into its own
  repository in September 2026; the other two are now `evidence/te-locating-run/` and
  `evidence/analysis-scripts/`.

**`first-pass-reconstruction/` specifically:**

- It treats `runMasker.sh` as running
  `RepeatMasker -lib consensi.fa.classified -pa 8 <genome>.fna`. The real script has since
  been recovered and does nothing of the sort — see
  [`../pipeline/detailed/02-stage-reference.md`](../pipeline/detailed/02-stage-reference.md).
- It groups `ReVamp_Final.py`, `NEW_Step_5_…` and `build_tfbs_te_gff.py` into one
  "VS Code Python scripts (manual 3-step run)" box. They are three separate things at two
  different points in the chain, and the first two are alternatives to each other rather than
  steps in sequence.
- Its stage list stops at five stations and omits the orthogroup-table construction that
  everything upstream of gene renaming depends on.

**`simple/` specifically:**

- It numbers the stages 1–4. The current account numbers them 0–6, and the numbers do not
  correspond: its "stage 2" is the current stage 3, its "stage 3" is stage 4, its "stage 4"
  is stage 6.
- Its "how to run it" sections describe running code that is not in this repository.
