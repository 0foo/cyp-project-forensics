output_file = open("Dmel_Cyp_stable_genes_Good_et_al_2014.txt", "w")
Dmel_CYP_gene_file = open("Dmel_Cyp_gene_list_Dermauw_2020.txt","r")
stable_gene_file = open("Cyp_stable_genes_Good_et_al_2014.txt","r")

stable_genes = {}

for line in stable_gene_file:
	line = line.rstrip("\n")
	Cyp_name = "Cyp" + line[3:].upper()
	stable_genes[Cyp_name] = "stable"

counter = 0
for line in Dmel_CYP_gene_file:
	line = line.rstrip("\n")
	fields = line.split("\t")
	stability = stable_genes.get(fields[1], "X")
	if (stability == "stable"):
		if (counter > 0):
			output_file.write("\n")
		output_file.write(line)
		counter = counter+1

Dmel_CYP_gene_file.close()
stable_gene_file.close()
output_file.close()
