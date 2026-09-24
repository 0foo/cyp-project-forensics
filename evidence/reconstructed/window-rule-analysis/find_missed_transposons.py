#!/usr/bin/env python3
"""
find_missed_transposons.py  --  NOT A LAB SCRIPT.

Written 2026-09-24 during the forensic investigation, to measure one defect in
the lab's `Locate_TE.py`: its 3 kb window is a *containment* test, so a repeat
must lie entirely inside [gene_start - 3000, gene_end + 3000] to be recorded.
Any element that reaches into the window but extends past its edge is dropped,
however close to the gene it begins.

This script reads the lab's files read-only and writes only into its own
directory. It does not modify anything under evidence/.

Method, per species:
  1. Reproduce `repeatOpp.py`'s filter exactly -- keep `gene` rows whose column 9
     mentions a symbol from Reg_Gene_Full.txt, skipping list lines that start
     with 'D', and emitting one row per matching symbol (the duplication is the
     lab's, and is preserved so row counts are comparable).
     For D. ananassae the lab's own filtered.gff is used instead, since it
     survives and is the actual input that produced the archived results.
  2. Apply the lab's test:      te_end <= stop AND te_start >= start
  3. Apply a standard overlap:  te_start <= stop AND te_end >= start
  4. Report what (2) loses relative to (3).

Validation: on D. ananassae, step 2 reproduces the archived
GenesAffectedByTEs.txt row count (900) exactly.

Usage:  python3 find_missed_transposons.py
"""
import csv, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
EV   = os.path.abspath(os.path.join(HERE, "..", ".."))
RUN  = os.path.join(EV, "te-locating-run")
FLANK = 3000

SPECIES = [
    # label,        annotation,                                              repeatmasker .out
    ("ananassae",  os.path.join(RUN, "filtered.gff"),
                   os.path.join(RUN, "DA_Files/Drosophila_ananassae.GCF_017639315.1.rm.fna.out")),
    ("sechellia",  os.path.join(RUN, "AnalysisForAll/GFF/DROSOPHILA_SECHELLIA_final.gff"),
                   os.path.join(RUN, "AnalysisForAll/FilesFromMasker/Drosophila_sechellia.GCF_004382195.2.rm.fna.out")),
    ("simulans",   os.path.join(RUN, "AnalysisForAll/GFF/DROSOPHILA_SIMULANS_final.gff"),
                   os.path.join(RUN, "AnalysisForAll/FilesFromMasker/Drosophila_simulans.GCF_016746395.2.rm.fna.out")),
]
REG = os.path.join(RUN, "AnalysisForAll/Reg_Gene_Full.txt")


def cyp_symbols():
    """Reg_Gene_Full.txt as repeatOpp.py reads it: every line starting with 'D' is skipped."""
    out = []
    with open(REG, encoding="utf-8") as fh:
        for line in fh:
            s = line.rstrip("\n").strip()
            if not s or s.startswith("D"):
                continue
            out.append(s)
    return out


def gene_rows(path, symbols, prefiltered):
    """(seqid, start, end, attrs, symbol) per row, reproducing repeatOpp.py's duplication."""
    rows = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) < 9:
                continue
            if prefiltered:
                rows.append((f[0], int(f[3]), int(f[4]), f[8], None))
                continue
            if f[2] != "gene":
                continue
            for sym in symbols:                 # no break: the lab emits one row per match
                if sym in f[8]:
                    rows.append((f[0], int(f[3]), int(f[4]), f[8], sym))
    return rows


def repeats(path):
    """(seqid, start, end, class, family, div) from a RepeatMasker .out."""
    out = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            f = line.split()
            if len(f) <= 10:
                continue
            try:
                s, e = int(f[5]), int(f[6])
            except ValueError:
                continue                        # the two header lines
            out.append((f[4], s, e, f[10], f[9], f[1]))
    return out


def name_of(attrs, fallback):
    for part in attrs.split(";"):
        if part.startswith("Name="):
            return part[5:]
    return fallback or "?"


def main():
    symbols = cyp_symbols()
    tsv = os.path.join(HERE, "missed_transposons.tsv")
    summary_rows = []
    with open(tsv, "w", newline="", encoding="utf-8") as out:
        w = csv.writer(out, delimiter="\t", lineterminator="\n")
        w.writerow(["species", "seqid", "cyp_gene", "gene_start", "gene_end",
                    "window_start", "window_end", "te_start", "te_end", "te_length_bp",
                    "repeat_family", "repeat_class", "pct_divergence",
                    "bp_outside_window", "relation_to_gene"])
        for label, gff, rmout in SPECIES:
            pre = gff.endswith("filtered.gff")
            genes = gene_rows(gff, symbols, pre)
            reps = repeats(rmout)
            by_seq = collections.defaultdict(list)
            for r in reps:
                by_seq[r[0]].append(r)

            kept = overlapped = 0
            missed = set()
            for seq, gs, ge, attrs, sym in genes:
                start, stop = gs - FLANK, ge + FLANK
                for _, ts, te, cls, fam, div in by_seq.get(seq, ()):
                    if not (ts <= stop and te >= start):
                        continue
                    overlapped += 1
                    if te <= stop and ts >= start:
                        kept += 1
                        continue
                    gene_name = name_of(attrs, sym)
                    if te > stop:
                        outside, rel = te - stop, ("downstream flank" if ts > ge else "overlaps gene")
                    else:
                        outside, rel = start - ts, ("upstream flank" if te < gs else "overlaps gene")
                    missed.add((seq, gene_name, gs, ge, start, stop, ts, te,
                                te - ts + 1, fam, cls, div, outside, rel))

            for m in sorted(missed, key=lambda x: -x[8]):
                w.writerow([label, m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7],
                            m[8], m[9], m[10], m[11], m[12], m[13]])

            summary_rows.append((label, len(genes), kept, overlapped,
                                 overlapped - kept, len(missed)))

    print(f"{'species':<12}{'gene rows':>10}{'kept':>9}{'overlap':>9}{'lost rows':>11}{'distinct TEs':>14}")
    for r in summary_rows:
        print(f"{r[0]:<12}{r[1]:>10}{r[2]:>9}{r[3]:>9}{r[4]:>11}{r[5]:>14}")
    print(f"\nwrote {tsv}")


if __name__ == "__main__":
    main()
