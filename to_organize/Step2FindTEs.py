#cyp genes that are affected by TEs
cypGene = "step1Temp.gff"

#All possible TEs (fasta files)
TEs = 'FilesFromMasker\dmel-all-chromosome-r6.67.fasta.out'

with open(cypGene, mode="r", encoding="utf-8") as cyp,open(TEs, mode="r", encoding="utf-8") as te, open("step2GenesAffectedByTEs.txt", mode="w", encoding="utf-8") as out:
    # preload TE file lines so we can iterate multiple times safely
    te_lines = [line.rstrip('\n') for line in te if line.strip()]

    for gene in cyp:
        gene = gene.strip()

        if not gene:
            continue

        cypFields = gene.split("\t")
        #print(cypFields)
        if len(cypFields) == 0:
            continue

        for ele in te_lines:
            eleFields = ele.split()
            # ensure expected column exists before indexing
            if len(eleFields) <= 4:
                continue
                
            start = int(cypFields[3]) - 3000
            stop = int(cypFields[4]) + 3000
            


            #print(eleFields[5])
            if cypFields[0] == eleFields[4] and (int(eleFields[6])<= stop and int(eleFields[5]) >= start):
               
                line = f"{cypFields[0]}\t{cypFields[8]}\t{ele}\n"
                out.write(line) 
print('done')
