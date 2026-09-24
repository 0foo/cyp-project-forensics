# Commands

Two lists. The first is **what the lab ran** — reconstructed from the photographs, the shell
history and the scripts themselves, and useful because several of those commands are the only
record of a stage. The second is **what was run during this investigation** to check the
first, kept so the checks can be repeated.

Nothing on this page is an instruction to run the pipeline. For that, see the separate
`cyp-te-pipeline` repository.

---

# Part 1 — What the lab ran

## Building the orthogroup table

Known only from `evidence/lab-environment/bash_history`. OrthoFinder was run over the twelve
species' proteomes; its results directory (`OrthoFinder/Results_Mar29_1/Orthogroups_Genes/`)
was then processed by a series of scripts:

```
python Grab_data_Atallah_12_2.py        # and _12_3.py, _12.py
python Rewrite_gene_names.py
python Remove_duplicates_Atallah.py
python D:/CYP_Gene_Project/04_24/04_22/All_Input/Bulk_gffread.py
```

> **None of those four scripts exist anywhere in this repository.** The history is the only
> evidence they were ever written. The scripts in
> `evidence/lab-scripts/orthogroup-tables/` (`Step_1_…` through `Step_4_…`) do the same kind
> of work and produced the tables that survive, but they are not the same files, and the
> shell history shows them being run from a WSL mount of a Windows `D:` drive.

The surviving `Step_*` scripts take no arguments either:

```
python Step_1_Replace_RNA_identifiers_with_gene_names_Redo.py
python Step_2_Remove_Duplicate_gene_names_10_31.py     # needs a config.py that was not kept
python Step_3_Count_CYP_Genes_Copy_10_31.py
python Step_4_Extract_CYP_Genes.py
```

## Stage 1 — RepeatModeler

From the terminal photograph *(OCR doc 01)*, and recovered verbatim as
`evidence/lab-scripts/shell/spinContainer.sh`:

```bash
docker run -it --rm \
    -v $(pwd):/Spring26RepeatModeler \
    -w /Spring26RepeatModeler \
    dfam/tetools:latest bash
```

That starts an **interactive shell**; it runs nothing. The operator then typed, inside the
container *(OCR doc 04)*:

```
BuildDatabase -name D_speciesname Species_genome_file.fa
RepeatModeler -database D_speciesname -threads 10 -LTRStruct
```

8–26 hours per genome, 45 hours observed on one run with `-LTRStruct` *(OCR docs 03c, 04)*.
Because `-v $(pwd):…` mounts only the current species folder, a second species meant a second
terminal and the whole sequence again.

## Stage 2 — RepeatMasker

The lab notebook records the command as *(OCR doc 02)*:

```
RepeatMasker -lib RM_#$date/consensi.fa.classified -pa 8  Drosophila_ .fna file
```

`evidence/lab-scripts/shell/runMasker.sh` has since been recovered, and **it does not match**:

```bash
RepeatMasker -lib GFF_Files/Dataset_1_12_species/DROSOPHILA_PAULISTORUM_final.gff
```

No `-pa`, no genome FASTA, and `-lib` pointing at a gene annotation GFF rather than a repeat
library. As saved it could not have produced anything. See
[`pipeline/detailed/02-stage-reference.md`](pipeline/detailed/02-stage-reference.md) for what
that does and does not tell us.

## Stage 3 — pairing Cyp genes with TEs

Three scripts, run in order, **taking no arguments**. Paths are string literals at the top of
each file and were edited before every run:

```
python repeatOpp.py        # annotation GFF + Cyp gene list  -> filtered.gff
python Locate_TE.py        # filtered.gff + RepeatMasker .out -> GenesAffectedByTEs.txt
python CleanAnnasse.py     # collapses column 2 to a gene symbol -> DAnasse_TE_Cyp.txt
```

| Script | The literals that were edited |
|---|---|
| `repeatOpp.py` | `GFF`, `rgFile` |
| `Locate_TE.py` | `cypGene`, `TEs` |
| `CleanAnnasse.py` | `toClean`, `aliasToFind` |

The notebook's own procedure is three edit–save–run cycles per species, with the output
renamed by hand afterwards to `D_<species>GenesAffectedByTE.txt` *(OCR doc 02, step 3)*.
Twenty-nine species were processed this way; three of the twenty-nine filenames are
misspelled.

A TE counts as affecting a gene if it falls **entirely inside** the gene's span extended by
3,000 bp at each end. That number is a literal in `Locate_TE.py` and appears in no output
file.

## Stage 0b — gene renaming

`ReVamp_Final.py` and `NEW_Step_5_Replace_gff_Names_with_Dmelanogaster_1_9.py`, both run
without arguments, both with hardcoded Windows paths. ReVamp takes about ten minutes per
species and was run over every species column in the HOG table in one loop.

## Stages 4–6 — merge and compare

The four scripts in `evidence/analysis-scripts/` do take arguments. Their documented
invocations, from their own module docstrings:

```bash
python build_tfbs_te_gff.py \
    --te-file D_suzukiiGenesAffectedByTE.txt \
    --gff dsuzukii_annotation.gff3 \
    --fasta dsuzukii_genome.fa \
    --output combined_cyp_annotation_suzukii.gff3

python compare_te_cyp_exposure.py   --config te_cyp_species_config.ini \
    --output-csv te_cyp_summary.csv --output-report te_cyp_report.md --plot
python compare_te_cyp_cncc.py       --config te_cyp_species_config.ini
python compare_te_cyp_xenobiotic.py --config te_cyp_species_config.ini \
    --gene-list xenobiotic_resistance_cyp_genes.txt
```

> **As delivered these do not run.** The files are named `build_tfbs_te_gff 1.py`,
> `compare_te_cyp_exposure 1 1.py` and so on, and two of the comparison scripts do
> `import compare_te_cyp_exposure`, which cannot resolve against a filename with spaces. The
> config files they reference (`te_cyp_species_config.ini`,
> `xenobiotic_resistance_cyp_genes.txt`, and the three `*.example.*` templates) are not in the
> delivery either. The suffixes are Windows duplicate-file renames from round trips through
> zip and OneDrive, which is also how the scripts arrived.

## Stage 5 — JBrowse

Not a command. A person, clicking: open new genome, choose the FASTA adapter, name the
assembly after the species, add a track pointing at the processed annotation
*(OCR docs 02, 05)*. Sessions survive for three species only.

---

# Part 2 — What was run to check it

Everything below was run on **copies** made outside this repository, with only paths changed,
writing output outside the repository. That is the standing rule, and these are the commands
that obey it.

## Getting the source annotations

The species annotations the lab renamed come from Zenodo record 18453526, *Comparative gene
annotation and orthology assignments across 301 species of Drosophilidae* (Dhakad & Obbard).

```bash
mkdir -p ~/dl-staging && cd ~/dl-staging
curl -L -C - --retry 10 -o annotations.tar.gz \
  "https://zenodo.org/api/records/18453526/files/annotations.tar.gz/content"
md5sum annotations.tar.gz      # d7cd2d6d0b98b4d51036b05c619c590b, 1,755,436,625 bytes
mkdir -p annotations && tar xzf annotations.tar.gz -C annotations
gunzip -k annotations/gffs/DROSOPHILA_ARIZONAE_final.gff.gz
```

Zenodo throttles to roughly 1–2.5 MB/s regardless of how many connections you open, so allow
15–25 minutes. **Download to local disk**, not to a network mount — a download written
straight to the sshfs-mounted storage box stalled and left a truncated file, which is how that
rule came about.

## Re-running the gene-renaming step

```bash
# copy the script out, change only the four paths, then:
mkdir -p ~/dl-staging/test_run && cd ~/dl-staging/test_run
python /path/to/ReVamp_copy.py           # pandas 2.x, ~10 minutes per species
```

Which four paths, and how the output compares to the lab's own, is in
[`scripts/06-final-final-gff.md`](scripts/06-final-final-gff.md). Use pandas **2.x**: pandas 3
changes string dtype handling, and the originals were made in January 2026.

## Re-running the TE-locating step

Same pattern — path-only copies of `repeatOpp.py`, `Locate_TE.py` and `CleanAnnasse.py`, run
outside the repository against `evidence/te-locating-run/DA_Files/`. Re-running the last two
steps from the archived `filtered.gff` reproduces the archived `GenesAffectedByTEs.txt` and
`DAnasse_TE_Cyp.txt` exactly, once CRLF line endings are normalised.

## Comparing an output against the lab's

Line endings and stray tabs account for every difference that is *not* a renaming difference,
so normalise them before diffing:

```bash
diff <(tr -d '\r' < lab_output.gff) <(tr -d '\r' < rerun_output.gff) | head
```

## Environment notes

The system Python on the working machine had neither `pip` nor `venv`. pip was bootstrapped
into a scratch virtualenv outside the repository; pandas was pinned below 3 to match January
2026 behaviour. Nothing was installed into the repository, and no requirements file is
committed here — this repository has nothing to run.

---

## Where to read more

- **What each stage did** — [`pipeline/detailed/02-stage-reference.md`](pipeline/detailed/02-stage-reference.md)
- **The formats between stages** — [`pipeline/detailed/03-data-contracts.md`](pipeline/detailed/03-data-contracts.md)
- **What is broken** — [`pipeline/detailed/04-gaps-and-provenance.md`](pipeline/detailed/04-gaps-and-provenance.md)
- **The scripts line by line** — [`scripts/`](scripts/)
- **The artifacts themselves** — [`../evidence/README.md`](../evidence/README.md)
