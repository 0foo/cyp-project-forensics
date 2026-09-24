import pandas as pd
import gffpandas.gffpandas as gffpd
import numpy as np
from BCBio import GFF
import re
#pandas is used to make working with csv/tsv/gff file easier
#12/14/2025 i lied
#12/15/2025
#gff file is too big to load so load it in chunks
#gff pandas is useless
#import BIOpython

hogogPath = "B:/Copy_toDuy/Copy_toDuy/Test_Duy/textfiles/HOG_OG_association_gene_names_without_duplicates_10_31.tsv"

hogog_df = pd.read_csv(hogogPath, sep = "\t", low_memory=False)


#for i, row in hogog_df.head(5).iterrows():
 #   print(i,row)

#puts fly names into an array for looping later
flyName = []
for label,value in hogog_df.head(0).items():
    flyName.append(str(label))

#janky removal of labels
flyName.remove("HOG")
flyName.remove("OG")
flyName.remove("Gene Tree Parent Clade")
#print(flyName)

#^^^^ puts all the fly names into a list called flyName

#testing the D.Virilis and finding its hog genes

testName = "DROSOPHILA_VIRILIS"
hog = "HOG"

#print(hogog_df[hogGenes])

#using numpy and pandas to create new data frame that contains only HOG and D,Virilis gene association,

#HOGVirilAssoc = np.array([hogog_df[hog]], [hogog_df[testName]])

#HOGVirilAssoc_df = pd.DataFrame(HOGVirilAssoc, columns=["HOG", "gene"])
#print(HOGVirilAssoc_df)


#Left note: So use 2d array and figure out how to make another dataframe ^^^^^ it not running for some reason figure that out how to put them together with 2 collums.
# it should be HOG and GENE as the collumns.
# 
# 12/14/2025 change of plans

#created a subset of HOG and genes of the species. replace species with flyNames[i] (all names in flyNames array)
key =  hogog_df[hog] #this is the genes in Virilis
value = hogog_df[testName] #this is the HOG. Its reversed. Too lazy to change every variable. ill change it for final product.
data = {"HOG": hogog_df[hog], "genes" :hogog_df[testName]}
#VirilDic = dict(zip(key,value))
#print(VirilDic)
viril_df = pd.DataFrame(data)


print(viril_df)

### Left Note : ok so replace the name and the parent name (in the annotation) wiht HOG (H00003. etc) and ID (in annotation) is gene-000020 etc.
# figure out how to loop through and get all the data from a cell of the dataframe and then scan through the .gff files for the old name and replace it with the new name
#format idea : "Name"= ,"Old Name"=, "ID"=  


### 12/15 reading into the gff file with pandas
dVirilPath = "B:/Copy_toDuy/Copy_toDuy/Test_Duy/Annotations_12_species/Annotations_12_species/DROSOPHILA_VIRILIS_final.gff"

# dVirilAnno =  gffpd.read_gff3(dVirilPath)

# df = dVirilAnno.df
# header = dVirilAnno.header
#cannot use this method because it runs into memory issues. it is to big to load at once

#dViril_Anno = pd.DataFrame(columns=['attribute'])
#print(dViril_Anno)
#i = 0
#set up counter for the rows in the df loop
# dVirilPath = "B:/Copy_toDuy/Copy_toDuy/Test_Duy/Annotations_12_species/Annotations_12_species/DROSOPHILA_VIRILIS_final.gff"
# in_handle = open(dVirilPath)
# for rec in GFF.parse(in_handle, target_lines=50):
    
#         dViril_Anno = pd.concat([dViril_Anno, pd.DataFrame([row_data])], ignore_index=True)
# print(dViril_Anno)
# in_handle.close()

##left off
#read into the gff file and use regex to find out how to match genes to names

# 12/16 
#scans file 
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
        
    dViril_Anno = pd.DataFrame(virilList, columns=['attribute'])
   # print(dViril_Anno)

###Left off:
# figured out how to add the ID attribute into a dataframe now figure out how to loop through df "viril_df" and df "dVirili_Anno" 
# and find out which names/genes matches with HOG
#2/3 done. Figure out what is wrong with Terry's looping problem.

#12/17 
#ok make a function that would separate genes in the viril_df[genes] into 2 separate series and delete the NaN HOG from df
# def count_gene(count, VirilDic[k]):
#     return
# #figure this out tmr

# def clean_up_DViril(VirilDic):
#    # arr = {}
#     for k in list(VirilDic.keys()):
#         if str(VirilDic[k])=="nan":
#             del VirilDic[k]
#     for k in list(VirilDic.keys()):
#         count = str(VirilDic[k]).count(",")
#         if count > 0:
#             count_gene(count, VirilDic[k])
#     return VirilDic

# viril_df = clean_up_DViril(VirilDic)

# df = pd.DataFrame(viril_df.keys(),viril_df.values())

# print(df)

## how datacleanigng with work
#array_with_flyName -> search for flyname in .gff psuedoDB (haven't made)-> find the flyName[i] on the table and match hog with fly gene. Make it into df ->
# create df of flyname[i] annotation and take its attributes and turn it int df
# -> take flygene_HOG df and match it with appropirate annotation attribute
    
#removed NAN from key list. figure out how to split the keys apart and map them to the same value
        
