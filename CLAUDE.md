# Project history (Claude Code sessions)

**This repository is a forensic investigation, not a project.** It began life as an ordinary project repo holding the CYP/transposable-element pipeline; on 2026-09-24 its purpose changed entirely. It now exists to trace down and understand how a poorly documented lab pipeline worked. Nothing here is meant to be run, fixed or extended — the runnable version lives in the separate `cyp-te-pipeline` repository. See [`README.md`](README.md) for the current entry point.

This folder was called `~/projects/cyp-project` until 2026-09-24 about 17:06 CDT. It was renamed to `~/projects/cyp-project-forensics` during that day's work. This file rebuilds, from the saved Claude Code transcripts, what happened in the folder under both names.

**Sources:**
- Transcripts in `~/.claude/projects/-home-nick-projects-cyp-project/` (6 sessions), `-home-nick-projects-cyp-project--git/` (1 session, started inside `.git/`) and `-home-nick-projects-cyp-project-forensics/` (post-rename sessions).
- `git log`.

**Times:** local time (CDT, UTC−5) unless marked otherwise. Some sessions ran at the same time as each other.

**Paths:** the session-by-session narrative below uses the paths as they were *at the time*. The repository was reorganised at the end of 2026-09-24 (session 10); the old→new mapping is in [`evidence/README.md`](evidence/README.md).

**Not covered:** no transcripts survive for the work behind the September 13–15 commits. That part is known only from git.

## Standing rules set during this work

- **The lab's files are forensic artifacts.** Never modify, fix or regenerate anything under `evidence/`. Run copies with only the paths changed, kept outside the artifact folders, and write outputs outside them too. Report defects as findings, not as fixes. (Set 2026-09-24 14:14: "this whole thing is an artifact and should not be changed. This is pure forensics.")
- **This is a forensics repo, not a project repo.** Documentation is an investigation report: what the lab's code did, what was reconstructed, what is uncertain, and where the evidence sits. It is not a user manual, and reconstructed behaviour is never presented as working software. (Set 2026-09-24, during the reorganisation: "it is no longer a project repo it's purely forensics for tracing down and understanding how a poorly documented pipeline worked.")
- **`/mnt/storagebox` is storage only.** It's a Hetzner Storage Box mounted over sshfs. Download and process on local disk, and rsync finished files there afterwards. (Set 2026-09-24 14:35, after a download written straight to the box stalled and left a truncated file.)

---

## Before the transcripts: git history

| Commit | Date | Author | What |
|---|---|---|---|
| `215fbe8` | 2026-09-13 06:55 | Nicholas Kiermaier | "save state": 57 files, ~1.44 M lines (the initial import of lab material) |
| `d01da9c` | 2026-09-13 07:03 | Nicholas Kiermaier | "save state": 22 files |
| `3747e24` | 2026-09-13 15:00 +0200 | Nick Kiermaier | Add pipeline documentation and OCR transcriptions (31 files) |
| `7f02c33` | 2026-09-13 15:11 +0200 | Nick Kiermaier | Add RepeatMasker as a second stage in the worker automation |
| `871944e` | 2026-09-13 15:38 +0200 | Nick Kiermaier | Refresh documentation and add `docs/commands.md` |
| `be73ebe` | 2026-09-15 09:26 | Nicholas Kiermaier | "save state": 5 files, 1,398 deletions (the RepeatModeler automation was split out into `~/projects/repeat-modeler-automation`) |
| `e1ce8a3` | 2026-09-24 17:09 | Nick Kiermaier | Add `to_organize` lab artifacts and the `final_final` GFF documentation (117 files). Pushed to `origin/master`. |

---

## 2026-09-24: session by session

### 1. What comes after RepeatMasker? (11:25–11:58, session `6b4ee4df`)

- **Question:** what are the next step or two after RepeatMasker finishes?
- **Answer:** Stage 3 in `pipeline-scripts-output/`: `repeatOpp.py` → `Locate_TE.py` → `CleanAnnasse.py`. Then rename the output to `D_<species>GenesAffectedByTE.txt` and build a combined GFF3 with `analysis-pipeline/build_tfbs_te_gff.py`.
- **Points raised:**
  - All three scripts have hardcoded Windows paths.
  - `repeatOpp.py` needs a GFF whose genes already carry *D. melanogaster* names.
  - A TE counts if it lies within 3 kb of a gene.
  - Every repeat class is counted, including simple repeats.
- **User's reply:** "there's another step to clean the gff". The session ended there.

### 2. Unpacking the lab archives and finding what makes `final_final` (12:25–12:48, session `d8bc0f60`)

**Unpacking:**
- Extracted `python.7z` (32 scripts) into `python/`, then renamed that folder to **`to_organize/`**.
- Inside `to_organize/`, extracted:
  - `tosend.7z`: 42 files. 32 were identical to the scripts already there; 10 were new `*_GenesAffectedByTE*.txt` results, including "Terry's edits".
  - `final_final.7z`: 26 `change_<SPECIES>_final_final.gff` files, about 15 GB.
- Moved the `tosend/` files into `to_organize/`. None conflicted. Then deleted the empty `tosend/`.

**What makes `final_final`:**
- **The script is `to_organize/ReVamp_Final.py`** (Duy's). It renames each species' gene IDs to Dmel names by HOG.
- **Inputs:**
  - `Dmel_output.tsv`
  - `HOG_OG_association_gene_names_without_duplicates_10_31.tsv`
  - `Anno_Duy/gff_fixed/<SPECIES>_final.gff`
- **Where the name comes from:** the input is already called `<SPECIES>_final.gff`, and the script adds `change_` in front and another `_final` at the end.
- **Older versions:** `ReVamp_Final_copy_1_10.py` is an older copy. Because of a bug, it names its output with a single `_final`. `Part5_Final.py`, `Step5.py` and `NEW_Step_5_…_1_9.py` are earlier attempts at the same renaming step.
- **The melanogaster file:** `change_DROSOPHILA_MELANOGASTER_final_final.gff` is 13.8 GB. The suspected cause is the plain-text `str.replace`.
- **`Dmel_output.tsv`** can't be downloaded. It looks like `gene_Getter("DROSOPHILA_MELANOGASTER")` from `Part5_Final.py`, saved as a TSV (the lost `Final_Step5.py`).

### 3. SSH config for GitHub (12:42–12:45, session `cfa0cde2`, run from `.git/`)

- **Change:** added a `Host github.com` entry to `~/.ssh/config` using `~/.ssh/0foo` with `IdentitiesOnly yes`.
- **Backup:** the old config is at `~/.ssh/config.bak`.
- **Test:** `ssh -T` authenticates as **0foo**.

### 4. HOG tables, rebuilding `Dmel_output.tsv`, finding the annotations (13:05–14:02, session `134ecbc9`)

**HOG tables:**
- Extracted `to_organize/hog_og.7z` into `hog_og/`: 20 versions of `HOG_OG_association*`, about 1 GB.

**Rebuilding `Dmel_output.tsv` (Claude wrote these files):**
- **Created `to_organize/make_Dmel_output.py`**, using the standard-library `csv` module because pandas and pip weren't installed.
- **It wrote `to_organize/Dmel_output.tsv`:** 12,151 rows. It takes the `HOG` and `DROSOPHILA_MELANOGASTER` columns from the `_10_31` table.
- **Checked against the lab's outputs:** the renamed IDs in the `final_final` files for suzukii, miranda and arizonae all appear in it.
- ⚠ **Neither file is a lab original.** Both were later committed inside `to_organize/` (see session 8).

**Crucigera file:**
- The user added `to_organize/repeat-modeler-masker-out/Drosophila_crucigera.nanopore.rm.out`.
- It's RepeatMasker output with no genes in it, and crucigera isn't one of the `final_final` species, so it can't be run through ReVamp or compared.

**Finding the annotations:**
- Started downloading Zenodo record 18453526 `annotations.tar.gz` **straight to `/mnt/storagebox/reference/annotations/`**. It stalled and left a truncated file there.
- Explored the Zenodo version history:
  - Apr/May 2025 (15016918, 15341692): the archive has `GFF/`.
  - **June 20, 2025 (15705949): the archive has `gff_fixed/`.** This is where the lab's `Anno_Duy/gff_fixed/` came from, so the lab didn't do any "fixing" of its own.
  - Feb 2026 (18453526): the archive has `gffs/*.gff.gz`.
  - Dataset authors: Dhakad & Obbard.
- Tried downloading the June archive into `to_organize/zenodo_dl/`, first as 2 parallel downloads and then as 8 byte-range chunks. Zenodo throttled to about 50–100 KB/s.
- ⚠ **Only an 11 MB partial file, `zenodo_dl/annotations_15705949.tar.gz`, was left.** It was later committed (see session 8).

**`data_stuff/` (added by the user):**
- The 87 Dmel CYP genes (Dermauw 2020), with CYP names and clans.
- Stable (29) and unstable (46) CYP lists from Good et al. 2014, plus "Updated" versions with HOG IDs added.
- `Create_Dmel_Cyp_stable_list.py`.
- Some HOG IDs in the "Updated" lists don't match the `_10_31` table.

The session ended on API connection errors.

### 5. The main forensics session (14:13–17:22, session `2c6e0c94`)

**a. The whole chain behind `final_final`:**
- OrthoFinder (`bash_history`) → `HOG_OG_association*.tsv`
- → `Step_1_Replace_RNA_identifiers_with_gene_names_Redo.py`
- → `Step_2_Remove_Duplicate_gene_names_10_31.py` (its `config.py` is missing)
- → `…without_duplicates_10_31.tsv`
- → `Dmel_output.tsv` + `gff_fixed/*_final.gff`
- → `ReVamp_Final.py`
- → `change_*_final_final.gff`

**b. Downloading the annotations (again):**
- The copy on the storage box was 272 MB and failed its md5 check.
- Resuming it in place stalled, so the download was moved to local disk. The user then set the storage-box rule.
- **Result:** `/home/nick/dl-staging/annotations.tar.gz`, 1,755,436,625 bytes, md5 `d7cd2d6d0b98b4d51036b05c619c590b`, matching Zenodo.
- Extracted and gunzipped to `/home/nick/dl-staging/annotations/gffs/`: 301 species, 19 GB.
- **Deleted without asking first:** a stalled browser download, `to_organize/annotations.NlXpBXmV.tar.gz.part`, and an empty `to_organize/annotations.tar.gz`.
- **Environment:** the system Python had no pip or venv, so pip was bootstrapped into a scratchpad venv. pandas was pinned to 2.3.3 (below 3) to match January 2026 behaviour.

**c. Reproducing ReVamp on *D. arizonae*:**
- Ran a path-patched copy of `ReVamp_Final.py`, about 10 minutes.
- **The output matches the lab's `change_DROSOPHILA_ARIZONAE_final_final.gff` on every line** once two formatting differences are removed:
  - the lab's file has CRLF line endings;
  - 19,458 mRNA lines have tabs where Zenodo has spaces, so the lab's `gff_fixed` copy already differed from Zenodo's.
- Both runs renamed the same 26,533 lines.

**d. Documentation:**
- **Wrote `docs/scripts/06-final-final-gff.md`.**
- **Updated 7 existing pages** that had said this step had no code in the repo.
- **Findings recorded:**
  - 788 of 11,063 arizonae orthologous genes (7%) are never renamed. Cells in the HOG table that list several genes are stored with quotes and spaces, so none of those genes match.
  - The substring replacement corrupts text, e.g. `genome` → `genom,nom,ouibe`.
  - The lab's input GFFs have lines with more than 9 tab-separated columns.

**e. The next step after `final_final`:**
- `repeatOpp.py` → `Locate_TE.py` → `CleanAnnasse.py`.
- The committed ananassae example used **Ayush's** `_withDmelNames.gff` (from `NEW_Step_5_Replace_gff_Names_with_Dmelanogaster_1_9.py`, which renames `Name=`), not Duy's `final_final` (which renames `ID=`).

**f. Ayush's version vs Duy's, on ananassae:**
- **Baseline:** rerunning Stage 3 on Ayush's version reproduces the committed `DAnasse_TE_Cyp.txt` exactly (after removing CRLF). The committed `DA_Files/…withDmelNames.gff` is **truncated**: first chromosome only, and it stops mid-line. The rerun started from the committed `filtered.gff` instead.
- **Duy's `final_final` gives a strict subset:**

  | | Ayush's | Duy's |
  |---|---|---|
  | Cyp loci | 91 | 57 |
  | Cyp/TE pairs | 465 | 366 |
  | Distinct Cyp genes | 50 | 48 |

- All 34 missing loci come from the multi-gene-cell defect.
- Cyp28a5 and Cyp6a19 disappear entirely. The Cyp313a cluster is hit hard.
- Claude then proposed fixing `ReVamp_Final.py:47`. **The user rejected this: it's pure forensics.** The forensic-artifact rule was saved.
- Claude's test output was moved out of `to_organize/test_run/` to `/home/nick/dl-staging/test_run/`.

**g. Which version each finished table came from:**
- This was a read-only check of the 29 tables in `pipeline-scripts-output/AnalysisForAll/output/`.
- **Built from Duy's `final_final` (19 species):** aldrichi, algonquin, anomalata, arawakana, arizonae, athabasca, elegans, helvetica, mauritiana, mayaguana, miranda, pandora, santomea, the four sulfurigaster tables, suzukii, tropicalis. Across these species, 516 loci that only Ayush's parse would find have zero TE rows nearby.
- **Built from Ayush's full renaming (7 species):** erecta, mojavensis, pseudoobscura, sechellia, simulans, subpulchrella, willistoni.
- **Undetermined:** eugracilis and paulistorum (both tables are empty) and melanogaster.
- Written into `06-final-final-gff.md` under "Which version each finished table came from".

**h. New repo `~/projects/cyp-te-pipeline` (the "happy path"):**
- **Layout:** `data-preparation/`, `data-analysis/` and `docs/`.
- **Script copies:** 14 scripts copied byte for byte (checked by checksum). The only change is filenames: the ` 1 1` suffixes were dropped.
- **Renaming step:** uses Ayush's `NEW_Step_5` with a **rebuilt, clearly labelled `config.py`**.
- **Validation:** the `_10_31` HOG table reproduces the lab's ananassae `filtered.gff` (166 lines).
  - `_1_9` has no line breaks, so it can't be read.
  - The undated table doesn't match the lab's results.
- **Committed and pushed** to `github.com/0foo/cyp-te-pipeline` after the user created the repo:
  - `94e68f8`: first commit.
  - `39d69b6`: repoints paths after the folder rename.
  - `d19472b`: adds `datasets/` (the HOG table and ananassae reference files, making the repo self-contained), copies of the automation docs, and `NOTES.md` with the open gaps.
- **Not run:** the full self-test from inside the repo. The user stopped it.

**i. Storage-box sync:** an rsync of the archive and unpacked folder to `/mnt/storagebox/reference/annotations/` was started. It was cut off when a session ended, and the user said "forget about the sync". **The storage box still holds a truncated `annotations.tar.gz` and possibly a partial unpacked folder.**

### 6. `/list-agents` only (15:56, session `6b365beb`)

### 7. Remote, archives, the 13 GB file, the rename (16:06–17:06, session `adabdb28`)

**Git remote:**
- `origin` pointed at `0foo/repeat-modeler-automation`, an unrelated history.
- Changed it to `git@github.com:0foo/cyp-project.git`, which already had `be73ebe`.

**Archives:**
- Moved the two zips out to `~/Downloads`, then back again, because the user meant the 7z files.
- **Moved `to_organize/final_final.7z` (122 MB) and `to_organize/hog_og.7z` (224 MB) to `~/Downloads/`.** They are still there.

**The 13 GB melanogaster file:**
- **Why it's so big (partly investigated):** it has 145,112 lines but is 13 GB, so a few lines must be huge. Repeated garbling (`JYalpha` → `JYNil,alpha`, repeating `gene_synonym`) points to a self-feeding find-and-replace. Not confirmed: the line-length scan died with the session.
- **Created `~/projects/cyp-old-data`** (`git init`, nothing committed) and **moved the 13 GB file there** from `to_organize/final_final/`.

**Large files compressed:**
- **Compressed to `.xz` with originals deleted** after checking a byte-exact round trip:
  - `to_organize/hog_og/HOG_OG_association.tsv` (111 MB → 9.9 MB)
  - `HOG_OG_association_1_9.tsv` (111 MB → 9.7 MB)
- ⚠ These are lab files, so the originals exist now only as `.xz`.

**The rename:**
- Changed `origin` to `git@github.com:0foo/cyp-project-forensics.git`.
- **Renamed `~/projects/cyp-project` → `~/projects/cyp-project-forensics`.**
- Copied the Claude memory folder to the new path.
- `~/projects/cyp-project-bkp` (at `be73ebe`) already existed and wasn't touched.

### 8. First session under the new name (17:07–17:34, session `ab903672`)

- **Commit:** `git add -A` and commit **`e1ce8a3`**, which adds all of `to_organize/` (about 2.5 GB, 109 files) and the doc changes. The author ("Nick Kiermaier <nickkiermaier@gmail.com>") was passed per commit because no global git identity is set.
- **Push:** the auto-mode classifier blocked Claude's push. `origin/master` is now at `e1ce8a3`, so the user pushed it.

### 9. This file (17:36, session `30e5b315`)

### 10. Reorganisation and documentation audit (2026-09-24, evening)

Triggered by: *"organize the to_organize folder … make the repo a little more organized, don't delete anything, don't change any code file content, but feel free to move files around … go through and make sure all the documentation is still accurate."* Followed by the framing above: the repo is purely forensics now.

- **Everything moved into two trees.** `evidence/` for artifacts, `docs/` for the investigation. `to_organize/` is gone as a name; nothing was deleted and no file content was changed. The full old→new mapping is in [`evidence/README.md`](evidence/README.md).
- **New entry points:** root `README.md`, `evidence/README.md` (the manifest and chain of custody), `docs/superseded/README.md`.
- **`docs/deep/` → `docs/scripts/`**, **`OCR docs/` → `docs/ocr/`** (the space in the path was a nuisance), **`docs/simple/` and `collected-docs/pipeline-docs/` → `docs/superseded/`** with banners explaining what in them is out of date.
- **Documentation audit.** Every page was checked against the files. Corrections made:
  - Docs described `repeat-modeler-automation/` as part of this repository. It was split out at `be73ebe` on 2026-09-15 and is not the lab's code; it is now labelled as such everywhere.
  - Docs said `to_organize/` was untracked. It was committed in `e1ce8a3`.
  - **`runMasker.sh` had in fact been recovered** and nobody had noticed. It contradicts the lab notebook and the Kaur write-up: `-lib` points at a gene annotation GFF, there is no genome FASTA argument and no `-pa`. Documented as a conflict, not resolved.
  - The 19-vs-7 split of the finished tables between the two renaming scripts was promoted from a buried subsection to a numbered finding (G4).
  - `docs/diagrams/05-data-lineage.md` pointed at a `docs/deep/06-data-formats.md` that never existed.
  - Stage numbering: `docs/superseded/simple/` counts four stages, `docs/pipeline/` counts seven (0–6). The mismatch is now stated rather than left to trip people.
  - "Fix:" framing throughout the script docs was changed to "what would have to change", to keep defects as findings.

### 11. The 3 kb window rule (2026-09-24, evening)

Asked whether `Locate_TE.py` captures a transposon whose *beginning* falls within 3 kb of a
gene, or requires the whole element to be inside the window. Answer: **the whole element**,
and that turned out to matter more than expected.

- The test is `te_end <= stop AND te_start >= start` — containment, not overlap. All three
  surviving copies of the script are identical.
- Reimplemented both tests outside the repository against the three species whose inputs
  survive. The lab's rule reproduces the archived *D. ananassae* count of 900 exactly, which
  validates the reimplementation before anything is concluded from it.
- The loss scales with element length: 1.4% of sub-200 bp repeats dropped, **71% of elements
  ≥5 kb**. 25 of the 38 lost associations are in the upstream flank.
- **It discards long elements in the *Cyp6g1* promoter in two separate species** — the gene
  and the position the *Accord* case makes the study's premise.
- Recorded as an expanded D3 in `docs/pipeline/detailed/04-gaps-and-provenance.md`, in
  `docs/scripts/02-te-locating-scripts.md`, and in both top-level READMEs. The list of
  discarded elements and the script that found it are in
  `evidence/reconstructed/window-rule-analysis/` — investigation output, not lab material.

---

## Where things are now

| What | Location |
|---|---|
| This repo | `~/projects/cyp-project-forensics` → `github.com/0foo/cyp-project-forensics` |
| Snapshot of the repo before the 2026-09-24 work | `~/projects/cyp-project-bkp` (`be73ebe`) |
| Happy-path pipeline | `~/projects/cyp-te-pipeline` → `github.com/0foo/cyp-te-pipeline` |
| 13 GB melanogaster `final_final` | `~/projects/cyp-old-data/` (not committed) |
| `final_final.7z`, `hog_og.7z` | `~/Downloads/` |
| Zenodo 18453526 annotations (md5-verified) + 19 GB unpacked | `/home/nick/dl-staging/` |
| Claude's ReVamp/Stage-3 test outputs | `/home/nick/dl-staging/test_run/` |
| Truncated annotations archive | `/mnt/storagebox/reference/annotations/` (never replaced; sync abandoned) |

## Things under `evidence/` that are NOT lab originals

- **`evidence/reconstructed/`** — everything in it. `make_Dmel_output.py` and `Dmel_output.tsv` were written by Claude on 2026-09-24 at 13:10; they are a reconstruction, not the lab's January file. `zenodo-partial-download/` is an 11 MB abandoned download.
- **`evidence/lab-data/hog-tables/HOG_OG_association.tsv.xz` and `…_1_9.tsv.xz`** — Claude's `xz` compression of lab files. The uncompressed originals were deleted after a verified byte-exact round trip. This is the only place a lab original was altered.
- **`evidence/lab-data/renamed-annotations/`** — holds 25 of the 26 files; the MELANOGASTER one was moved to `cyp-old-data`.
- **`evidence/analysis-scripts/README.md`** — written 2026-09-13 from the scripts' docstrings, not part of the OneDrive delivery.
- **Timestamps:** the extracted files carry 2026-09-24 timestamps, from extraction, not the lab's dates.

## Open questions left from the sessions

These are tracked properly in [`docs/pipeline/detailed/04-gaps-and-provenance.md`](docs/pipeline/detailed/04-gaps-and-provenance.md), Part 3. In short:

- Why is the melanogaster `final_final` 13 GB? The line-length scan never finished. (U4)
- What changed between Zenodo's May `GFF/` and June `gff_fixed/`? The two were never diffed. (U5)
- What was the recovered `runMasker.sh` actually for? It cannot be what produced the `.out` files. (G1)
- Who wrote `evidence/analysis-scripts/`? Nothing in the archive credits anyone.
- The pipeline's gaps: see `~/projects/cyp-te-pipeline/NOTES.md`. They include:
  - genome sources;
  - the high/low exposure species config;
  - the xenobiotic gene list;
  - `requirements.txt`;
  - a check script;
  - two broken links between the copied automation docs.
