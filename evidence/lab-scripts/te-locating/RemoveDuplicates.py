seen = set()

with open("DROSOPHILA_MELANOGASTER_withTEsandTFBSs.gff", "r") as lines_in, open("DROSOPHILA_MELANOGASTER_withTEsandTFBSsNoDuplicates.gff", "w") as Lines_out:
	for line in lines_in:
		if line not in seen:
			Lines_out.write(line)
			seen.add(line)
			
			
			