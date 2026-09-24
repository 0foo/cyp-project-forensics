toClean =  'step2GenesAffectedByTEs.txt'

aliasToFind = 'Reg_Gene_Full.txt'
with open(toClean, mode = 'r',encoding = 'utf-8') as file, open(aliasToFind, mode = 'r', encoding = 'utf-8') as names, open('output/D_Mel_FlyBase_GenesAffectedByTE.txt', mode = 'w', encoding = 'utf-8') as out: 
    nameList = []
    container = []

    for name in names:
        nm = name.strip()
        if not nm:
            continue
        if nm.startswith("D"):
            continue
        nameList.append(nm)
    #print(nameList)


    for line in file:
        fields = line.rstrip("\n").split("\t")
        if len(fields) < 2:
            container.append(fields)
            continue

        for name in nameList:
            if name in fields[1]:
                fields[1] = name
                break
        container.append(fields)

    for ele in container:
        out.write("\t".join(ele) + "\n")

print('done')