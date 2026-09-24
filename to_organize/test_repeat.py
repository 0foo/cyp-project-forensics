path = 'C:/Users/User/Documents/BioAtallah/RepeatMasker/fastaFiles/Drosophila_melanogaster.GCF_000001215.4.rm.fna'

with open(path, "r", encoding = 'utf-8') as file:
    for l in file :
        print(l)