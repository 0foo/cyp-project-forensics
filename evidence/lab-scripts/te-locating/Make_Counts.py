from unittest import skip


TE_file = open("Dmel_TFBS_in_interesting_TEs_with_TF_names.txt","r")
Output_file = open("Dmel_TFBS_and_TE_totals.txt","w")

TE_lines = TE_file.readlines()

Cyp_gene_list = []
TE_ID_list = []

for line in TE_lines:
	sections = line.split("\t")
	Cyp_gene = sections[1]
	#print(Cyp_gene)
	if Cyp_gene in Cyp_gene_list:
		cont = 1
	else:
		Cyp_gene_list.append(Cyp_gene)
#print(Cyp_gene_list)

for Cyp_gene in Cyp_gene_list:
	print(Cyp_gene)

	TE_ID_list = []
	TE_total_list = []
	TFBS_ID_list = []
	TFBS_total_list = []
	for line in TE_lines:
		#print("starting new line")
		sections = line.split("\t")
		if sections[1] == Cyp_gene:
			TE_name = sections[6]
			TE_start = sections[7]
			TE_stop = sections[8].strip("\n")
			TE_unique_ID = TE_name + ":" + TE_start + "-" + TE_stop
			if TE_unique_ID in TE_ID_list:
				TE_total_list.append(TE_name)
			else:
				TE_total_list.append(TE_name)
				TE_ID_list.append(TE_unique_ID)
			TFBS_name = sections[2]
			TFBS_start = sections[3]
			TFBS_stop = sections[4]
			TFBS_unique_ID = TFBS_name + ":" + TFBS_start + "-" + TFBS_stop
			if TFBS_unique_ID in TFBS_ID_list:
				TFBS_total_list.append(TFBS_name)
			else:
				TFBS_total_list.append(TFBS_name)
				TFBS_ID_list.append(TFBS_unique_ID)
	#print(TE_total_list)
	#print(TE_ID_list)
	
	TE_complete_count = len(TE_total_list)
	TE_unique_count = len(TE_ID_list)
	TFBS_complete_count = len(TFBS_total_list)
	TFBS_unique_count = len(TFBS_ID_list)

	Output_file.write(Cyp_gene)
	if Cyp_gene == "gene":

		Output_file.write("Total TE count" + "\t")
		Output_file.write("Unique TE count" + "\t")
		Output_file.write("Total TFBS count" + "\t")
		Output_file.write("Unique TFBS count" + "\t")
		Output_file.write("\n")
	else:

		Output_file.write("\t")
		Output_file.write(str(TE_complete_count))
		Output_file.write("\t")
		Output_file.write(str(TE_unique_count))
		Output_file.write("\t")
		Output_file.write(str(TFBS_complete_count))
		Output_file.write("\t")
		Output_file.write(str(TFBS_unique_count))
		Output_file.write("\n")
			

