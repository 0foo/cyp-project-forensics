import pandas as pd
import re
import os
from pathlib import Path

DmelPath =  "D:/CYP_Gene_Project/Dhakad_et_al_2025_Data_Analysis/reVamp_Duy_Scripts/Dmel_output.tsv"
DmelBase = pd.read_csv(DmelPath, sep ="\t", low_memory=False)

#print(DmelBase.head(5))

hogogPath = "D:/CYP_Gene_Project/Dhakad_et_al_2025_Data_Analysis/Output/HOG_OG_association_gene_names_without_duplicates_10_31.tsv"
hogog_df = pd.read_csv(hogogPath, sep = "\t", low_memory=False)

flyName = []
for label,value in hogog_df.head(0).items():
    flyName.append(label)

#removal of extra labels
flyName.remove("HOG")
flyName.remove("OG")
flyName.remove("Gene Tree Parent Clade")

def gene_Getter(names):
    testName = str(names)
    hog = "HOG"
    value =  hogog_df[hog] #hogs of species
    key = hogog_df[testName] #genes of species
    flyDict = dict(zip(key,value))

    #quickfix: reverses genes as value and HOG as keys to abuse O(1) speed
    hog_to_gene = {v: k for k, v in flyDict.items()}


    #merges Dmel with associated species
    rows = []
    for _, row in DmelBase.iterrows():
        hog = row["hog"]
        if str(hog) in hog_to_gene:
            rows.append({
                "hog": hog, 
                "Dmel": row["genes"],
                f"{testName}": hog_to_gene[str(hog)]
        })
    genesTF = pd.DataFrame(rows)

    #split comma separated values in linked to species gene
    genesTF[f"{testName}"] = genesTF[f"{testName}"].str.split(',')
    genesTF = genesTF.explode(f"{testName}")

    return genesTF

def anno_Cleaner(flyPath):
    annoList = []
    with open(flyPath) as gff:
        for line in gff:
            #skips header
            if line.startswith("#"):
                continue
            #turns the line into a list with 8 indices
            fields = line.rstrip("\n").split("\t")
            #for safety it will blow up with different files i think
            if len(fields) != 9 :
                continue
            #added 1/9 to check if the annotation line is a gene
            if fields[2]=="gene":
                attribute = fields[8]
                annoList.append(attribute)
            

        cleanedAnno = pd.DataFrame(annoList, columns=['attribute'])

    return cleanedAnno

def HOG_to_Parent(genesTF, cleanAnno):
    results = []
    #added VV
    species_name = genesTF.columns[2]

    #safety check
    attrs_series = cleanAnno["attribute"].astype(str)
    attrs_list = attrs_series.tolist()

    #build the inverted index
    token_re = re.compile(r"\b[^\s;=,]+\b")
    index = {}
    for attr in attrs_list:
        try:
            tokens = set(token_re.findall(attr))
        #this should not happen but just in case things blow up UPDATE 1/9: this will happen
        except Exception:
            tokens = set()
        for tok in tokens:
            index.setdefault(tok, []).append(attr)

    #ensures duplicate entries don't get overwritten 
    gene_to_hogs = {}
    for _, row in genesTF.iterrows():
        #added VV
        species_gene = row[f"{species_name}"]
        dmel_gene = row["Dmel"]
        hog = row["hog"]
        gene_to_hogs.setdefault(species_gene, []).append({
            "Dmel": dmel_gene,
            "hog": hog
        })

    #match the gene and HOG to where the attribute using the pseudo database 
    for gene, hog_list in gene_to_hogs.items():
        # safety check
        key = str(gene)
        matched_attrs = index.get(key, [])

        if matched_attrs:
            for attr in matched_attrs:
                for hog_dict in hog_list:
                    results.append({
                        "Dmel": hog_dict["Dmel"],
                        #Added VV
                        f"{species_name}" : gene,
                        "hog": hog_dict["hog"],
                        "attribute": attr
                    })
        #ideally, this does not happen #UPDATE: 1/9 This will happen a bunch now
        else:
            for hog_dict in hog_list:
                results.append({
                    "Dmel": hog_dict["Dmel"],
                    #Added VV
                    f"{species_name}": gene,
                    "hog": hog_dict["hog"],
                    "attribute": pd.NA
                })
    return pd.DataFrame(results)

def ReplaceinAnno(complete, flySpeciesPath):
    col1 = complete.columns[0]  # First column
    col2 = complete.columns[1]  # Second column

    key = complete[col2].values     # Column 2 becomes keys
    value = complete[col1].values   # Column 1 becomes values
    inNout = dict(zip(key, value))
    
    #filter through null enteries
    inNout = {k: v for k, v in inNout.items() if isinstance(k, str) and isinstance(v, str)}

    base = os.path.splitext(os.path.basename(flySpeciesPath))[0]
    out_name = f"change_{base}_final.gff"
    with open(flySpeciesPath, 'r', encoding='utf-8') as input, open(out_name, 'w', encoding='utf-8') as output:
        for line in input:
            modified_line = line
            for old, new in inNout.items():
                modified_line = modified_line.replace(old, new)
            output.write(modified_line)
    return


for names in flyName:

    #location of the fly annotations
    flySpeciesPath = os.path.join(
        "D:/CYP_Gene_Project/Dhakad_et_al_2025_Data_Analysis/Dhakad_et_al_2025_Data/Anno_Duy/gff_fixed",
        f"{names}_final.gff"
    )

    checkPoint = Path("D:/CYP_Gene_Project/Dhakad_et_al_2025_Data_Analysis/reVamp_Duy_Scripts/change_" + names + "_final_final.gff")

    # Check whether the annotation file exists
    to_print = os.path.exists(flySpeciesPath)

    # Skip if already processed
    if checkPoint.is_file():
        print(f"{names} already done")
        continue

    # If annotation exists, process it; otherwise report missing file
    if to_print:
        print(names)
        genesTF = gene_Getter(names)
        cleanedAnno = anno_Cleaner(flySpeciesPath)
        complete = HOG_to_Parent(genesTF, cleanedAnno)
        SuperDone = ReplaceinAnno(complete, flySpeciesPath)
    else:
        print(f"Annotation not found for {names}: {flySpeciesPath}")