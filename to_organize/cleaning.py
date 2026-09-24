"""Read species list and load into a DataFrame.

This script reads species names from a plain text file (one per line),
strips whitespace, ignores empty lines, and prints a small sample.
"""

from pathlib import Path
from typing import List

import pandas as pd


SPECIES_FILE = Path(r"C:/Users/User/Documents/BioAtallah/TerryPoster/reWorked/Cyp_Genes_with_tissue_expression.txt")
OUT_CSV = SPECIES_FILE.with_name("gene_list_first_token.csv")


def read_species(path: Path) -> List[str]:
    """Return a list of non-empty, stripped lines from ``path``.

    Args:
        path: Path to a UTF-8 encoded text file with one species per line.
    """
    with path.open("r", encoding="utf-8") as fh:
        # If a line contains spaces, keep only the first element/token.
        result: List[str] = []
        for line in fh:
            text = line.strip()
            if not text:
                continue
            first = text.split()[0]
            result.append(first)
        return result


def main() -> None:
    species = read_species(SPECIES_FILE)
    df = pd.DataFrame({"species": species})
    print(df.head())
    df.to_csv(OUT_CSV, index=False, encoding="utf-8")
    print(f"Wrote {len(df)} species to: {OUT_CSV}")


if __name__ == "__main__":
    main()