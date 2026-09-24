# Evidence

Everything in this directory is an artifact. **Nothing here is ever modified, fixed,
regenerated or tidied.** A script that does not run stays as it is; a filename with a typo
keeps the typo; a table with a defect keeps the defect. Defects are written up in
[`docs/`](../docs/), never patched here.

To execute something for a test, copy it outside the repository, change only paths in the
copy, and write output outside the repository too.

There is one exception, quarantined in [`reconstructed/`](#reconstructed): files produced
*during* the investigation rather than by the lab. They are kept apart precisely so they can
never be mistaken for originals.

---

## Where it all came from

| Directory | Origin |
|---|---|
| `lab-scripts/`, `lab-data/`, `lab-archives/`, `lab-environment/` | Extracted from 7-Zip archives handed over by the lab (`python.7z`, `tosend.7z`, `data_stuff.7z`, `final_final.7z`, `hog_og.7z`), plus loose files added directly |
| `te-locating-run/` | The lab's own working folder for the TE-locating step, with one species carried end to end and 29 finished species tables |
| `analysis-scripts/` | Four Python scripts that reached the project as a OneDrive export; the export zip is kept beside them |
| `photographs/` | Seventeen phone photographs of lab notebooks, terminal windows and File Explorer windows. Transcribed in [`docs/ocr/`](../docs/ocr/) |
| `reconstructed/` | Produced during this investigation. Not lab originals |

**Timestamps are not evidence.** Almost every file here carries the date it was extracted
from an archive, not the date the lab wrote it. Dates in filenames (`_10_31`, `_1_9`,
`_11_5`) are the lab's own versioning and *are* meaningful; filesystem mtimes are not.

---

## `lab-scripts/`

The lab's code, grouped by what it does. None of it runs as-is: every file carries absolute
Windows paths (`C:/Users/User/Documents/BioAtallah/…`, `D:/CYP_Gene_Project/…`,
`B:/Copy_toDuy/…`) at module scope and takes no arguments.

### `orthogroup-tables/`

Builds the HOG (hierarchical orthogroup) table that everything else keys on. Reads
OrthoFinder output and each species' annotation, and turns mRNA identifiers into gene
identifiers.

| File | Role |
|---|---|
| `Step_1_Replace_RNA_identifiers_with_gene_names_Redo.py` | mRNA IDs → gene IDs, via each GFF's `Parent=` |
| `Step_2_Remove_Duplicate_gene_names_10_31.py` | Collapses duplicate gene names within a cell |
| `Step_3_Count_CYP_Genes_Copy_10_31.py` | Per-species Cyp gene counts |
| `Step_4_Extract_CYP_Genes.py` | Restricts the counts to the stable/unstable Cyp lists |

**Neither Step 1 nor Step 2 can be re-run.** Step 2 imports a `config.py` that was never
kept, and Step 1 reads a `Dhakad_et_al_2025_Data/Dmel_HOG_association.tsv` that is not
anywhere in this repository. The tables they produced survive in `lab-data/hog-tables/`;
the code path to a *new* species does not.

### `gene-renaming/`

The step that gives every species' genes their *D. melanogaster* ortholog names. This is the
most thoroughly investigated part of the pipeline — see
[`docs/scripts/06-final-final-gff.md`](../docs/scripts/06-final-final-gff.md).

| File | Author | Role |
|---|---|---|
| `ReVamp_Final.py` | Duy | Produced the `change_<SPECIES>_final_final.gff` files in `lab-data/renamed-annotations/`. Verified by re-running |
| `ReVamp_Final_copy_1_10.py` | Duy | An older copy, with a bug (`cleanedAnno` for `cleanAnno`) and a different output name |
| `Part5_Final.py`, `Step5.py`, `Step5_1_test.py` | Duy | Earlier attempts at the same step. `Step5_1_test.py` is a scratchpad exploring exactly the multi-gene-cell parsing that `ReVamp_Final.py` gets wrong |
| `NEW_Step_5_Replace_gff_Names_with_Dmelanogaster_1_9.py` | Ayush | The *other* renaming script, producing `*_withDmelNames.gff`. Parses attributes properly instead of doing raw text replacement, and does not have ReVamp's defect |

The two scripts do not produce the same result, and the finished per-species tables in
`te-locating-run/AnalysisForAll/output/` are a **mix of both — 19 species from Duy's, 7 from
Ayush's, 3 undeterminable**. Duy's silently leaves about 7% of orthologous genes un-renamed
(it splits multi-gene orthogroup cells on a bare comma, but the table stores them quoted and
space-separated), and the losses fall on multi-copy Cyp clusters specifically. Nothing in the
archive shows anyone noticing that both were in use.

That finding is the reason this directory matters, and it is the one place where reading the
lab's code changes how its published numbers should be read.

### `te-locating/`

The step that pairs Cyp genes with nearby transposable elements, plus its variants and
offcuts.

| File | Role |
|---|---|
| `repeatOpp.py` → `Locate_TE.py` → `CleanAnnasse.py` | The three-script chain, in order. The *D. ananassae* copies |
| `Step1FindCyp.py` → `Step2FindTEs.py` → `Step3CleanData.py` | The same three steps, pointed at FlyBase *D. melanogaster* files |
| `CleanedData.py` | `CleanAnnasse.py` again, writing `Dmel_TE_Cyp.txt` |
| `FindStableCyp.py` | `repeatOpp.py` again, against the *D. melanogaster* annotation |
| `Filter_startandstops.py` | Extracts `start_codon`/`stop_codon` rows from an annotation |
| `RemoveDuplicates.py` | Line-level de-duplication of a combined GFF |
| `Make_Counts.py`, `inprogress.py` | TFBS-per-TE tallies; `inprogress.py` is the unfinished earlier form of `Make_Counts.py` |

**This directory is itself the evidence for how the lab worked.** `Locate_TE.py` here and
`Locate_TE.py` in `te-locating-run/` are the same script differing only in their two
hardcoded paths — one set pointing at *D. ananassae*, the other at *D. melanogaster*. That
is the "open the file, paste a path, save, click run" cycle recorded in the lab notebook,
preserved as two files.

### `poster-figures/`

Data-wrangling and plotting for a conference poster, working from the HOG gene-count tables.
`poster.py` → `finPoster.py` → `finfinPoster.py` → `remakeFinPoster.py` is a visible
progression of the same figure. `cleaning.py`, `makethingsUPPER.py` and
`check_species_matches.py` are the supporting species-list manipulation. None of this feeds
the pipeline.

### `shell/`

| File | Note |
|---|---|
| `spinContainer.sh` | Matches the terminal photograph (`docs/ocr/01`) line for line. Starts an interactive `dfam/tetools:latest` container; it does not run RepeatModeler |
| `runMasker.sh` | **Recovered, and it is not what the notebook describes.** Two lines, no `-pa`, no genome FASTA, and the `-lib` argument is a *GFF file* rather than a repeat library. See [`docs/pipeline/detailed/02-stage-reference.md`](../docs/pipeline/detailed/02-stage-reference.md) |

### `scratch/`

`dMel.py` and `test_repeat.py` open a file and print it. `tempCodeRunnerFile.py` is a
three-line fragment left behind by the VS Code Code Runner extension — mid-expression,
starting `ool = True):`. Kept because they date and place the work, not because they do
anything.

---

## `lab-data/`

### `hog-tables/`

Twenty versions of the orthogroup table, about 1 GB. One row per HOG, one column per species
(308 columns), each cell holding that species' genes in that orthogroup.

The one that matters is
`HOG_OG_association_gene_names_without_duplicates_10_31.tsv` — the input
`ReVamp_Final.py` actually reads. The `_1_9` variant is the same table regenerated in
January; the undated variants are earlier still.

> `HOG_OG_association.tsv` and `HOG_OG_association_1_9.tsv` are present **only as `.xz`**.
> They were compressed during this investigation (111 MB → ~10 MB each) and the
> uncompressed originals deleted after a verified byte-exact round trip. This is the one
> place a lab original was altered, and it is recorded here for that reason.

### `renamed-annotations/`

25 `change_<SPECIES>_final_final.gff` files, 1.7 GB in total, each an annotation whose gene
IDs have been swapped for *D. melanogaster* symbols by `ReVamp_Final.py`.

**26 were produced; 25 are here.** `change_DROSOPHILA_MELANOGASTER_final_final.gff` is
13.8 GB — from 145,112 lines — and lives outside this repository in `cyp-old-data/`. Why one
file with an ordinary line count is 13.8 GB is an open question; the evidence points at
`ReVamp_Final.py`'s chained `str.replace` feeding on its own output when the replacement
keys are short gene symbols rather than fixed-width IDs.

### `te-tables/`

Per-species "genes affected by TE" tables that came over with the archives rather than being
produced in `te-locating-run/`. The `*_TerryEdits` / `*_terryEdits` pairs are hand-edited
versions of the file beside them. `GenesAffectedByTEs.txt` is an intermediate, not a final
table. `D_Ananassae_GenesAffectedByTE.txt` (98 rows) is an early partial run of a species
that was later completed.

### `cyp-gene-lists/`

The literature-derived gene lists: the 87 *D. melanogaster* Cyp genes with clans
(Dermauw 2020), and Good et al. 2014's split of Cyp genes into evolutionarily stable (29) and
unstable (46) sets, with and without HOG identifiers attached. `Create_Dmel_Cyp_stable_list.py`
builds one from the others.

Some HOG identifiers in the `Updated_*` lists do not match the `_10_31` table.

### `repeatmasker-out/`

`Drosophila_crucigera.nanopore.rm.out` — RepeatMasker output for a species with no gene
annotation and no `final_final` file, so it cannot be carried further. It is a sample of the
format rather than a stage in anything.

---

## `lab-archives/`

`python.7z`, `tosend.7z` and `data_stuff.7z` as received. Their contents are already
extracted into the directories above; the archives are kept as the un-tampered original
delivery. `tosend.7z` is the more interesting of the two script archives — 32 of its 42 files
were byte-identical to what was already present, and the 10 new ones were results, including
the hand-edited "Terry's edits" tables.

## `lab-environment/`

Traces of the machines the work ran on, and the only record of several steps.

| File | What it shows |
|---|---|
| `bash_history` | The orthogroup work as it was actually driven: OrthoFinder results directories, `Grab_data_Atallah_12_2.py`, `Rewrite_gene_names.py`, `Bulk_gffread.py` — **scripts that are named here and exist nowhere else** |
| `directory.txt` | A `ls -la` of the RepeatModeler working directory: per-species `-families.fa`/`.stk`/`-rmod.log` and BLAST database files, with real dates |
| `listing.txt`, `listing2.txt` | Recursive listings of the RepeatModeler output tree, including the `RM_<pid>.<date>` run directories and their round-1…round-5 subfolders |

## `te-locating-run/`

The lab's working folder for the TE-locating step, and the most useful thing in this
repository: it holds real inputs *and* real outputs for the same species, so the scripts can
be checked against what they actually produced.

| Path | What it is |
|---|---|
| `DA_Files/` | *D. ananassae* inputs — the renamed annotation and the RepeatMasker `.out` (39 MB, 297,073 lines) |
| `filtered.gff`, `GenesAffectedByTEs.txt`, `DAnasse_TE_Cyp.txt` | That species, step by step |
| `repeatOpp.py`, `Locate_TE.py`, `CleanAnnasse.py` | The scripts that produced them, paths and all |
| `AnalysisForAll/output/` | **29 finished species tables** |
| `AnalysisForAll/Reg_Gene_Full.txt` | The 96-line Cyp target list |
| `AnalysisForAll/GFF/`, `AnalysisForAll/FilesFromMasker/` | *D. sechellia* and *D. simulans* inputs |
| `AnalysisForAll/step1Temp.gff`, `step2GenesAffectedByTEs.txt` | The same intermediates from the *D. melanogaster* run |

`DA_Files/DROSOPHILA_ANANASSAE_final_withDmelNames.gff` is **truncated** — one chromosome,
ending mid-line — so it is not what the committed results were made from. `filtered.gff`
*is* consistent with the full file, and re-running the last two steps from it reproduces the
committed outputs exactly.

Every table here was produced under the containment window rule described in
[`reconstructed/window-rule-analysis/`](reconstructed/window-rule-analysis/), which silently
drops long elements near genes. Nothing in the tables records that, so the counts in them are
lower bounds of a particular, undocumented kind.

Three of the 29 output filenames are misspelled (`D_secheliaGenesAffectedByT.txt`,
`D_athabascaGenesAfffectedByTE.txt`, `D_arawakanaGenesAffectedByTe.txt`) and the
capitalisation of `ByTE`/`ByTe`/`ByT` varies. Those typos are load-bearing evidence of the
manual workflow and are not to be corrected.

## `analysis-scripts/`

Four Python scripts that merge the TE tables into combined GFF3s and run the cross-species
comparison, plus `OneDrive_1_9-1-2026.zip`, the export they arrived in. Their own README is
kept beside them, reframed.

The ` 1` and ` 1 1` suffixes in the filenames are Windows duplicate-file renames picked up on
round trips through zip and OneDrive. They are also the reason two of the three comparison
scripts cannot import the third: **as delivered, they do not run.** Left as-is.

## `photographs/`

The seventeen source images, transcribed in [`docs/ocr/`](../docs/ocr/). `Photos-1-001.zip`
contains no unique images — it duplicates the eleven `PXL_20260910_18*.jpg` files sitting
loose beside it.

## `reconstructed/`

**Not lab originals.** Produced during this investigation and kept separate so they are never
mistaken for evidence.

| File | What it is |
|---|---|
| `make_Dmel_output.py` | Written 2026-09-24 to rebuild `Dmel_output.tsv` from the HOG table, using only the standard library |
| `Dmel_output.tsv` | Its output: 12,151 rows of HOG → *D. melanogaster* symbol. The lab's original was never kept. This rebuild reproduces the lab's *D. arizonae* result exactly, so the two are equivalent at least there |
| `zenodo-partial-download/annotations_15705949.tar.gz` | An 11 MB partial download of the June 2025 Zenodo annotations, abandoned when Zenodo throttled. Kept because it is the only local trace of that record's contents |
| `window-rule-analysis/` | The transposons the lab's 3 kb window rule discards, measured across the three species whose inputs survive, plus the script that produced the list. See its own README |

### `window-rule-analysis/` — the transposons the pipeline never saw

`Locate_TE.py` requires a repeat to lie *entirely* inside a gene's ±3 kb window, so an element
reaching into the window but extending past its edge is dropped however close to the gene it
begins. This directory holds the elements that were dropped:
`missed_transposons.tsv` (38 associations, 22 Cyp genes, 3 species) and the re-runnable script
that found them.

The finding that matters: **the rule discards a 4,321 bp LINE/I-Jockey element 650 bp upstream
of *Cyp6g1* in *D. simulans*, and a 2,129 bp element 1,245 bp upstream of *Cyp6g1* in
*D. ananassae*.** *Cyp6g1* and its *Accord* insertion are the case the whole study
generalises from, and *Accord* is ~7 kb — a size a containment test against a 3 kb flank
cannot admit. Details and caveats:
[`window-rule-analysis/README.md`](reconstructed/window-rule-analysis/README.md).

---

## Where things moved

This repository was reorganised on 2026-09-24. Nothing was deleted and no file content was
altered; the mapping below is the chain of custody.

| Was | Is now |
|---|---|
| `to_organize/*.py` (lab scripts) | `evidence/lab-scripts/<group>/` |
| `to_organize/*.sh` | `evidence/lab-scripts/shell/` |
| `to_organize/hog_og/` | `evidence/lab-data/hog-tables/` |
| `to_organize/final_final/` | `evidence/lab-data/renamed-annotations/` |
| `to_organize/data_stuff/` | `evidence/lab-data/cyp-gene-lists/` |
| `to_organize/repeat-modeler-masker-out/` | `evidence/lab-data/repeatmasker-out/` |
| `to_organize/*GenesAffectedByTE*.txt` | `evidence/lab-data/te-tables/` |
| `to_organize/*.7z` | `evidence/lab-archives/` |
| `to_organize/bash_history`, `directory.txt`, `listing*.txt` | `evidence/lab-environment/` |
| `to_organize/make_Dmel_output.py`, `Dmel_output.tsv`, `zenodo_dl/` | `evidence/reconstructed/` |
| `pipeline-scripts-output/` | `evidence/te-locating-run/` |
| `analysis-pipeline/` | `evidence/analysis-scripts/` |
| `collected-docs/src/` | `evidence/photographs/` |
| `collected-docs/pipeline-docs/` | `docs/superseded/first-pass-reconstruction/` |
| `OCR docs/` | `docs/ocr/` |
| `docs/deep/` | `docs/scripts/` |
| `docs/simple/` | `docs/superseded/simple/` |

Before that, `to_organize/` was called `python/` — the folder `python.7z` extracted to.
