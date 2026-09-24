# Making the `final_final` GFFs

How `change_<SPECIES>_final_final.gff` was produced: each species' gene annotation, with its
gene IDs swapped for the *D. melanogaster* gene symbol of the same orthogroup. This is the
**gene-renaming step (stage 0b)**, and it is the part of the pipeline this investigation
established most completely — the code was recovered, re-run, and its output diffed against
the lab's own (see [Verification](#verification)).

It is also where the investigation found the defect that most affects results.

## The short version

Two people wrote this step, independently, and their scripts do not agree:

| | **Duy** | **Ayush** |
|---|---|---|
| Script | `ReVamp_Final.py` | `NEW_Step_5_Replace_gff_Names_with_Dmelanogaster_1_9.py` |
| Folder, per the lab log | `Gff_Dataset#2`, 7/9/2026 | `Gff_Dataset#1`, 5/7/2026 |
| Output naming | `change_<SPECIES>_final_final.gff` | `<SPECIES>_final_withDmelNames.gff` |
| Method | `str.replace` over each whole line, once per dictionary key | parse the attribute column, rewrite fields |
| Attribute rewritten | `ID=` (and `Parent=` to match) | `Name=` |
| Multi-gene orthogroup cells | **silently skipped** | parsed correctly |
| Short gene symbols | **corrupt surrounding text** | unaffected |

Four consequences, each established below:

1. **`ReVamp_Final.py` leaves about 7% of orthologous genes un-renamed.** Orthogroup cells
   holding several genes are stored quoted and space-separated
   (`"gene-G00000006376, gene-G00000006377"`); the script splits on a bare comma, so neither
   fragment matches and *no* gene in that cell is renamed. For *D. arizonae*: **788 of
   11,063**. → [`gene_Getter`](#gene_getter-23--which-dmel-symbol-does-each-gene-get)
2. **The losses concentrate on exactly the genes the study cares about.** Genes sharing an
   orthogroup cell are a species' multiple copies of one gene, so the damage lands on
   multi-copy Cyp clusters. On *D. ananassae*: 57 Cyp loci found instead of 91, 366 Cyp/TE
   pairs instead of 465, and *Cyp28a5* and *Cyp6a19* gone entirely. →
   [Effect downstream](#effect-downstream-final_final-vs-_withdmelnames-d-ananassae)
3. **Both versions were used on real species.** Of the 29 finished tables, **19 came from
   Duy's output and 7 from Ayush's**; the remaining three cannot be determined. →
   [Which version each finished table came from](#which-version-each-finished-table-came-from)
4. **So the cross-species comparison is not comparing like with like.** It sets 19 species
   whose Cyp gene sets are systematically short against 7 whose are not, and the shortfall
   scales with gene family size — the very property the study is testing against insecticide
   exposure.

Nothing in the archive shows anyone noticing. The lab log names both scripts and both
datasets without ranking them; the lab notebook's procedure points at Duy's *(OCR doc 02)*;
and the one worked example that survives end to end was built with Ayush's.

---

The 26 finished files are in
[`../../evidence/lab-data/renamed-annotations/`](../../evidence/lab-data/renamed-annotations/)
— 25 of them, at least; the *D. melanogaster* one is 13.8 GB and is held outside the
repository. `final_final.7z`, the archive they came in, is in
[`../../evidence/lab-archives/`](../../evidence/lab-archives/).

**The name does not mean "final".** The inputs are already called `<SPECIES>_final.gff`;
the script prefixes `change_` and appends another `_final` (`ReVamp_Final.py:146-147`).

---

## The chain at a glance

```
Zenodo 18453526 ── annotations.tar.gz ──► gffs/<SPECIES>_final.gff.gz   (301 species)
       │                                            │
       └─ orthogroup tables ──► HOG_OG_association*.tsv                   │
                                    │                                   │
     Step_1_Replace_RNA_identifiers_with_gene_names_Redo.py  ◄──────────┤
        (mRNA IDs in the HOG table → gene IDs, via each GFF's Parent=)  │
                                    │                                   │
     Step_2_Remove_Duplicate_gene_names_10_31.py                        │
                                    │                                   │
     hog-tables/HOG_OG_association_gene_names_without_duplicates_10_31.tsv │
                    │                          │                        │
     make_Dmel_output.py                       │                        │
                    │                          │                        │
            Dmel_output.tsv                    │                        │
                    └──────────► ReVamp_Final.py ◄──────────────────────┘
                                       │
                     change_<SPECIES>_final_final.gff
```

All scripts named here live in
[`../../evidence/lab-scripts/`](../../evidence/lab-scripts/) — the renaming scripts under
`gene-renaming/`, the table-building steps under `orthogroup-tables/`. The tables themselves
are in [`../../evidence/lab-data/hog-tables/`](../../evidence/lab-data/hog-tables/), and
`Dmel_output.tsv` — which is a **reconstruction**, not a lab original — is in
[`../../evidence/reconstructed/`](../../evidence/reconstructed/). Line references below point
at those files.

---

## Inputs

### 1. The species annotations — `<SPECIES>_final.gff`

From Zenodo record [18453526](https://zenodo.org/records/18453526), *Comparative gene
annotation and orthology assignments across 301 species of Drosophilidae*:

| | |
|---|---|
| URL | `https://zenodo.org/records/18453526/files/annotations.tar.gz?download=1` |
| Size | 1,755,436,625 bytes |
| md5 | `d7cd2d6d0b98b4d51036b05c619c590b` |
| Contents | `gffs/<SPECIES>_final.gff.gz`, one per species, 301 total |

Zenodo serves it at roughly 1–2.5 MB/s regardless of client or number of connections, so
allow 15–25 minutes. `curl -C -` resumes a broken download.

These files **already carry the orthology**: mRNA records have `dmel_orthologs=` and
`hog=N1.HOG…` attributes (12,325 of arizonae's mRNAs). Those attributes come from the
published dataset, not from anything the lab ran.

The lab's working copies lived in a folder called `gff_fixed/`. They are *not* byte-identical
to Zenodo's — see [Verification](#verification) — but the differences do not affect renaming.

### 2. The HOG table — `lab-data/hog-tables/HOG_OG_association_gene_names_without_duplicates_10_31.tsv`

One row per hierarchical orthogroup (HOG), one column per species (308 columns, including
`HOG`, `OG` and `Gene Tree Parent Clade`). Each cell holds that species' genes in the HOG,
but **what identifies a gene varies by species**: gene IDs for NCBI-annotated species
(`gene-G00000008057`, arizonae), gene names for CAT-annotated ones (`LOC6575132`, aldrichi),
and gene symbols for `DROSOPHILA_MELANOGASTER` (`Myo81F`, `e`, `a`…). ReVamp's text
replacement therefore rewrites `ID=` in some species and `Name=` in others.

Built in two steps:

- **`Step_1_Replace_RNA_identifiers_with_gene_names_Redo.py`** reads the raw
  `HOG_OG_association_*.tsv` (mRNA IDs per cell) and each species' `gff_fixed/*_final.gff`,
  maps every mRNA to its gene through `Parent=` (lines 57, 63, 66), and writes the gene IDs
  back into the table. mRNAs it cannot map are written as `<id>_NOT_FOUND` (line 86).
  *D. melanogaster* is handled separately, from `Dmel_HOG_association.tsv` (lines 36, 74).
- **`Step_2_Remove_Duplicate_gene_names_10_31.py`** collapses duplicate gene names within a
  cell (several mRNAs of one gene all map to the same gene ID).

Step 2 imports its paths from a `config.py` that was not kept, and Step 1's input
`Dmel_HOG_association.tsv` is nowhere in the archive either. **Neither step can be re-run as
it stands.** The table they produced is present, and it is what `ReVamp_Final.py` reads — so
the chain is verifiable from the table forward, and unrecoverable behind it.

Further back still, `evidence/lab-environment/bash_history` shows the original OrthoFinder
post-processing being driven by four scripts — `Grab_data_Atallah_12_2.py`,
`Rewrite_gene_names.py`, `Remove_duplicates_Atallah.py`, `Bulk_gffread.py` — none of which
exist anywhere. The `Step_*` scripts above do the same kind of work and produced the surviving
tables, but they are not those files.

**Two versions exist.** `ReVamp_Final.py` reads the `_10_31` table; the current Step 1 writes
a `_1_9` one. The `final_final` files were made from `_10_31`.

### 3. The Dmel lookup — `Dmel_output.tsv`

Two columns, `hog` and `genes`: every HOG that has a *D. melanogaster* gene, and that gene's
symbol(s). 12,151 rows; 710 hold more than one symbol, comma-separated.

**The lab's original was never kept.** `make_Dmel_output.py` — written during this
investigation, not by the lab — rebuilds the file from the HOG table by copying the `HOG` and
`DROSOPHILA_MELANOGASTER` columns for non-empty rows (lines 13–14). Both the script and its
output live in [`../../evidence/reconstructed/`](../../evidence/reconstructed/) for that
reason.

The rebuild reproduces the *D. arizonae* output exactly, so the two are equivalent at least
for that species. That is an equivalence, not an identity, and every conclusion below that
depends on `Dmel_output.tsv` inherits the caveat.

---

## `ReVamp_Final.py`, step by step

The script loops over every species column in the HOG table (`:157`), skips any whose output
already exists (`:165-173`), and runs four functions.

### `gene_Getter` (`:23`) — which Dmel symbol does each gene get?

Builds `HOG → cell` for this species (`:28-31`), then walks `Dmel_output.tsv` and keeps each
HOG that has both a Dmel symbol and a gene in this species. Cells with several genes are
split on `,` and exploded to one row per gene (`:47-48`).

> **Defect — 7% of genes are silently skipped.** Multi-gene cells are written with quotes
> and a space after each comma: `"gene-G00000006376, gene-G00000006377"`. Splitting on `,`
> leaves `"gene-G00000006376` and ` gene-G00000006377"`, which never match anything in the
> GFF. For arizonae that is **788 of 11,063** orthologous genes left with their original ID.

### `anno_Cleaner` (`:52`) — collect gene attributes

Reads the GFF and keeps column 9 of every `gene` line (`:65`). Lines that do not split into
exactly 9 tab-separated fields are dropped (`:62`).

### `HOG_to_Parent` (`:74`) — match genes to attribute strings

Builds an inverted index from every token in those attribute strings (`:84-88`) and looks up
each species gene in it. The result has one row per (Dmel symbol, species gene) pair.

The matched attribute is carried along but **never used** — `ReplaceinAnno` reads only the
first two columns. Genes with no match are kept too (with `attribute = NA`), so this step
changes nothing about the output. It is safe to ignore when reasoning about results.

### `ReplaceinAnno` (`:135`) — rewrite the file

Builds `{species gene → Dmel symbol}` (`:141`, `:144`), then, **for every line of the GFF,
runs `str.replace` once per dictionary entry** (`:152`).

What that does in practice, for arizonae:

- Only `ID=` and `Parent=` values change: 10,274 `gene` IDs and 16,259 `Parent=` references
  (`ID=gene-G00000000002` → `ID=Myo81F`, and every child's `Parent=` along with it), 26,533
  lines in all. Parent/child links stay consistent. No duplicate gene IDs result.
- A multi-symbol Dmel entry is inserted verbatim, commas and all: `ID=Odjl,dj,CG1792`.

> **Defect — substring replacement corrupts text when keys are short.** There is no word
> boundary. For arizonae the keys are fixed-width IDs (`gene-G` + 11 digits), so nothing else
> is hit. For **D. melanogaster** the keys are gene *symbols*, some one or two letters long
> (`a`, `e`, `ab`), and replacements also chain — a later key can rewrite an earlier result.
> `genome` becomes `genom,nom,ouibe` in 5 places in
> `change_DROSOPHILA_MELANOGASTER_final_final.gff`. Check any species whose HOG column holds
> symbols rather than `gene-G…` IDs.

It is also slow — ~10,000 keys × ~317,000 lines — **about 10 minutes per species**.

---

## Reproducing it

This section is here so the [verification](#verification) below can be repeated and checked,
not because the step needs running again.

**`ReVamp_Final.py` and everything under `evidence/` is an artifact. Do not edit it, fix it,
or write output next to it.** To re-run the step, copy the script somewhere else, change only
the paths in the copy, and write output outside the repository.

The script has hardcoded Windows paths (`D:/CYP_Gene_Project/…`, lines 6, 11, 161, 165) and
needs `pandas`. Use pandas **2.x**: that is what the originals were made with, and pandas 3
changes string dtype handling.

1. **Download and unpack the annotations to local disk** (not onto a network mount):

   ```bash
   mkdir -p ~/dl-staging && cd ~/dl-staging
   curl -L -C - --retry 10 -o annotations.tar.gz \
     "https://zenodo.org/api/records/18453526/files/annotations.tar.gz/content"
   md5sum annotations.tar.gz        # d7cd2d6d0b98b4d51036b05c619c590b
   mkdir -p annotations && tar xzf annotations.tar.gz -C annotations
   gunzip -k annotations/gffs/<SPECIES>_final.gff.gz
   ```

2. **Make a copy of the script outside the repository** and change only these paths in the
   copy:

   | Line | Set to |
   |---|---|
   | 6 `DmelPath` | `evidence/reconstructed/Dmel_output.tsv` (the rebuild — see above) |
   | 11 `hogogPath` | `evidence/lab-data/hog-tables/HOG_OG_association_gene_names_without_duplicates_10_31.tsv` |
   | 161 (in `flySpeciesPath`) | the folder holding the unpacked `<SPECIES>_final.gff` files |
   | 165 `checkPoint` | `"change_" + names + "_final_final.gff"` (current directory) |

   To do one species, replace `for names in flyName:` (line 157) with
   `for names in ["DROSOPHILA_ARIZONAE"]:` in the copy.

3. **Run the copy** from a working directory outside the repository:

   ```bash
   mkdir -p ~/dl-staging/test_run && cd ~/dl-staging/test_run
   python /path/to/ReVamp_copy.py
   ```

   It prints each species name, writes `change_<SPECIES>_final_final.gff` to the current
   directory, and skips species whose output already exists — delete an output to redo it.
   Species with no annotation file print `Annotation not found`.

`ReVamp_Final_copy_1_10.py` is an older copy. It has a bug (`cleanedAnno` for `cleanAnno`,
line 79) and names outputs differently. Do not use it.

---

## Verification

Re-run on 2026-09-24 for **D. arizonae** (the smallest of the 26), starting from the Zenodo
annotation, and compared with
`lab-data/renamed-annotations/change_DROSOPHILA_ARIZONAE_final_final.gff`:

| | Original | Re-run |
|---|---|---|
| Lines | 317,256 | 317,256 |
| Line endings | CRLF (made on Windows) | LF |
| Lines changed from input | 26,533 | 26,533 |

After normalising two formatting differences, **the files are identical line for line**:

1. **Line endings** — CRLF vs LF.
2. **Tabs inside column 9** — on 19,458 `mRNA` lines the original has tabs where Zenodo has
   spaces, inside free-text attributes (`Supporting⇥evidence⇥includes…`). `ReVamp_Final.py`
   never touches whitespace, so these tabs were already in the lab's `gff_fixed` copy. They
   give those lines more than 9 columns, which is invalid GFF3 and will trip strict parsers.

Neither difference is in the renaming. The renaming logic reproduces exactly.

---

## Effect downstream: `final_final` vs `_withDmelNames` (D. ananassae)

Two renaming scripts exist (see the next section), and the one worked example of the next
stage — `evidence/te-locating-run/`, which pairs Cyp genes with nearby TEs — was run on
Ayush's `_withDmelNames` output, not on a `final_final` file. To see whether the choice
matters, both versions of *D. ananassae* were run through that stage on 2026-09-24, using
path-only copies of `repeatOpp.py`, `Locate_TE.py` and `CleanAnnasse.py` and the archived
RepeatMasker `.out`.

**Baseline.** The archived `DA_Files/DROSOPHILA_ANANASSAE_final_withDmelNames.gff` is
**truncated** — 4,330 lines, one chromosome, ending mid-line (`NC_057927.1⇥Gno`) — so it
cannot be what the archived results were made from; they span 6 chromosomes. The archived
`filtered.gff` (166 lines) is, however, `repeatOpp.py`'s output from the full file. Re-running
`Locate_TE.py` and `CleanAnnasse.py` from it reproduces the archived
`GenesAffectedByTEs.txt` and `DAnasse_TE_Cyp.txt` exactly, apart from CRLF line endings.

**`final_final` side.** Built with `ReVamp_Final.py` (path-only copy) from the Zenodo
annotation — ananassae is not among the 26 renamed species — then run through the same three
scripts.

| (unique rows) | `_withDmelNames` (as archived) | `final_final` |
|---|---|---|
| Cyp gene loci found | 91 | 57 |
| Cyp gene / TE pairs | 465 | 366 |
| Distinct Cyp names | 50 | 48 |

The `final_final` result is a **strict subset**: every locus and TE row it finds is also in
the archived result, with the same Cyp name. Nothing is extra or conflicting.

**All 34 missing loci are the quoted multi-gene cell defect** described under `gene_Getter`
above. In such a cell *no* gene is renamed, so each keeps its `gene-G…` ID and `repeatOpp.py`
never sees a Cyp name. Ayush's script parses those cells correctly.

13 of the 50 Cyp genes lose TE pairs; two disappear entirely:

| Gene | `_withDmelNames` | `final_final` |
|---|---|---|
| Cyp309a2 | 37 | 17 |
| Cyp313a1 | 19 | 2 |
| Cyp4e3 | 36 | 20 |
| Cyp4p1 | 10 | 1 |
| Cyp28d1 | 11 | 3 |
| Cyp4ac1 | 11 | 5 |
| Cyp9b1 | 15 | 9 |
| Cyp6d5 | 14 | 9 |
| Cyp9c1 | 9 | 5 |
| Cyp12d1 | 9 | 7 |
| Cyp6a17 | 2 | 1 |
| **Cyp28a5** | 4 | **0** |
| **Cyp6a19** | 1 | **0** |

The losses concentrate in genes with several ananassae copies (the Cyp313a cluster
especially), because those are the HOGs whose cells list several genes.

**Implication:** any species whose TE table was built from a `final_final` file under-counts
Cyp genes in multi-copy orthogroups. The next section works out which species those are.

### Which version each finished table came from

Not recorded anywhere, but recoverable from the tables themselves (analysis of 2026-09-24,
read-only). Each row of a `D_<species>GenesAffectedByTE.txt` holds a TE's position and the
Cyp name it was credited to. For every row we asked which renamed annotation contains a gene
with that Cyp name within ±3 kb of the TE — the lab's own `change_<SPECIES>_final_final.gff`
where one exists, and a model of Ayush's full parse of the HOG table otherwise.

Two things make this harder than it looks:

- **The HOG table's keys differ by species.** For NCBI-annotated species a cell holds gene
  IDs (`gene-G00000000544`); for CAT-annotated species it holds gene names (`LOC6575132`),
  and ReVamp rewrites `Name=` instead of `ID=`.
- **Many CAT annotations already carry Dmel symbols** (`Name=Cyp4c3`, from
  `source_gene_common_name`), so most Cyp genes match in *either* version. Only the loci that
  one version names and the other does not can tell them apart.

| Group | Species | Rows only Ayush's version explains | Loci only Ayush's version names → rows near them |
|---|---|---|---|
| **Built from `final_final` (ReVamp)** | aldrichi, algonquin, anomalata, arawakana, arizonae, athabasca, elegans, helvetica, mauritiana, mayaguana, miranda, pandora, santomea, sulfurigaster (all four), suzukii, tropicalis | **0** in every species | 9–108 per species, 516 in total → **0 rows** |
| **Not built by ReVamp** (no `final_final` file exists) | erecta, mojavensis, pseudoobscura, sechellia, simulans, subpulchrella, willistoni | 35–178 per species | 10–21 per species → those same 35–178 rows |

In the second group, loci that only a full parse names contribute dozens of TE rows per
species; in the first, 516 such loci contribute none. TEs (simple repeats especially) sit
within 3 kb of almost every gene, so that silence is not chance: **the first group's tables
were built from the `final_final` files and inherit ReVamp's missing loci.** The second
group's were built from a renaming that parses multi-gene cells correctly — consistent with
Ayush's `_withDmelNames` files, which is also what the archived ananassae example used.

Not classifiable: `D_eugracilis…` and `D_paulistorum…` are **empty** (0 rows);
`D_melanogaster…` needs no ortholog renaming, so both versions agree. The mapping from table
names to species also absorbs the lab's typos (`mauritania`, `pseudodoobscura`, `sechelia`,
`sulfirigaster`).

**Consequence for stage 6:** the finished tables mix two renaming methods. Cross-species
comparisons set 19 ReVamp-built species, which under-count Cyp loci in multi-copy
orthogroups, against 7 fully parsed ones.

The small `evidence/lab-data/te-tables/D_Ananassae_GenesAffectedByTE.txt` (98 rows, 23 unique,
two genes) is an early partial run; all its rows are in the finished table.

---

## Relation to `NEW_Step_5_…_1_9.py`

`NEW_Step_5_Replace_gff_Names_with_Dmelanogaster_1_9.py` (Ayush, Gff_Dataset#1) does the same
job by parsing and rewriting attributes field by field (`rewrite_gff_attributes`,
`process_gff_line`) instead of raw text replacement. That avoids both defects above: no
substring corruption, and multi-gene cells parse correctly.

Which dataset the lab *intended* to use was never recorded, and the documents do not settle it
— the log describes both without ranking them, and the notebook's procedure points at Dataset
#2 *(OCR doc 02)*. What the data settles is that **both were used**, on different species, and
that nothing in the archive shows anyone noticing. See
[`04-gaps-and-provenance.md`](../pipeline/detailed/04-gaps-and-provenance.md), G2 and G4.
