# Gaps, defects and provenance

What is missing from the lab's pipeline, what is wrong with it, what is unresolved — and where
each of those claims comes from. Nothing here is speculation; anything inferred says so.

This is the page to read before quoting any number this pipeline produced.

---

## Part 1 — Gaps: what did not survive

### G1. RepeatMasker (stage 2) — **recovered, and the recovery made things worse**

`runMasker.sh` has been found
([`../../../evidence/lab-scripts/shell/runMasker.sh`](../../../evidence/lab-scripts/shell/runMasker.sh)).
It is one command long and it contradicts every other source: `-lib` points at a gene
annotation GFF rather than a repeat library, there is no genome FASTA argument, and there is no
`-pa`. As saved it cannot have produced anything.

So the gap is not closed, it has changed shape. The command that actually produced the
surviving `.out` files is still known only from two independent secondary sources — the lab
notebook and the Kaur write-up, which agree with each other *(OCR docs 02, 05)*. What the
recovered file was for is open; the most economical reading is that it was path-edited per run
like the Python scripts and this is simply the state it was left in. See
[`02-stage-reference.md`](02-stage-reference.md).

### G2. Gene renaming (stage 0b) — **recovered and verified**

This was the largest gap and it is now largely closed. Both scripts are in
[`../../../evidence/lab-scripts/gene-renaming/`](../../../evidence/lab-scripts/gene-renaming/):

- `ReVamp_Final.py` (Duy, Dataset #2), along with the HOG table it reads and 25 of the 26
  `change_<SPECIES>_final_final.gff` files it produced. Re-running it on *D. arizonae* from
  the published Zenodo annotations reproduces the lab's own output **line for line**, once
  CRLF line endings and some stray tabs are normalised.
- `NEW_Step_5_Replace_gff_Names_with_Dmelanogaster_1_9.py` (Ayush, Dataset #1), which does the
  same job by parsing attributes properly instead of by raw text replacement.

The full account, including the defect that makes the two disagree, is in
[`../../scripts/06-final-final-gff.md`](../../scripts/06-final-final-gff.md).

**What is still gone** is the code that would build the HOG table for a *new* species:
`Step_2_…`'s `config.py`, `Step_1_…`'s `Dmel_HOG_association.tsv`, and the four OrthoFinder
post-processing scripts that appear in the shell history and nowhere else
(`Grab_data_Atallah_12_2.py`, `Rewrite_gene_names.py`, `Remove_duplicates_Atallah.py`,
`Bulk_gffread.py`). The orthology itself is not lost — it is published, as `hog=N1.HOG…`
attributes in the Zenodo annotations — but the lab's path to it is.

**Which dataset supersedes the other is still unresolved.** The log describes both without
ranking them; the lab notebook's procedure points at Dataset #2 *(OCR doc 02)*. The surviving
per-species tables say something the documents do not: **19 of them were built from Dataset #2
and 7 from Dataset #1**. See G4.

### G4. The finished tables mix two renaming methods — **the most consequential finding here**

Not a gap in the code but a gap in the record, and it affects results directly.

`ReVamp_Final.py` fails to rename any gene in a HOG cell that lists several genes, because
such cells are stored quoted and space-separated and the script splits on bare commas. For
*D. arizonae* that is **788 of 11,063** orthologous genes — about 7% — left with their
original IDs. Ayush's script parses those cells correctly.

Attributing each of the 29 finished tables back to one script or the other (by asking which
renamed annotation could explain each table's rows) gives:

| Built from | Species | Effect |
|---|---|---|
| **`ReVamp_Final.py`** | aldrichi, algonquin, anomalata, arawakana, arizonae, athabasca, elegans, helvetica, mauritiana, mayaguana, miranda, pandora, santomea, the four sulfurigaster tables, suzukii, tropicalis — **19** | 516 Cyp loci that a correct parse would find contribute **zero** TE rows |
| **the fully-parsing script** | erecta, mojavensis, pseudoobscura, sechellia, simulans, subpulchrella, willistoni — **7** | those loci are present |
| undeterminable | eugracilis and paulistorum (both tables are empty), melanogaster (needs no renaming) — **3** | — |

**Consequence:** the cross-species comparison sets 19 species whose Cyp gene sets are
systematically under-counted in multi-copy orthogroups against 7 whose are not. The
under-counting is not random with respect to gene family size, which is exactly the wrong
property for a comparison of gene-family-linked TE burden.

### G3. Files referenced but absent

### G3. Files referenced but absent

- `species_config.example.ini`, `te_cyp_species_config.example.ini` and
  `xenobiotic_resistance_cyp_genes.example.txt` are referenced by all four scripts in
  `evidence/analysis-scripts/` and by its README. **None exist.** Formats are documented in
  [`03-data-contracts.md`](03-data-contracts.md); the templates have to be written by hand.
- `12species_andothers.txt` — the full twelve-species list. Seen in a File Explorer window
  *(OCR doc 03b)*, not photographed open. The lab notebook's list gives only six of the twelve,
  three of them illegible *(OCR doc 02)*.
- **A fourth log page listing per-species family counts and runtimes.** Its existence is
  visible as mirror-image show-through on the back of log page 3 — `Families:` and `Runtime:`
  lines against species names — but the page itself was never photographed *(OCR doc 04)*.
  This is the only place per-species TE family counts were recorded.
- `TEandTFdata.xls`, the lab's results spreadsheet *(OCR doc 04)*.
- `Old Scripts/`, contents unphotographed *(OCR doc 03a)*.
- The four OrthoFinder post-processing scripts named in
  [`../../../evidence/lab-environment/bash_history`](../../../evidence/lab-environment/bash_history)
  and nowhere else — `Grab_data_Atallah_12_2.py`, `Rewrite_gene_names.py`,
  `Remove_duplicates_Atallah.py`, `Bulk_gffread.py`.
- The original `Dmel_output.tsv`. What is in
  [`../../../evidence/reconstructed/`](../../../evidence/reconstructed/) is a rebuild made
  during this investigation, not the lab's file — it reproduces the lab's *D. arizonae* result
  exactly, but that is an equivalence for one species, not an identity.
- `change_DROSOPHILA_MELANOGASTER_final_final.gff`. It exists, but at 13.8 GB from 145,112
  lines it is too large to commit and is held outside this repository. Its size is itself an
  open question — see U4.

---

## Part 2 — Defects in the surviving code

Ordered by how much they affect a result somebody might publish. These are **findings, not
work items**: nothing in `evidence/` is edited. Where a "fix" is described, it is a
characterisation of the defect — this is the thing that is wrong — and a note for whoever
rebuilds the pipeline elsewhere.

### D1. Simple repeats are counted as transposable elements

RepeatMasker reports every repeat, not only TEs. Nothing in the pipeline filters on repeat
class: stage 3b keeps every hit in the window, stage 4 records the class faithfully as
`repeat_class=` and then never uses it, and none of the three comparison scripts mention it.

Measured on the surviving *D. ananassae* result (900 rows):

| Class | Rows | Actually a TE? |
|---|---|---|
| `Simple_repeat` | 502 | no |
| `Low_complexity` | 118 | no |
| `Unknown` | 136 | unclassified |
| `RC/Helentron`, `LTR/Gypsy`, `LINE/CR1`, `RC/Helitron`, `DNA/TcMar-Tc1`, other | 144 | yes |

**About 69% of what the pipeline calls "TE burden" is microsatellite and low-complexity
sequence.** If simple-repeat density is uniform across species this adds noise; if it varies
with genome assembly quality or GC content — which it does — it adds bias, and in a comparison
between species groups that is exactly the wrong kind of error.

**What would have to change:** a filter on `repeat_class` (field 10 of the `.out` line). The
natural place is stage 3b, though stage 4 already parses the class and could expose an
exclusion option without disturbing the narrow-waist format. The point of recording it here is
that **the lab's inclusion of simple repeats was silent — there is no evidence anywhere in the
archive that it was a decision at all**, rather than something inherited from RepeatMasker's
default output and never examined.

### D2. Row duplication in `filtered.gff`

`repeatOpp.py` emits one row per *matching symbol* rather than per gene, so a gene annotated
with four Cyp names is written four times. Measured: **166 rows, 91 unique, 57 distinct
genes**, from 117 input gene records.

Stage 4 de-duplicates on the way in, so the final GFF3 is correct — but any count taken from
`filtered.gff`, `GenesAffectedByTEs.txt` or `D_*GenesAffectedByTE.txt` directly is inflated by
roughly 80%. The `AnalysisForAll/` intermediate files have this property.

### D3. The TE window tests containment, not overlap

`Locate_TE.py` requires the repeat to lie *entirely* within `[gene_start − 3000,
gene_end + 3000]`. An element straddling the window edge is dropped.

This is the wrong default for TE work — overlap is the standard criterion — and it biases
against exactly the long elements most likely to matter. The *Accord* insertion upstream of
*Cyp6g1*, the case that motivates the whole project, is ~7 kb; an element that size sitting in
a promoter would be excluded by this test unless it happened to fall wholly inside the window.

Because stage 4 writes the association into `Description=Within range of …` and stage 6 reads
it from there, **this rule is fixed at stage 3 and cannot be revisited downstream.**

Related, minor: `start` goes negative for genes within 3 kb of the start of a sequence. Harmless
in practice, but the window is silently asymmetric for those genes.

### D4. The `D`-prefix skip drops five real entries

Both `repeatOpp.py` and `CleanAnnasse.py` skip every line of `Reg_Gene_Full.txt` beginning with
`D`. Five genuine entries are discarded: `Dvir\GJ21722`, `Dmoj\GI21254`, `Dvir\GJ21709`,
`Dvir\GJ22648`, `Dvir\GJ20586`. The effective target list is **91 symbols, not 96**.

### D5. Substring matching in stage 3, exact matching in stage 6

Stage 3 matches with `Rgene in fields[8]` — a substring test against the whole attribute
column. Stage 6's xenobiotic list matches exactly and case-insensitively. The two stages
therefore disagree about what "this gene is on the list" means, and a short symbol in
`Reg_Gene_Full.txt` will match longer unrelated symbols.

### D6. The ` 1 1` filename suffixes break the imports

`compare_te_cyp_cncc.py` and `compare_te_cyp_xenobiotic.py` both do
`import compare_te_cyp_exposure`, which cannot resolve against a file named
`compare_te_cyp_exposure 1 1.py`. **As delivered, two of the three comparison scripts cannot
have run at all.**

That is a forensic point rather than a packaging nit. Whatever results the lab has from the
CncC and xenobiotic comparisons were produced from *some* copy of these files under importable
names — a copy that is not in the archive. The delivery preserved in
`evidence/analysis-scripts/` is a broken export of working code, not the working code.

The suffixes are Windows duplicate-file renames acquired on round trips through zip and
OneDrive — ` 1` in the Summer 2026 working folder *(OCR doc 03a)*, doubled to ` 1 1` by a
further export, of which `evidence/analysis-scripts/OneDrive_1_9-1-2026.zip` is one.

### D7. Stage 3 has hardcoded absolute paths and no arguments

All three scripts carry `C:/Users/User/Documents/BioAtallah/...` literals at module scope and
must be edited before each run. This is the direct cause of the twenty-nine hand-typed output
filenames, three of which are misspelled (`D_secheliaGenesAffectedByT.txt`,
`D_athabascaGenesAfffectedByTE.txt`, `D_arawakanaGenesAffectedByTe.txt`).

This is not merely inconvenient: it is why the archive contains the *same script twice with
different paths baked in* (`Locate_TE.py`, in `evidence/te-locating-run/` and in
`evidence/lab-scripts/te-locating/`), and why there is no way to tell from any surviving file
which species a given run was for except by reading the literals at the top.

### D8. Scaling

`Locate_TE.py` is `O(genes × repeats)` with the entire `.out` file held in memory — 91 genes ×
297,073 repeats for *D. ananassae*. Adequate for a Cyp-only gene set; it will not survive being
pointed at a whole-genome annotation.

---

## Part 3 — Unresolved questions

### U1. The Flynn et al. benchmark shortfall

Rerunning *D. melanogaster* on the same genome with the same stated parameters
(`-LTRStruct`, `-srand 1570222393`, `-LTRMaxSeqLen 10000`) produced **471 families against the
published 734** — a 36% shortfall. Runtime 12:39:21. The corresponding authors were emailed to
ask about further parameters; the log records *"Awaiting response"* and nothing after
*(OCR doc 04, page 3)*.

**This is unresolved and it is material.** Until it is closed out, per-species family counts
from this pipeline should be treated as a lower bound rather than a measurement. Note also
that `-srand` is not a documented RepeatModeler option as transcribed — it may be
version-specific or a transcription artefact, and it has not been verified against
`RepeatModeler --help`.

### U2. Pseudoreplication

The comparison pools individual Cyp genes across species and treats each as an independent
observation. Genes within a species share a genome and a phylogeny, so they are not. With only
a handful of species there is no clean alternative: a species-level test would have almost no
power.

The code handles this about as well as it can be handled — it states the caveat in every
generated report, runs a bootstrap over species clusters for a more honest confidence
interval, and labels the species-level comparison as descriptive rather than inferential. **The
caveat should never be removed from the report template**, and results should not be quoted
without it.

### U3. How many species is this study actually about?

Four different numbers appear, and they are not contradictory — they are ambition, target,
completed and visualised. Quote the right one:

| Number | What it is | Source |
|---|---|---|
| 300+ | the stated ambition | write-up introduction *(OCR doc 05)* |
| 12 | the target batch | lab notebook heading, though only six are listed *(OCR doc 02)* |
| 17 | per-species working folders in the Summer 2026 analysis directory | *(OCR doc 03a)* |
| 29 | species with a completed stage 3 table | `AnalysisForAll/output/`, counted |
| 5 | species in the comparison configuration | the stage 6 script docstrings |
| 3 | species with saved JBrowse sessions | *(OCR docs 03b, 04)* |

The "300+" figure should not be read as a count of anything that exists.

A seventh number is worth adding now: **19 vs 7** — the split of the 29 finished tables
between the two renaming scripts (G4). It is the number that most affects whether the
comparison means anything.

### U4. Why is the *D. melanogaster* `final_final` file 13.8 GB?

`change_DROSOPHILA_MELANOGASTER_final_final.gff` has 145,112 lines and is 13.8 GB, so some
lines must be enormous. The garbling visible in it points at the cause: `JYalpha` becomes
`JYNil,alpha`, `gene_synonym` repeats, and `genome` becomes `genom,nom,ouibe`.

`ReVamp_Final.py` runs `str.replace` once per dictionary entry over every line, with no word
boundaries and no protection against a later key rewriting an earlier key's output. For every
other species the replacement keys are fixed-width IDs (`gene-G` + 11 digits) and nothing else
in the file can match them. For *D. melanogaster* the keys are gene *symbols*, some of them one
or two letters (`a`, `e`, `ab`) — so the replacements chain, feeding on their own output.

**This is a hypothesis, not a measurement.** The line-length scan that would confirm it was
started and never finished. It is the most likely explanation by some distance, and it is
consistent with every garbled string observed, but it has not been demonstrated.

### U5. What changed between the Zenodo releases?

The lab's working annotations lived in a folder called `gff_fixed/`, and the natural reading
of that name is that somebody fixed something. They did not: the June 2025 Zenodo release
(record 15705949) already ships a directory called `gff_fixed/`, so the lab simply used what
was published. The April/May 2025 releases (15016918, 15341692) ship `GFF/` instead, and the
February 2026 release (18453526) ships `gffs/*.gff.gz`.

**What actually differs between `GFF/` and `gff_fixed/` was never established.** Downloading
the June archive to compare them was attempted and abandoned — Zenodo throttled to 50–100 KB/s
and only an 11 MB fragment came down, which is what sits in
[`../../../evidence/reconstructed/zenodo-partial-download/`](../../../evidence/reconstructed/zenodo-partial-download/).

Two things *are* established, from the verified re-run in
[`../../scripts/06-final-final-gff.md`](../../scripts/06-final-final-gff.md): the lab's
`gff_fixed` copies are **not** byte-identical to the February 2026 `gffs/` ones — 19,458 mRNA
lines have literal tabs where the later release has spaces — and that difference does not
affect renaming.

---

## Part 4 — Provenance

### Who did what

From the Spring 2026 log and the write-up *(OCR docs 04, 05)*:

| Person | Contribution |
|---|---|
| Diljot Kaur (log author, write-up author) | Fixed the gene-renaming code; ran RepeatModeler2 and RepeatMasker; kept the log; wrote the procedural write-up; made the LBRN poster |
| Duy | `ReVamp_Final.py` → Gff_Dataset#2; co-developed the March pipeline; ran RepeatMasker processing |
| Ayush | Winter-break edits producing `NEW_Step_5_Replace_gff_Names_with_Dmelanogaster_1_9.py` → Gff_Dataset#1 |
| Charles | Co-developed the March pipeline; downstream RepeatMasker/TFBS result processing |
| Terry | Custom scripts, named in the write-up only — and named again, independently, by the hand-edited `*_TerryEdits` TE tables in `evidence/lab-data/te-tables/` |

The pipeline itself is dated: *"March — Developed pipeline for RepeatModeler2 → RepeatMasker →
TFBS/Motif Analysis with Duy and Charles"* *(OCR doc 04)*.

**Nobody is credited with `evidence/analysis-scripts/`.** The four scripts there are markedly
more careful than anything else in the archive — argument parsing, documented fallbacks,
cross-validated statistics, a `--self-test` mode — and they arrived as a January 2026 OneDrive
export rather than being found among the lab's working files. No log entry, write-up page or
notebook line mentions them. That is the largest hole in the attribution.

### Why the code looks the way it does

Nearly every oddity in the archive traces to a documented fact about how the work was
actually done. This table is the short answer to most "why on earth…?" questions:

| Observation | Explanation | Source |
|---|---|---|
| Stage 1 had to be babysat over days; everything else is plain scripts | 8-26 h per genome; 45 h observed | *OCR docs 04, 03c* |
| The same script exists twice with different paths baked in | One copy per species run; the path *was* the configuration | `evidence/lab-scripts/te-locating/` vs `evidence/te-locating-run/` |
| Two incompatible gene-renaming scripts, both kept | Two people solved the same problem independently, months apart, and nothing ever chose between them | *OCR doc 04*, and G4 above |
| Hardcoded Windows paths at the top of the stage 3 scripts | They were run by hand in VS Code, pasting one path per run, three runs per species | *OCR docs 02, 05, 06* |
| ` 1` and ` 1 1` filename suffixes | Windows duplicate-rename on round trips through zip/OneDrive | *OCR doc 03a* |
| No end-to-end driver script exists | No single machine ever ran the whole pipeline — stage 2 happened on a collaborator's machine, reached via OneDrive | *OCR doc 04* |
| Zero third-party Python dependencies | Code had to run on whatever machine received the zip | inferred from the above |
| Genome FASTAs still read from the older `Dhakad` tree | Apparently never moved when `Spring26/` became the working directory | *OCR docs 02, 04, 06* |

### The archive itself

**The photographs.** Seventeen images in
[`../../../evidence/photographs/`](../../../evidence/photographs/), transcribed in
[`../../ocr/`](../../ocr/): a terminal window, two shots of one lab-notebook page, three File
Explorer windows, a typed three-page monthly log, a five-page student write-up, and a
handwritten data-flow sketch. `Photos-1-001.zip` contains no unique images.

All seventeen have been read and their transcriptions verified against the images. What the
photographs establish that no file does: the container invocation, the RepeatModeler command
and its parameters, the 8-26 hour runtime, the manual VS Code procedure, the OneDrive handoff,
the Flynn benchmark shortfall, and who wrote which script.

**The machine traces.** Three files in
[`../../../evidence/lab-environment/`](../../../evidence/lab-environment/) do work the
photographs cannot. `bash_history` is the only record that the OrthoFinder post-processing
scripts ever existed, and it shows the orthogroup work being driven from a WSL mount of a
Windows `D:` drive. `directory.txt` and `listing.txt` date the RepeatModeler runs
independently of the File Explorer screenshots, and name the `RM_<pid>.<date>` run directories
the notebook refers to only as `RM_#$date`.

**The archives.** `python.7z`, `tosend.7z` and `data_stuff.7z`, kept unopened beside their
extracted contents in [`../../../evidence/lab-archives/`](../../../evidence/lab-archives/).
`tosend.7z` is the informative one: 32 of its 42 files were byte-identical to scripts already
present, and the 10 that were not are results — including the hand-edited `*_TerryEdits`
tables, which are the only direct evidence of manual correction of pipeline output anywhere in
the archive.
