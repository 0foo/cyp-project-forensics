import csv

#recreates Dmel_output.tsv (input to ReVamp_Final.py): each HOG and its D. melanogaster gene name(s)
hogogPath = "hog_og/HOG_OG_association_gene_names_without_duplicates_10_31.tsv"

count = 0
with open(hogogPath, newline="", encoding="utf-8") as hogog, open("Dmel_output.tsv", "w", newline="", encoding="utf-8") as output:
    reader = csv.DictReader(hogog, delimiter="\t")
    writer = csv.writer(output, delimiter="\t", lineterminator="\n")
    writer.writerow(["hog", "genes"])
    for row in reader:
        #only HOGs that have a Dmel gene
        if row["DROSOPHILA_MELANOGASTER"]:
            writer.writerow([row["HOG"], row["DROSOPHILA_MELANOGASTER"]])
            count += 1

print(f"wrote {count} rows to Dmel_output.tsv")
