# The scripts, read line by line

This is the close-reading tier: each of the lab's scripts taken apart and explained, with its
defects called out where you would hit them. For the pipeline as a whole, start with
[`../pipeline/`](../pipeline/).

**These documents describe code, they do not invite you to run it.** Everything covered here
lives under [`../../evidence/`](../../evidence/) and is a forensic artifact: it is not
modified, and suggested fixes are recorded as findings about what *would* change, not as
work to do in this repository.

| Doc | Covers | The files it reads |
|---|---|---|
| [01-repeat-modeler-automation.md](01-repeat-modeler-automation.md) | `worker.sh`, `rm-manager.sh`, `rmodeler.conf` — concurrency, crash recovery, signal handling, container flags | **not in this repository** — see the note below |
| [02-te-locating-scripts.md](02-te-locating-scripts.md) | `repeatOpp.py`, `Locate_TE.py`, `CleanAnnasse.py` — line by line, with the bugs | `evidence/te-locating-run/` |
| [03-build-tfbs-te-gff.md](03-build-tfbs-te-gff.md) | `build_tfbs_te_gff.py` — all six internal phases, the FASTA indexer, the CncC motif, GFF3 emission | `evidence/analysis-scripts/` |
| [04-comparison-scripts.md](04-comparison-scripts.md) | the three `compare_te_cyp_*` scripts — parsing, filtering, the two restricted variants, report construction | `evidence/analysis-scripts/` |
| [05-statistics.md](05-statistics.md) | every test implemented, why it was chosen, how it is validated, and what the design cannot answer | `evidence/analysis-scripts/` |
| [06-final-final-gff.md](06-final-final-gff.md) | `ReVamp_Final.py` and its inputs — how `change_<SPECIES>_final_final.gff` was made, the defect that loses 7% of genes, and the verified re-run | `evidence/lab-scripts/gene-renaming/`, `evidence/lab-data/` |

> **Document 01 is the odd one out.** It describes `repeat-modeler-automation/`, which is
> *not* the lab's code and is no longer in this repository — it was written in September 2026
> to replace the lab's manual RepeatModeler/RepeatMasker sessions, and was split out into its
> own repository on 2026-09-15. It is kept here because it is the most complete description
> of what the lab's stage 1 and stage 2 had to do, and because the pipeline documentation
> still refers to it. Read it as background, not as an inventory of this repository.

Two further documents were once planned here and are deliberately **not** written, because
they would duplicate pipeline-level material that already exists:

- *data formats* → [`pipeline/detailed/03-data-contracts.md`](../pipeline/detailed/03-data-contracts.md)
- *provenance and history* → [`pipeline/detailed/04-gaps-and-provenance.md`](../pipeline/detailed/04-gaps-and-provenance.md)

Formats and provenance are properties of the pipeline, not of any one script, so they belong
there rather than here.

## Conventions

- Line references are `file.py:123` and point at the files as they sit in
  [`../../evidence/`](../../evidence/), **including the ` 1` / ` 1 1` filename suffixes**.
- Where behaviour is inferred rather than read directly from code, it says so.
- Known defects are called out in place rather than collected at the end, so you meet them
  where they bite.
- Where a document says "fix", it means *this is what would have to change*, as a
  characterisation of the defect. Nothing in `evidence/` is ever edited.
