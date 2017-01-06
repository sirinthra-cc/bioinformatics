def hp_id_search(keyword):

    hp_file = open("database/hp2.obo", 'r')
    lines = tuple(hp_file)
    data = dict()
    for i in range(len(lines)):
        if lines[i].find("id", 0, 2) == 0:
            id_temp = lines[i][-7:].strip()
            data[id_temp] = []

        elif lines[i].find("name", 0, 4) == 0:
            data[id_temp].append(lines[i][6:].strip())
        elif lines[i].find("def", 0, 3) == 0:
            data[id_temp].append(lines[i][6:].strip())
        elif lines[i].find("alt_id", 0, 6) == 0:
            data[id_temp].append(lines[i][9:].strip())
        elif lines[i].find("xref", 0, 4) == 0:
            data[id_temp].append(lines[i][7:].strip())

    result = []

    for x in data:
        for y in data[x]:
            if y.find(keyword, 0, len(y)) > 0:
                result.append((x, data[x][0]))
                break

    return result
