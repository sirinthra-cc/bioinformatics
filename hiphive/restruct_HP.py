def hp_id_search(keyword):

    hp_file = open("database/hp2.obo", 'r')
    omim_file = open("database/OMIM_ALL_FREQUENCIES_diseases_to_genes_to_phenotypes.txt", 'r')
    lines = tuple(omim_file)
    data = dict()
    result = []
    for i in range(len(lines)):
        if lines[i].find(keyword,5,11) == 5:
            words = lines[i].split("\t")
            result.append((words[3],words[4].strip()))
    lines = tuple(hp_file)
    for i in range(len(lines)):
        if lines[i].find("id", 0, 2) == 0:
            id_temp = lines[i][-7:].strip()
            data[id_temp] = []

        elif lines[i].find("name", 0, 4) == 0:
            data[id_temp].append([lines[i][6:].strip(),"name"])
            #print(id_temp,data[id_temp])
        elif lines[i].find("def", 0, 3) == 0:
            data[id_temp].append([lines[i][6:].strip(),"def"])
            #print(id_temp,data[id_temp])

        elif lines[i].find("alt_id", 0, 6) == 0:
            data[id_temp].append([lines[i][9:].strip(),"alt_id"])
            #print(id_temp,data[id_temp])

        elif lines[i].find("xref", 0, 4) == 0:
            data[id_temp].append([lines[i][7:].strip(),"xref"])
            #print(id_temp,data[id_temp])



    for x in data:
        for y in data[x]:
            if y[0].find(keyword, 0, len(y[0])) > 0 and y[1] == "name":
                result.append(("HP:"+x, data[x][0][0]))
                data[x] = []
               # print("append name")
                break
    for x in data:
        for y in data[x]:
            if y[0].find(keyword, 0, len(y[0])) > 0 and y[1] == "def":
                result.append(("HP:"+x, data[x][0][0]))
                data[x] = []
              #  print("append def")
                break
    for x in data:
        for y in data[x]:
            if y[0].find(keyword, 0, len(y[0])) > 0 and y[1] == "alt_id":
                result.append(("HP:"+x, data[x][0][0]))
                data[x] = []
               # print("append alt_id")
                break
    for x in data:
        for y in data[x]:
            if y[0].find(keyword, 0, len(y[0])) > 0 and y[1] == "xref":
                result.append(("HP:"+x, data[x][0][0]))
                data[x] = []
              #  print("append xref")
                break
    return result