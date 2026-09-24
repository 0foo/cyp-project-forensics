# Flow charts

Mermaid diagrams, extracted so they can be read on their own. GitHub, GitLab and most Markdown
previewers render these inline; VS Code needs the *Markdown Preview Mermaid Support*
extension.

| Diagram | Scope |
|---|---|
| [01-end-to-end.md](01-end-to-end.md) | Genome FASTA → result. The whole pipeline on one page, with the two places the evidence conflicts. |
| [02-worker-concurrency.md](02-worker-concurrency.md) | **Not the lab's code.** The state machine of the 2026 replacement for stages 1 and 2, kept as the clearest statement of what those stages demanded. |
| [03-gff3-build.md](03-gff3-build.md) | Inside `build_tfbs_te_gff.py`: its six internal phases and their fallbacks. |
| [04-comparison-flow.md](04-comparison-flow.md) | The three `compare_te_cyp_*` scripts and the statistics they share. |
| [05-data-lineage.md](05-data-lineage.md) | Which file became which, for every data file in [`../../evidence/`](../../evidence/). |
