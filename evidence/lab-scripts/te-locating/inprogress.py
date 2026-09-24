
TE_file = open("Dmel_TFBS_in_interesting_TEs_with_TF_names.txt","r")
Output_file = open("Dmel_TFBS_and_TE_totals.txt","w")

TE_lines = TE_file.readlines()

Cyp_gene_list = []
TE_ID_list = []
for line in TE_lines:
	sections = line.split("\t")
	Cyp_gene = sections[1]
	
	if Cyp_gene in Cyp_gene_list:
		cont = 1
		TE_name = sections[6]
		TE_start = sections[7]
		TE_stop = sections[8].strip("\n")
		TE_unique_ID = TE_name + ":" + TE_start + "-" + TE_stop


		if TE_unique_ID in TE_ID_list:
			cont = 1
		else:
			TE_ID_list.append(TE_unique_ID)
			
	else:
		Cyp_gene_list.append(Cyp_gene)
		TE_name = sections[6]
		TE_start = sections[7]
		TE_stop = sections[8].strip("\n")
		TE_unique_ID = TE_name + ":" + TE_start + "-" + TE_stop


		if TE_unique_ID in TE_ID_list:
			cont = 1
		else:
			TE_ID_list.append(TE_unique_ID)
			
print(Cyp_gene_list)
print(TE_ID_list)