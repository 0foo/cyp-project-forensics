
Annotation_file = open("DROSOPHILA_MELANOGASTER_final.gff","r")
Output_file = open("DROSOPHILA_MELANOGASTER_StartsandStops.gff","w")

Annotation_lines = Annotation_file.readlines()

for line in Annotation_lines:
    parts = line.split("\t")
    if len(parts) > 2:
        ID = parts[2]
        if ID == "start_codon":
            Output_file.write(line)
        if ID == "stop_codon":
            Output_file.write(line)

    
    
Output_file.close()
Annotation_file.close()
   