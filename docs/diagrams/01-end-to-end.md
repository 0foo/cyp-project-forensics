# End to end

The pipeline as it ran, on one page. Stage names here are the lab's own work; the boxes are
labelled with where the evidence for each now sits.

## The whole pipeline

```mermaid
flowchart TD
    subgraph S1["Stages 1-2 — run by hand in a container"]
        direction TB
        A["Genome FASTA<br/>one per species"]
        A --> B["spinContainer.sh<br/>interactive dfam/tetools shell"]
        B --> C["BuildDatabase<br/>typed by hand"]
        C --> D["RepeatModeler<br/>8-26 h per genome"]
        D --> E[["consensi.fa.classified<br/>de novo TE library"]]
        E --> F["RepeatMasker -lib<br/>command known only from<br/>the notebook and write-up"]
    end

    subgraph GAP["Stage 0 — orthogroup table + renaming"]
        direction TB
        G["Gene annotation<br/>Zenodo, already carrying hog= attributes"]
        H["ReVamp_Final.py  OR<br/>NEW_Step_5_... — two scripts,<br/>two different results"]
    end

    F --> I[["sample.rm.out<br/>every repeat, located"]]
    G --> H
    H --> J[["annotation.gff<br/>Cyp symbols in Name="]]

    subgraph S2["Stage 3 — evidence/te-locating-run/"]
        direction TB
        K["repeatOpp.py<br/>keep only Cyp gene rows"]
        L["Locate_TE.py<br/>overlap within +/-3 kb"]
        M["CleanAnnasse.py<br/>collapse attrs to bare symbol"]
        K --> L --> M
    end

    J --> K
    I --> L
    M --> N[["D_species GenesAffectedByTE.txt<br/>seqid TAB gene TAB RepeatMasker fields"]]

    subgraph S3["Stage 4 — evidence/analysis-scripts/"]
        direction TB
        O["build_tfbs_te_gff.py"]
        P["FIMO + JASPAR + CncC:Maf-S ARE"]
        O --> P
    end

    N --> O
    J --> O
    A --> O
    P --> Q[["combined.gff3<br/>gene / mRNA / exon / intron<br/>mobile_genetic_element<br/>TF_binding_site"]]

    Q --> R["JBrowse 2<br/>GFF3Tabix track"]

    subgraph S4["Stage 6 — evidence/analysis-scripts/"]
        direction TB
        S["compare_te_cyp_exposure.py<br/>all Cyp genes"]
        T["compare_te_cyp_cncc.py<br/>CncC-proximal subset"]
        U["compare_te_cyp_xenobiotic.py<br/>curated resistance list"]
        S -.->|"imports parsing + stats"| T
        S -.->|"imports parsing + stats"| U
    end

    Q --> S
    Q --> T
    Q --> U
    S --> V[["CSV + markdown report + PNG"]]
    T --> V
    U --> V

    style GAP stroke-dasharray: 6 4
    style S1 fill:#eef6ff,stroke:#4a7fb5
    style S2 fill:#fff6ee,stroke:#b5814a
    style S3 fill:#f0ffee,stroke:#5ab54a
    style S4 fill:#f6eeff,stroke:#8a4ab5
```

## The two seams

**The dashed box, stage 0, is where two people diverged.** The annotation feeding stage 3 has
to carry *D. melanogaster* Cyp symbols in `Name=`, and two scripts produced that: Duy's
`ReVamp_Final.py` and Ayush's `NEW_Step_5_…`. They do not agree, nothing ever chose between
them, and the 29 finished tables are a mix — 19 from one, 7 from the other. See
[`../scripts/06-final-final-gff.md`](../scripts/06-final-final-gff.md).

**The RepeatMasker box is where the sources conflict.** `runMasker.sh` has been recovered and
does not match the lab notebook *(OCR doc 02)* or the write-up *(OCR doc 05)*, which agree
with each other. The diagram shows what those two describe, because that is what is consistent
with the surviving `.out` files. See
[`../pipeline/detailed/02-stage-reference.md`](../pipeline/detailed/02-stage-reference.md).

## Where the surviving data sits on that path

```mermaid
flowchart LR
    B["evidence/te-locating-run/DA_Files/<br/>D. ananassae inputs"]
    C["evidence/te-locating-run/<br/>filtered.gff, GenesAffectedByTEs.txt,<br/>DAnasse_TE_Cyp.txt"]
    D["AnalysisForAll/output/<br/>29 species, TE-hits tables"]
    E["evidence/analysis-scripts/<br/>scripts only, no data"]
    F["evidence/lab-data/renamed-annotations/<br/>25 renamed annotations"]

    F -.->|"the other branch of stage 0"| D
    B -->|"worked example"| C
    C -->|"same 3 steps, batched"| D
    D -.->|"would feed"| E

    style E fill:#f0ffee
    style F fill:#fff6ee
```

The archive contains **one fully worked example** (*D. ananassae*, every intermediate
preserved), **29 finished TE-hits tables** and **25 renamed annotations** — but no combined
GFF3 and no comparison output at all. Stages 4 and 6 left nothing behind: their inputs
survive, their outputs do not, and the lab's own results spreadsheet (`TEandTFdata.xls`) is
not in the archive either.
