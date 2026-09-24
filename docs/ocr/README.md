# OCR transcriptions

Transcriptions of the 17 photographs in
[`../../evidence/photographs/`](../../evidence/photographs/). Each source image is transcribed
into a document here, as close to verbatim as the photograph allows.

## Why these exist

The lab's pipeline was never version-controlled. Alongside the loose scripts and output files
in [`../../evidence/`](../../evidence/), what survives is a pile of phone photos: a terminal
window, a lab notebook, a few File Explorer windows, a typed monthly log, and a printed
student write-up. Everything the code does *not* tell you — where files lived, who wrote which
script, how long runs took, what the manual steps were — is only in those photos.

These documents are the machine-readable version of them, so the rest of `docs/` can cite a
source instead of repeating folklore.

**They are primary sources and the code is not always the more reliable one.** Stage 2 is the
case that matters: a `runMasker.sh` has since been recovered from the lab archives, and it
contradicts both doc 02 and doc 05, which agree with each other and with the shape of the
surviving output. Where a photograph and a file disagree, the disagreement itself is the
finding — see
[`../pipeline/detailed/02-stage-reference.md`](../pipeline/detailed/02-stage-reference.md).

## How to read these

- **Verbatim blocks** reproduce what is on the page, including the original's typos
  (`grom` for `from`, `demonstarates`, `libraires`, `transp0osable`, `Proect` for `Project`).
  These are not transcription errors; they are in the source.
- **`[?]`** marks a word that could not be read with confidence.
- **`[VERIFY]`** marks a claim that should be checked against a live system before anyone
  acts on it.
- Commentary from this transcription is kept in clearly-labelled *Notes* sections, never
  mixed into a verbatim block.

## Inventory

| Doc | Source image(s) | What it is |
|---|---|---|
| [01-spincontainer-terminal.md](01-spincontainer-terminal.md) | `PXL_20260824_155714317.jpg` | Terminal: `cat spinContainer.sh` |
| [02-lab-notebook-pipeline-page.md](02-lab-notebook-pipeline-page.md) | `PXL_20260824_162859737.jpg`, `PXL_20260824_163729437.jpg` | Handwritten notebook: RepeatMasker, species list, VS Code steps, JBrowse |
| [03-file-explorer-screenshots.md](03-file-explorer-screenshots.md) | `PXL_20260831_174105078.jpg`, `PXL_20260904_193934568.jpg`, `PXL_20260904_194848577.jpg` | Three Windows Explorer windows: directory layouts |
| [04-atallah-lab-spring-2026-log.md](04-atallah-lab-spring-2026-log.md) | `PXL_20260910_180224777.jpg`, `…180230890.jpg`, `…180319215.jpg` (+ dups `…180311619`, `…180314998`) | Typed 3-page monthly log, Jan–May 2026 |
| [05-kaur-writeup-bioinformatics-scripts.md](05-kaur-writeup-bioinformatics-scripts.md) | `PXL_20260910_180237566.jpg`, `…180244049.jpg`, `…180250348.jpg`, `…180256463.jpg`, `…180259530.jpg` | Diljot Kaur, 5-page write-up |
| [06-notepad-file-handoff-sketch.md](06-notepad-file-handoff-sketch.md) | `PXL_20260910_180342882.jpg` | Handwritten sketch of the file handoff chain |

`evidence/photographs/Photos-1-001.zip` contains no unique images — it is a copy of the
eleven `PXL_20260910_18*.jpg` files already present loose in the same folder.

Two images are exact re-shoots of pages captured elsewhere in the set and are folded into
the document for the page they duplicate:
`PXL_20260910_180311619.jpg` (= log page 1) and `PXL_20260910_180314998.jpg` (= log page 2).

## Verification status

Every one of the seventeen images has been opened and read against its transcription. The
table below records that pass, so a later reader can tell what was checked rather than
assuming.

| Image | Transcribed in | Verified | Notes |
|---|---|---|---|
| `PXL_20260824_155714317.jpg` | 01 | ✅ | `spinContainer.sh` contents confirmed line for line, including flag order |
| `PXL_20260824_163729437.jpg` | 02 | ✅ | Primary (flat) shot of the notebook page |
| `PXL_20260824_162859737.jpg` | 02 | ✅ | Same page, angled; adds only the Dfam banner behind it |
| `PXL_20260831_174105078.jpg` | 03a | ✅ | Folder and script names confirmed; top entry reads `Eugracilis`, clipped |
| `PXL_20260904_193934568.jpg` | 03b | ✅ | All ten `Spring26` entries and their dates confirmed |
| `PXL_20260904_194848577.jpg` | 03c | ✅ | RepeatModeler output listing and timestamps confirmed |
| `PXL_20260910_180224777.jpg` | 04 p1 | ✅ | Confirmed verbatim, including the boxed command table |
| `PXL_20260910_180230890.jpg` | 04 p2 | ✅ | Confirmed verbatim, including the `CYP_Gene_Proect` typo |
| `PXL_20260910_180319215.jpg` | 04 p3 | ✅ | Flynn benchmark figures confirmed; blue annotation still illegible |
| `PXL_20260910_180311619.jpg` | 04 p1 | ✅ | Confirmed a duplicate re-shoot of page 1, not new content |
| `PXL_20260910_180314998.jpg` | 04 p2 | ✅ | Confirmed a duplicate re-shoot of page 2, not new content |
| `PXL_20260910_180237566.jpg` | 05 p1 | ✅ | Confirmed verbatim |
| `PXL_20260910_180244049.jpg` | 05 p2 | ✅ | Confirmed verbatim |
| `PXL_20260910_180250348.jpg` | 05 p3 | ✅ | Confirmed verbatim |
| `PXL_20260910_180256463.jpg` | 05 p4 | ✅ | Steep angle, rotated text; readable and confirmed |
| `PXL_20260910_180259530.jpg` | 05 p5 | ✅ | Left margin genuinely cut off by framing; bracketed reconstructions confirmed as reconstructions |
| `PXL_20260910_180342882.jpg` | 06 | ✅ | Handoff sketch confirmed, including `Run_Maske.sh` written without the `r` |

Two findings from the verification pass are worth recording:

- **The fourth log page is real.** Page 3's show-through resolves far enough to make out
  `Families:` and `Runtime:` lines against species names in the 400-1000 range. A page listing
  per-species family counts and runtimes exists and was not photographed. It is the only
  record of those numbers.
- **Page 3 of the log sits on top of page 1 of the write-up** in two of the photographs,
  which is what ties the log's authorship to Diljot Kaur directly rather than by inference.

## What these sources establish

Read together, the six documents pin down a handful of things the code alone does not:

- The **container invocation** is `dfam/tetools:latest` with the working directory
  bind-mounted at `/Spring26RepeatModeler` (doc 01). The lab's own `spinContainer.sh` has
  since been recovered and matches this transcription line for line — one of the few places a
  photograph and a file confirm each other exactly.
- The **RepeatModeler command** is `-threads 10 -LTRStruct` (doc 04), against a database
  built by `BuildDatabase -name D_speciesname`.
- **Runtime is 8–26 hours per genome**, driven by genome size (doc 04). This is the single
  fact that explains the shape of everything upstream of stage 3 — and the design of the
  worker/manager pair that later replaced it.
- The **Stage-3 Python step was run by hand in VS Code**, with three file paths pasted into
  the script source before each of three separate runs (docs 02, 05). The hardcoded Windows
  paths still visible at the top of `evidence/te-locating-run/*.py` are the residue of this —
  and `Locate_TE.py` survives twice, differing only in those paths, which is the cycle caught
  mid-stride.
- A **validation run fell short of the published benchmark**: 471 TE families vs. Flynn et
  al.'s 734, on the same genome and parameters (doc 04). Unresolved.

See [`../pipeline/detailed/04-gaps-and-provenance.md`](../pipeline/detailed/04-gaps-and-provenance.md)
for what each of these implies.
