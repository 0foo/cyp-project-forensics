import pandas as pd
from pathlib import Path


# Paths
genePath = Path(r"C:/Users/User/Documents/BioAtallah/TerryPoster/reWorked/gene_list_first_token.csv")
# Allow multiple possible species filenames (user may have `newspecies.csv` or `new_species.csv`)
species_candidates = [
	Path(r"C:/Users/User/Documents/BioAtallah/TerryPoster/reWorked/species.csv"),
	Path(r"C:/Users/User/Documents/BioAtallah/TerryPoster/reWorked/newspecies.csv"),
	Path(r"C:/Users/User/Documents/BioAtallah/TerryPoster/reWorked/new_species.csv"),
	Path(r"C:/Users/User/Documents/BioAtallah/TerryPoster/reWorked/species_list50.txt"),
]
speciesPath = None
for p in species_candidates:
	if p.exists():
		speciesPath = p
		break
if speciesPath is None:
	raise FileNotFoundError("No species file found in reWorked; expected one of: species.csv, newspecies.csv, new_species.csv, species_list50.txt")
mainPath = Path(r"C:/Users/User/Documents/BioAtallah/TerryPoster/reWorked/Big_HOG_OG_Cyp_gene_counts_11_5.tsv")



def csv_first_column_to_list(path: Path) -> list:
	"""Read CSV and return the first column as a list of strings.

	Handles files with or without a header.
	"""
	# Try reading with pandas (works for CSV/TSV); fall back to plain text lines
	try:
		df = pd.read_csv(path, header=None)
		return df.iloc[:, 0].astype(str).tolist()
	except Exception:
		with open(path, 'r', encoding='utf-8') as f:
			return [line.strip() for line in f if line.strip()]


geneList = csv_first_column_to_list(genePath)
#print(geneList)
speciesList = csv_first_column_to_list(speciesPath)
#print(speciesList)

df = pd.read_csv(mainPath, sep = "\t", index_col=0)
toClean_df = pd.DataFrame(df)

#print(toClean_df)
#print(toClean_df)
# Ensure index and column names are strings
toClean_df.index = toClean_df.index.astype(str)
toClean_df.columns = toClean_df.columns.astype(str)

# Build case-insensitive maps from the DataFrame to allow matching
index_map = {idx.upper(): idx for idx in toClean_df.index}
col_map = {col.upper(): col for col in toClean_df.columns}

# Preserve order from speciesList and geneList; only keep ones that exist in the TSV
rows_to_keep = [index_map[s.strip().upper()] for s in speciesList if s.strip().upper() in index_map]
cols_to_keep = [col_map[g.strip().upper()] for g in geneList if g.strip().upper() in col_map]

missing_species = [s for s in speciesList if s.strip().upper() not in index_map]
missing_genes = [g for g in geneList if g.strip().upper() not in col_map]

toClean_df = toClean_df.loc[rows_to_keep, cols_to_keep]

print(f"Kept {toClean_df.shape[0]} rows and {toClean_df.shape[1]} columns after filtering")
if missing_species:
	print(f"Species not found: {len(missing_species)} (examples: {missing_species[:10]})")
if missing_genes:
	print(f"Genes not found: {len(missing_genes)} (examples: {missing_genes[:10]})")

# Save filtered DataFrame to TSV in the same folder as the source TSV
output_path = mainPath.parent / "filtered_counts.tsv"
toClean_df.to_csv(output_path, sep='\t')
print(f"Saved filtered TSV to {output_path}")
# for y in toClean_df.index.astype(str):
# 	for species in speciesList:
# 		if y != species:
# 			toClean_df.drop(y)

print(toClean_df)
			
