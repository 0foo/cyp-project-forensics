import pandas as pd
import re
my_dict = {
    "gene-G00000000124, gene-G00000010343":"N1.HOG0044357",
    "gene-G00000001798, gene-G00000005344":"N1.HOG0044358",
    "gene-G00000004168, gene-G00000003359":"N1.HOG0044359",
    "gene-G00000005310, gene-G00000005305":"N1.HOG0044360",
    "gene-G00000005307":"N1.HOG0044361"
}
#my_new_dict = {}
arr = []
for k,v in my_dict.items():
    if "," in k :
        new_k = k.split(", ")
        for item in new_k:
            arr.append({item:v})
        continue
    arr.append({k:v})

rows = []
for d in arr:
    for genes,hog  in d.items():
        rows.append({
            "genes": genes, #idk why its reverse
            "hog": hog #idk why its reversed
        })
#genes and HOG df
genesTF = pd.DataFrame(rows)

dVirilPath = "B:/Copy_toDuy/Copy_toDuy/Test_Duy/viril_test.gff"


virilList = []
with open(dVirilPath) as gff:
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
        virilList.append(attribute)


        
#print(virilList)
#print(genesTF)




dViril_Anno = pd.DataFrame(virilList, columns=['attribute'])


matches = []
# iterate genes and look for them inside each GFF attribute string
for _, row in genesTF.iterrows():
    gene = row["genes"]
    hog = row["hog"]
    found = False
    #loops through 
    for attr in dViril_Anno["attribute"]:
        if re.search(gene, attr):
            matches.append({"genes": gene, "hog": hog, "attribute": attr})
            found = True
    #for safety. i hope
    if not found:
        matches.append({"genes": gene, "hog": hog, "attribute": pd.NA})

complete = pd.DataFrame(matches)
#merged dataframe
#print(complete)


#checks to see if attribute collum has the parent gene
to_check = "Parent"
complete= complete[complete['attribute'].str.contains(to_check, na=False)]

print(complete)
    


#new_stuff = genesTF["genes"].isin(dViril_Anno)

#print(new_stuff)
#print(dViril_Anno)
#print(dViril_Anno.loc[0,"attribute"])
#print(type(genesTF.loc[0,"genes"]))



#answer = []
#gene = str(genesTF.loc[0,"genes"])
# for items in virilList:
#     to_add = re.search(item, gene)
#     if str(to_add)== str(genesTF.loc[0,"genes"]):
#         answer.append(to_add)
    #     answer = "yes"
    # else:
    #     answer = "no"

#print(genesTF.loc[0,"genes"])
#print(answer)

#mask = genesTF["genes"].isin(dViril_Anno["attribute"])

#print(genesTF[mask])

#print(genesTF)
#print(dViril_Anno.head(5))
