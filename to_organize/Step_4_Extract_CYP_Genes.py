HOG_OG_association_gene_counts_file = open("Output/HOG_OG_association_gene_counts_10_31.tsv", "r")
output = open("Output/HOG_OG_Cyp_gene_counts_11_5.tsv", "w")

Stable_cyp_genes_list = open("2025_07_Dhakad_et_al_2025_Data/Updated_Cyp_stable_genes_with_HOGs_Good_et_al_2014.txt", "r")
Unstable_cyp_genes_list = open("2025_07_Dhakad_et_al_2025_Data/Updated_Cyp_unstable_genes_with_HOGs_Good_et_al_2014.txt", "r")

HOG_lines = HOG_OG_association_gene_counts_file.readlines()

Stable_lines = Stable_cyp_genes_list.readlines()
Unstable_lines = Unstable_cyp_genes_list.readlines()
#Stable_genes = {}
CYP_genes = {}

fields_counter = 0
for line in Stable_lines:
	fields = line.rstrip("\n").split("\t")
	if (fields_counter > 0):
		HOG_fields = fields[1].split(",")
		#Stable_genes[fields[1]] = [fields[0]]
		for HOGs in HOG_fields:
			CYP_genes[HOGs] = [fields[0]]
	fields_counter = fields_counter + 1

for line in Unstable_lines:
	fields = line.rstrip("\n").split("\t")
	if (fields_counter > 0):
		HOG_fields = fields[1].split(",")
		for HOGs in HOG_fields:
			CYP_genes[HOGs] = [fields[0]]
	fields_counter = fields_counter + 1


print("dictionary before", CYP_genes)
CYP_counter = 0
for line in HOG_lines:
	fields = line.rstrip("\n").split("\t")
	HOG_number = fields[0]
	if HOG_number in CYP_genes:
		##CYP = CYP_genes[HOG_number]
		CYP = CYP_genes.get(HOG_number)
		#print("This works!", HOG_number, CYP)
		CYP_write = str(CYP).strip("['']")
		output.write(CYP_write)
		output.write("\t")
		output.write(line)
		del CYP_genes[HOG_number]
		#CYP_genes.pop(CYP_write)
		#print(CYP_write)

print("dictionary after", CYP_genes)
output.close()

	