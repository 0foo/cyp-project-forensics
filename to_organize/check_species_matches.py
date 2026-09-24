import pandas as pd
from pathlib import Path

mainPath = Path(r"C:/Users/User/Documents/BioAtallah/TerryPoster/reWorked/Big_HOG_OG_Cyp_gene_counts_11_5.tsv")
speciesPath = Path(r"C:/Users/User/Documents/BioAtallah/TerryPoster/reWorked/new_species.csv")

df = pd.read_csv(mainPath, sep='\t', index_col=0)
# read species file lines
with open(speciesPath, 'r', encoding='utf-8') as f:
    species = [line.strip() for line in f if line.strip()]

index_vals = df.index.astype(str).tolist()

# simple case-insensitive sets
index_set = {s.upper() for s in index_vals}
species_set = {s.upper() for s in species}

intersection = index_set & species_set

print(f"TSV rows: {len(index_vals)}")
print(f"Species list entries: {len(species)}")
print(f"Direct intersection size: {len(intersection)}")
if intersection:
    print('Examples of direct matches:', list(intersection)[:20])

print('\nFirst 20 TSV index entries:')
for s in index_vals[:20]:
    print('  ', s)

print('\nFirst 20 species list entries:')
for s in species[:20]:
    print('  ', s)

# try normalized matching: keep only alphanumerics and underscores
import re

def normalize(name):
    name = re.sub('[^A-Za-z0-9]+', '_', name)
    name = re.sub('_+', '_', name)
    return name.strip('_').upper()

norm_index = {normalize(s): s for s in index_vals}
norm_species = {normalize(s): s for s in species}

norm_inter = set(norm_index.keys()) & set(norm_species.keys())
print('\nNormalized intersection size:', len(norm_inter))
if norm_inter:
    print('Examples normalized matches:', list(norm_inter)[:20])

# show some species that didn't match
unmatched = [s for s in species if normalize(s) not in norm_index]
print(f"\nSpecies entries with no normalized match (first 20): {len(unmatched)}")
for s in unmatched[:20]:
    print('  ', s)

