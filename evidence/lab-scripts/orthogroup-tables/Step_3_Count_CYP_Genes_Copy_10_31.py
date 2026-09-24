import subprocess
import os
import re

HOG_OG_association_gene_names_without_duplicates_file = open("Output/HOG_OG_association_gene_names_without_duplicates_10_31.tsv","r")
output_file = open("Output/HOG_OG_association_gene_counts_10_31.tsv","w")

lines = HOG_OG_association_gene_names_without_duplicates_file.readlines()

#species_names = lines.rstrip("\n").split("\t")

lines_counter = 0
for line in lines:
    fields = line.split("\t")
    species_counter = 0
    if (lines_counter == 0):
        output_file.write(line)
    else:
        fields = line.rstrip("\n").split("\t")
        output_file.write(fields[0])
        output_file.write("\t")
        output_file.write(fields[1])
        output_file.write("\t")
        output_file.write(fields[2])
        output_file.write("\t")
        i = 3
        #for field in fields[i]:
        for field in fields:
           # print(field, "this is field")
            species_cyp_genes=[]
            #Cyp_Genes = field
            Gene = field.split(", ")
            for Genes in Gene:
                if len(Genes) == 0:
                    Genes = 0
                    #print("empty")
                else:
                    species_cyp_genes.append(Genes)
            species_cyp_count = len(species_cyp_genes)
           # print(species_cyp_genes)
            species_count = str(species_cyp_count)
            output_file.write(species_count)
           # print(species_counter, "species")
           # print(species_count, "genes")
            if (species_counter > 0):
                output_file.write("\t")
            species_counter = species_counter + 1
            i = i + 1
    if (lines_counter > 0):
        output_file.write("\n")
    lines_counter = lines_counter + 1
    
HOG_OG_association_gene_names_without_duplicates_file.close()
output_file.close()