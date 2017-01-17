import csv
CHROM = 0; POS = 1; ID = 2; REF = 3; ALT = 4; QUAL = 5; FILTER = 6; INFO = 7; FORMAT = 8; G = 9; REVEL_SCORE = 6;
CHR = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
       '20', '21', '22', 'X', 'Y']
revel_ref = "/Users/jijy/Documents/indiv/revel_all_chromosomes.csv"
exac_ref = "/Volumes/My Passport/AnalysisTool/database/variant.153.csv"
thwe_ref = "/Volumes/My Passport/AnalysisTool/database/variant.153.csv"


def get_variant_and_depth(filename):
    read_en = False
    variant = dict()
    for chro in CHR:
        variant[chro] = set()

    for row in list(open(filename, "r")):
        words = row.strip().split()
        if read_en:
            chro = words[CHROM][3:]
            pos = int(words[POS])
            if words[QUAL] != '.':
                variant[chro].add(pos)

        if words[CHROM] == "#CHROM":
            read_en = True
    return variant


def get_ac(info):
    start = info.find('AC=')
    start += 3
    end = info.find(';', start)
    return int(info[start:end])


def filtration(var_file,mode_revel,mode_exac,mode_thwe,output_path):
    var_dict  = get_variant_and_depth(var_file)
    output = open(output_path, 'w')
    writer = csv.writer(output)
    read_en = False
    if mode_revel:
        f = open(revel_ref, 'r')
        for words in csv.reader(iter(f.readline, '')):
            if read_en:
                chro = words[CHROM][3:]
                pos = int(words[POS])
                revel_score = int(words[REVEL_SCORE])
                if revel_score < 0.05:
                    try:
                        var_dict[chro].remove(pos)
                    except KeyError:
                        pass
            if words[CHROM] == 'chr':
                read_en = True

    read_en = False

    if mode_exac:
        f = open(exac_ref, 'r')
        for row in csv.reader(iter(f.readline, '')):
            srow = "".join(row)
            words = srow.split()
            print(words)
            if read_en:
                chro = words[CHROM][3:]
                pos = int(words[POS])
                ac = get_ac(words[INFO])
                if ac > 10:
                    try:
                        var_dict[chro].remove(pos)
                    except KeyError:
                        pass
            if words[CHROM] == '#CHROM':
                read_en = True

    read_en = False

    if mode_thwe:
        f = open(thwe_ref, 'r')
        for row in csv.reader(iter(f.readline, '')):
            srow = "".join(row)
            words = srow.split()
            print(words)
            if read_en:
                chro = words[CHROM][3:]
                pos = int(words[POS])
                ac = get_ac(words[INFO])
                if ac > 1:
                    try:
                        var_dict[chro].remove(pos)

                    except KeyError:
                        pass
            if words[CHROM] == '#CHROM':
                read_en = True
    for row in var_dict:
        writer.writerows(var_dict[row])
    return var_dict
