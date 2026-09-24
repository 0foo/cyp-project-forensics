# Data lineage

Every data file in the archive, and what produced it.

## The *D. ananassae* worked example

`evidence/te-locating-run/` preserves one species end to end — every intermediate, in order.
It is the best available specification of what this stage did, because the files can be
diffed against each other.

```mermaid
flowchart TD
    A[("DA_Files/<br/>DROSOPHILA_ANANASSAE_final_withDmelNames.gff<br/>annotation, Cyp symbols already in Name=")]
    B[("AnalysisForAll/Reg_Gene_Full.txt<br/>96 lines — Cyp symbols<br/>+ 5 Dvir\/Dmoj\ ortholog IDs")]
    C[("DA_Files/<br/>Drosophila_ananassae.GCF_017639315.1.rm.fna.out<br/>RepeatMasker output")]

    A --> S1["<b>repeatOpp.py</b><br/>keep gene rows whose attrs<br/>contain a Cyp symbol"]
    B --> S1
    S1 --> D[("filtered.gff<br/>Cyp gene rows only")]

    D --> S2["<b>Locate_TE.py</b><br/>seqid match AND<br/>overlap within +/-3000 bp"]
    C --> S2
    S2 --> E[("GenesAffectedByTEs.txt<br/>col 2 = the whole GFF attribute blob")]

    E --> S3["<b>CleanAnnasse.py</b><br/>replace col 2 with the bare symbol"]
    B --> S3
    S3 --> F[("DAnasse_TE_Cyp.txt<br/>seqid TAB Cyp12e1 TAB RepeatMasker fields")]

    F -.->|"this is the --te-hits format"| G["build_tfbs_te_gff.py"]

    style F fill:#e8f5e9,stroke:#388e3c
```

The transformation `CleanAnnasse.py` performs is visible in one line. Before:

```
NC_057927.1	Name=Cyp12e1;ID=gene-G00000000064;Name_old=LOC6500252;dbxref=…	   13   28.7  1.4  4.5  NC_057927.1    846413   846481 …
```

After:

```
NC_057927.1	Cyp12e1	   13   28.7  1.4  4.5  NC_057927.1    846413   846481 …
```

That is the whole point of the third script: collapse a 300-character attribute string into
the bare gene symbol, because `build_tfbs_te_gff.py` reads column 2 as a symbol.

## The 29-species batch

`AnalysisForAll/` is the same three steps applied across species, with the *D. melanogaster*
intermediates left in place as the reference run.

```mermaid
flowchart LR
    subgraph REF["D. melanogaster reference run"]
        R1[("GFF/ + FilesFromMasker/")] --> R2[("step1Temp.gff")]
        R2 --> R3[("step2GenesAffectedByTEs.txt")]
        R3 --> R4[("output/D_melanogasterGenesAffectedByTE.txt")]
    end

    subgraph BATCH["output/ — 29 species"]
        O1["D_simulans…"]
        O2["D_sechelia…"]
        O3["D_willistoni…"]
        O4["… 26 more"]
    end

    R4 --- BATCH

    style R2 fill:#f5f5f5
    style R3 fill:#f5f5f5
```

`step1Temp.gff` and `step2GenesAffectedByTEs.txt` are the same artifacts as `filtered.gff`
and `GenesAffectedByTEs.txt` above, under batch-run names — confirming the three-step shape
was stable across both runs.

## The split upstream of the batch

The 29 tables did not all come down the same path. The annotation each one started from was
produced by one of **two different renaming scripts**, written independently by two people,
which do not agree with each other:

```mermaid
flowchart TD
    Z[("Zenodo annotations<br/>301 species, hog= attributes")]
    H[("HOG_OG_association_…_10_31.tsv")]

    Z --> D
    H --> D
    Z --> A
    H --> A

    D["ReVamp_Final.py  (Duy)<br/>rewrites ID=<br/>splits cells on ','"]
    A["NEW_Step_5_… (Ayush)<br/>rewrites Name=<br/>parses cells properly"]

    D --> DO[("change_SPECIES_final_final.gff<br/>25 files in evidence/lab-data/renamed-annotations/")]
    A --> AO[("SPECIES_final_withDmelNames.gff<br/>1 truncated copy in DA_Files/")]

    DO -->|"19 species"| OUT[("AnalysisForAll/output/<br/>29 tables")]
    AO -->|"7 species"| OUT
    UNK["eugracilis, paulistorum (empty)<br/>melanogaster (no renaming needed)"] -.->|"3, undeterminable"| OUT

    style D fill:#ffe9e0,stroke:#c05a2a
    style DO fill:#ffe9e0,stroke:#c05a2a
    style A fill:#e6f7e6,stroke:#4a9a4a
    style AO fill:#e6f7e6,stroke:#4a9a4a
```

The red path loses roughly 7% of orthologous genes — every gene in an orthogroup cell that
lists more than one — so the 19 tables on that branch under-count Cyp loci in exactly the
multi-copy gene families the study is about. Neither the tables nor anything else in the
archive records which branch a given species took; the attribution above was reconstructed by
asking, for every TE row, which renamed annotation could account for it.

Full working: [`../scripts/06-final-final-gff.md`](../scripts/06-final-final-gff.md).

## Reference gene lists

```mermaid
flowchart TD
    A[("Cyp_stable_genes_Good_et_al_2014.txt<br/>29 symbols")]
    B[("Cyp_unstable_genes_Good_et_al_2014.txt<br/>46 symbols")]
    C[("Reg_Gene_Full.txt<br/>96 lines")]

    A --> C
    B --> C
    C -->|"used as the gene filter"| D["repeatOpp.py<br/>CleanAnnasse.py"]

    note["29 + 46 = 75, but Reg_Gene_Full has 96 lines.<br/>The extra ~21 include 5 ortholog IDs<br/>(Dvir\GJ21722, Dmoj\GI21254, …)<br/>which both scripts skip via startswith('D')"]
    C -.- note

    style note fill:#fff8e1,stroke-dasharray: 3 3
```

The `startswith("D")` skip in `repeatOpp.py` and `CleanAnnasse.py` exists to drop those
`Dvir\`/`Dmoj\` prefixed ortholog identifiers. It is a blunt instrument — it would also
silently drop any Cyp symbol beginning with a capital D — but no such symbol exists in
these lists.

"Stable" and "unstable" refer to Good et al. 2014's classification of Cyp gene copy-number
stability across *Drosophila*. Both lists are merged for filtering; the distinction is not
used by any surviving script.

## What is missing

```mermaid
flowchart LR
    A["evidence/analysis-scripts/"] -.->|"needs"| B["species_config.example.ini"]
    A -.->|"needs"| C["te_cyp_species_config.example.ini"]
    A -.->|"needs"| D["xenobiotic_resistance_cyp_genes.example.txt"]

    style B fill:#ffebee,stroke:#c62828,stroke-dasharray: 4 3
    style C fill:#ffebee,stroke:#c62828,stroke-dasharray: 4 3
    style D fill:#ffebee,stroke:#c62828,stroke-dasharray: 4 3
```

All four scripts reference these three example files by name in their docstrings, help text
and error messages. **None of them are in the archive** — nor are the real configs those
templates were for, which means the exact species-to-exposure-group assignment the lab used is
not recorded anywhere. The formats themselves are reconstructable, and are specified in
[`../pipeline/detailed/03-data-contracts.md`](../pipeline/detailed/03-data-contracts.md).
