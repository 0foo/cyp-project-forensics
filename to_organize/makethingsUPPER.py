import csv

path = 'C:/Users/User/Documents/BioAtallah/TerryPoster/reWorked/species.csv'
outPath = 'C:/Users/User/Documents/BioAtallah/TerryPoster/reWorked/new_species.csv'

with open(path, 'r', encoding='utf-8', newline='') as infile, open(outPath, 'w', encoding='utf-8', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        capitalized_row = [cell.upper() for cell in row]
        writer.writerow(capitalized_row)
