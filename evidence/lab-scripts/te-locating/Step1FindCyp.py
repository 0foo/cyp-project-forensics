#import pandas as pd

#Gff file
GFF = 'GFF/dmel-all-r6.67.gff'

rgFile ="Reg_Gene_Full.txt"

stripGFF = []
regGene = []

with open(rgFile, mode = "r", encoding="utf-8") as t:
    for gene in t:
        if gene.startswith('D'):
           continue
        regGene.append(gene.rstrip('\n'))
        #print(gene)
        

with open(GFF, mode = "r", encoding="utf-8") as s:

    for line in s:
        if line.startswith("#"):
            continue
        fields = line.rstrip("\n").split("\t")

        for Rgene in regGene:
            print(Rgene)
            if fields[2] == "gene" and Rgene in fields[8]:
                stripGFF.append(line)
            
    print(stripGFF)


with open("step1Temp.gff", "w", encoding="utf-8") as out:
    for row in stripGFF:
          out.write(row)

print('done')