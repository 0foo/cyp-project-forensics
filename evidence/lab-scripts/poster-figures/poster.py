import pandas as pd
import matplotlib.pyplot as plt

path = "C:/Users/User/Documents/BioAtallah/TerryPoster/small_HOG_OG_Cyp_gene_counts_11_5.tsv"

# read dataframe (first column as index)
df = pd.read_csv(path, sep="\t", index_col=0)

# keep only the first 30 columns (drop all columns after column 30)
# if there are fewer than 30 columns this is a no-op
df = df.iloc[:, :8]

#print(f"Kept {df.shape[1]} columns, shape={df.shape}")

print(df)

# optionally save truncated file (uncomment to enable)
out_path = "C:/Users/User/Documents/BioAtallah/TerryPoster/small_HOG_OG_Cyp_gene_counts_11_5_trunc.tsv"
df.to_csv(out_path, sep='\t')