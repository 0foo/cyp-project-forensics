import pandas as pd
import re
import os
#regex for matching texts in the .gff files
#pandas is used to make data easily readible
#os is used for the checking of the files

hogogPath = "B:/Copy_toDuy/Copy_toDuy/Test_Duy/textfiles/HOG_OG_association_gene_names_without_duplicates_10_31.tsv"

hogog_df = pd.read_csv(hogogPath, sep = "\t", low_memory=False)


# puts all the fly names into a list called flyName
# for each species, loop through them and find the HOG and fly-gene relationship
flyName = []
for label,value in hogog_df.head(0).items():
    flyName.append(str(label))

#removal of extra labels
flyName.remove("HOG")
flyName.remove("OG")
flyName.remove("Gene Tree Parent Clade")

def gene_Getter(names):
    testName = str(names)
    hog = "HOG"
    #cleans up all the genes and puts them into a dictionary array
    value =  hogog_df[hog] #hogs
    key = hogog_df[testName] #genes of species
    flyDict = dict(zip(key,value))

    #fancy way to remove NA keys
    flyDict = {
        k: v for k, v in flyDict.items()
            if not pd.isna(k)}

    #splits the keys if there is any commas in the key, and splits it if any, if not then add key and value to array.
    arr = []
    for k, v in flyDict.items():
        if isinstance(k, str) and "," in k:
            new_k = k.split(", ")
            for item in new_k:
                arr.append({item:v})
            continue
        arr.append({k:v})

    # print(arr)
    rows = []
    for d in arr:
        for genes,hog  in d.items():
            rows.append({
            "genes": genes, 
            "hog": hog 
        })
    #genes and HOG df
    genesTF = pd.DataFrame(rows)

    #this array contains dictionaries of species genes as keys and HOGs as values
    return genesTF

def anno_Cleaner(flySpeciesPath):
    annoList = []
    with open(flySpeciesPath) as gff:
        for line in gff:
            #skips header
            if line.startswith("#"):
                continue
            #turns the line into a list with 8 indices
            fields = line.rstrip("\n").split("\t")
            #for safety it will blow up with different files i think
            if len(fields) != 9:
                continue

            attribute = fields[8]
            annoList.append(attribute)

        cleanedAnno = pd.DataFrame(annoList, columns=['attribute'])

    return cleanedAnno

def HOG_to_Parent(genesTF, cleanedAnno):
    results = []

    #stafty check
    attrs_series = cleanedAnno["attribute"].astype(str)
    attrs_list = attrs_series.tolist()

    #build the inverted index
    token_re = re.compile(r"\b[^\s;=,]+\b")
    index = {}
    for attr in attrs_list:
        try:
            tokens = set(token_re.findall(attr))
        #this should not happen but just in case things blow up
        except Exception:
            tokens = set()
        for tok in tokens:
            index.setdefault(tok, []).append(attr)

    #ensures duplicate HOGS don't get overwritten.
    gene_to_hogs = {}
    for _, row in genesTF.iterrows():
        g = row["genes"]
        h = row["hog"]
        gene_to_hogs.setdefault(g, []).append(h)

    #match the gene and HOG to where the attribute.
    for gene, hogs in gene_to_hogs.items():
        # safty check
        key = str(gene)
        matched_attrs = index.get(key, [])

        if matched_attrs:
            for attr in matched_attrs:
                for hog in hogs:
                    results.append({
                        "genes": gene,
                        "hog": hog,
                        "attribute": attr
                    })
        #ideally, this does not happen
        else:
            for hog in hogs:
                results.append({
                    "genes": gene,
                    "hog": hog,
                    "attribute": pd.NA
                })

    return pd.DataFrame(results)


for names in flyName:

    #location of the fly annotations
    flySpeciesPath = f"B:/Copy_toDuy/Copy_toDuy/Test_Duy/Annotations_12_species/Annotations_12_species/{str(names)}_final.gff"

    # #to check if there exists a path
    to_print = os.path.exists(flySpeciesPath)
    
    if to_print == True:
        print(names)
        genesTF = gene_Getter(names)
       #print(genesTF)
        cleanedAnno = anno_Cleaner(flySpeciesPath)
        #print(cleanedAnno)
        complete = HOG_to_Parent(genesTF, cleanedAnno)
        print(complete.head(5))
        

    