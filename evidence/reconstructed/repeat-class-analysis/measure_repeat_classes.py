#!/usr/bin/env python3
"""
measure_repeat_classes.py  --  NOT A LAB SCRIPT.

Written 2026-09-24 during the forensic investigation, to quantify defect D1:
RepeatMasker reports every repeat, not only transposable elements, and nothing
in the lab's pipeline ever filters on repeat class. This measures how much of
what the pipeline calls "TE burden" is not a transposable element at all.

Reads the 29 finished per-species tables in
evidence/te-locating-run/AnalysisForAll/output/ read-only, and writes only into
its own directory.

Each row of those tables is:
    <seqid> TAB <cyp gene> TAB <raw RepeatMasker .out line>
and whitespace field 10 of the third column is the repeat class/family.
"""
import collections, csv, glob, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.abspath(os.path.join(HERE, "..", "..",
                                      "te-locating-run/AnalysisForAll/output"))

# RepeatMasker class/family prefixes that are definitively NOT transposable elements.
NOT_A_TE = ("Simple_repeat", "Low_complexity", "Satellite", "rRNA", "tRNA",
            "snRNA", "scRNA", "srpRNA", "ARTEFACT", "Other")
UNCLASSIFIED = ("Unknown",)


def classify(cls):
    if cls.startswith(NOT_A_TE):
        return "not a TE"
    if cls.startswith(UNCLASSIFIED):
        return "unclassified"
    return "transposable element"


def species_of(path):
    b = os.path.basename(path)
    for suffix in ("GenesAffectedByTE.txt", "GenesAffectedbyTE.txt",
                   "GenesAffectedByTe.txt", "GenesAfffectedByTE.txt",
                   "GenesAffectedByT.txt"):
        if b.endswith(suffix):
            return b[:-len(suffix)].lstrip("D_")
    return b


def rows(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\r\n")
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            f = parts[2].split()
            if len(f) <= 10:
                continue
            try:
                start, end = int(f[5]), int(f[6])
            except ValueError:
                continue
            yield parts[1], f[10], end - start + 1, float(f[1])


def main():
    per_species = {}
    overall = collections.Counter()
    overall_bp = collections.Counter()
    lengths = collections.defaultdict(list)
    class_counts = collections.Counter()

    for path in sorted(glob.glob(os.path.join(OUTDIR, "*.txt"))):
        sp = species_of(path)
        cat = collections.Counter()
        bp = collections.Counter()
        genes_any, genes_real = set(), set()
        n = 0
        for gene, cls, length, div in rows(path):
            k = classify(cls)
            cat[k] += 1
            bp[k] += length
            lengths[k].append(length)
            class_counts[cls] += 1
            genes_any.add(gene)
            if k == "transposable element":
                genes_real.add(gene)
            n += 1
        if n == 0:
            per_species[sp] = None
            continue
        per_species[sp] = dict(n=n, cat=cat, bp=bp,
                               genes_any=len(genes_any), genes_real=len(genes_real))
        overall.update(cat)
        overall_bp.update(bp)

    tot = sum(overall.values())
    print(f"=== ALL SPECIES POOLED — {tot:,} TE-hit rows across "
          f"{sum(1 for v in per_species.values() if v):,} non-empty tables ===\n")
    print(f"{'category':<24}{'rows':>10}{'% rows':>9}{'bp':>14}{'% bp':>8}{'median bp':>11}")
    totbp = sum(overall_bp.values())
    for k in ("not a TE", "unclassified", "transposable element"):
        L = sorted(lengths[k])
        print(f"{k:<24}{overall[k]:>10,}{100*overall[k]/tot:>8.1f}%"
              f"{overall_bp[k]:>14,}{100*overall_bp[k]/totbp:>7.1f}%"
              f"{L[len(L)//2]:>11,}")
    junk = overall["not a TE"]
    print(f"\nNOT a transposable element : {junk:,} of {tot:,} rows = "
          f"{100*junk/tot:.1f}%")
    print(f"  including 'Unknown'      : {junk+overall['unclassified']:,} = "
          f"{100*(junk+overall['unclassified'])/tot:.1f}% not confirmed as a TE")

    print("\n=== the 12 commonest classes ===")
    for cls, n in class_counts.most_common(12):
        print(f"   {n:>7,}  {100*n/tot:>5.1f}%  {cls:<20} [{classify(cls)}]")

    print("\n=== per species — is the junk fraction uniform? ===")
    print(f"{'species':<32}{'rows':>7}{'% not a TE':>12}{'genes w/ hit':>14}{'genes w/ real TE':>18}")
    fracs = []
    for sp in sorted(per_species):
        v = per_species[sp]
        if not v:
            print(f"{sp:<32}{'0':>7}{'—':>12}{'—':>14}{'—':>18}")
            continue
        f = 100 * v["cat"]["not a TE"] / v["n"]
        fracs.append((f, sp))
        print(f"{sp:<32}{v['n']:>7}{f:>11.1f}%{v['genes_any']:>14}{v['genes_real']:>18}")
    fracs.sort()
    print(f"\n   range {fracs[0][0]:.1f}% ({fracs[0][1]}) to {fracs[-1][0]:.1f}% ({fracs[-1][1]})"
          f"  —  spread of {fracs[-1][0]-fracs[0][0]:.1f} percentage points")
    mean = sum(f for f, _ in fracs) / len(fracs)
    var = sum((f - mean) ** 2 for f, _ in fracs) / len(fracs)
    print(f"   mean {mean:.1f}%, standard deviation {var**0.5:.1f} points")

    ga = sum(v["genes_any"] for v in per_species.values() if v)
    gr = sum(v["genes_real"] for v in per_species.values() if v)
    print(f"\n=== effect on the per-gene table the statistics actually run on ===")
    print(f"   gene/species pairs with >=1 recorded hit          : {ga}")
    print(f"   ... that still have one if non-TEs are filtered out: {gr}")
    print(f"   would flip to 'no TE'                              : {ga-gr}"
          f"  ({100*(ga-gr)/ga:.1f}%)")

    with open(os.path.join(HERE, "repeat_class_by_species.tsv"), "w",
              newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["species", "rows", "rows_not_a_TE", "rows_unclassified",
                    "rows_transposable_element", "pct_not_a_TE",
                    "bp_not_a_TE", "bp_transposable_element",
                    "cyp_genes_with_any_hit", "cyp_genes_with_real_TE"])
        for sp in sorted(per_species):
            v = per_species[sp]
            if not v:
                w.writerow([sp, 0, 0, 0, 0, "", 0, 0, 0, 0]); continue
            w.writerow([sp, v["n"], v["cat"]["not a TE"], v["cat"]["unclassified"],
                        v["cat"]["transposable element"],
                        f"{100*v['cat']['not a TE']/v['n']:.1f}",
                        v["bp"]["not a TE"], v["bp"]["transposable element"],
                        v["genes_any"], v["genes_real"]])
    print(f"\nwrote {os.path.join(HERE,'repeat_class_by_species.tsv')}")


if __name__ == "__main__":
    main()
