import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

DATA_PATH = r"C:/Users/User/Documents/BioAtallah/TerryPoster/small_HOG_OG_Cyp_gene_counts_11_5.tsv"

# read dataframe (first column as index)
df = pd.read_csv(DATA_PATH, sep="\t", index_col=0)

# coerce to numeric and sanitize
try:
	df = df.astype(float)
except Exception:
	df = df.apply(pd.to_numeric, errors='coerce')
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Discrete colormap mapping: 0 grey; 1 light blue; 2 blue; 3-4 dark blue; 5-6 yellow; 7-8 orange; 9+ deep orange
colors = [
	"#B0B0B0",  # 0
	"#A6C8FF",  # 1 (lighter blue)
	"#4F79FF",  # 2 (blue)
	"#08306B",  # 3-4 (dark blue)
	"#FFD700",  # 5-6 (yellow)
	"#FF8C00",  # 7-8 (orange)
	"#FF4500",  # 9+ (deep orange)
]

# compute bounds; ensure finite
raw_max = np.nanmax(df.values) if np.size(df.values) else np.nan
if not np.isfinite(raw_max):
	raw_max = 9.0
maxv = max(9.0, float(raw_max))

# new boundaries to separate 1 and 2: 0,1,2,3-4,5-6,7-8,9+
bounds = [-0.5, 0.5, 1.5, 2.5, 4.5, 6.5, 8.5, maxv + 1.0]
cmap = mcolors.ListedColormap(colors)
norm = mcolors.BoundaryNorm(bounds, cmap.N)

# plot
plt.figure(figsize=(14, 8))
ax = sns.heatmap(
	df,
	cmap=cmap,
	norm=norm,
	xticklabels=True,
	yticklabels=True,
	cbar=True,
	linewidths=0.25,
	linecolor='white'
)

ax.set_title("Gene Occurrence per Species (scaled dataset)")
ax.set_xlabel("Genes")
ax.set_ylabel("Species")

# tidy colorbar labels
cbar = ax.collections[0].colorbar
midpoints = [(bounds[i] + bounds[i+1]) / 2.0 for i in range(len(bounds) - 1)]
labels = ['0', '1', '2', '3-4', '5-6', '7-8', '8+']
cbar.set_ticks(midpoints)
cbar.set_ticklabels(labels)

plt.xticks(rotation=45, ha='right', fontsize=8)
plt.yticks(fontsize=8)
plt.tight_layout()

# save output
out = r"C:/Users/User/Documents/BioAtallah/TerryPoster/fin_poster.png"
plt.savefig(out, dpi=200)
print(f"Saved heatmap to {out} (shape={df.shape})")