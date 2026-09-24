path = 'GFF\dmel-all-r6.67.gff'

with open(path, mode = 'r', encoding='utf-8') as gff:
    for line in gff:
        print(line)