import csv
from config.settings import BASE_DIR


CHROM = 0; POS = 1; ID = 2; REF = 3; ALT = 4; QUAL = 5; FILTER = 6; INFO = 7; FORMAT = 8; G = 9; REVEL_SCORE = 6;
CHR = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
       '20', '21', '22', 'X', 'Y']
HEADER = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'G']
revel_ref = BASE_DIR + "/database/Revel_all_chromosomes.csv"
exac_ref = BASE_DIR + "/database/variant.153.csv"
thwe_ref = BASE_DIR + "/database/variant.153.csv"


def get_variant_and_depth(filename):
    read_en = False
    variant = dict()
    for chro in CHR:
        variant[chro] = dict()

    for row in list(open(filename, "r")):
        words = row.strip().split()
        if read_en:
            chro = words[CHROM][3:]
            pos = int(words[POS])
            if words[QUAL] != '.':
                variant[chro][pos] = [words[REF], words[ALT]]
        if words[CHROM] == "#CHROM":
            read_en = True
    return variant


def get_ac(info):
    start = info.find('AC=')
    start += 3
    end = info.find(';', start)
    return int(info[start:end])


def filtration(var_file, output_name, revel_max=None, exac_min=None, thwe_min=None):
    var_dict = get_variant_and_depth(var_file)
    output_path = BASE_DIR + '/output/' + output_name + '.vcf'
    read_en = False
    if revel_max:
        f = open(revel_ref, 'r')
        for words in csv.reader(iter(f.readline, '')):
            if read_en:
                chro = words[CHROM][3:]
                pos = int(words[POS])
                revel_score = float(words[REVEL_SCORE])
                if revel_score < revel_max:
                    try:
                        if var_dict[chro][pos] == [words[REF], words[ALT]]:
                            var_dict[chro].pop(pos, None)
                    except KeyError:
                        pass
            if words[CHROM] == 'chr':
                read_en = True

    read_en = False
    if exac_min:
        f = open(exac_ref, 'r')
        for row in csv.reader(iter(f.readline, '')):
            srow = "".join(row)
            words = srow.split()
            if read_en:
                chro = words[CHROM][3:]
                pos = int(words[POS])
                ac = get_ac(words[INFO])
                if ac > exac_min:
                    try:
                        var_dict[chro].pop(pos, None)
                    except KeyError:
                        pass
            if words[CHROM] == '#CHROM':
                read_en = True

    read_en = False
    if thwe_min:
        f = open(thwe_ref, 'r')
        for row in csv.reader(iter(f.readline, '')):
            srow = "".join(row)
            words = srow.split()
            if read_en:
                chro = words[CHROM][3:]
                pos = int(words[POS])
                ac = get_ac(words[INFO])
                if ac > thwe_min:
                    try:
                        var_dict[chro].pop(pos, None)
                    except KeyError:
                        pass
            if words[CHROM] == '#CHROM':
                read_en = True

    write_file(var_file, var_dict, output_path)
    return var_dict


def write_file(var_file, to_be_written_dict, output_path):
    rf = open(var_file, 'r')
    wf = open(output_path, 'w', newline='')

    try:
        writer = csv.writer(wf, delimiter='\t')
        reader = csv.reader(rf, delimiter='\t')
        read_en = False
        for row in reader:
            if read_en:
                if int(row[POS]) in to_be_written_dict[row[CHROM][3:]]:
                    writer.writerow(row)
            elif row[0] == "#CHROM":
                read_en = True
                writer.writerow(HEADER)
            else:
                writer.writerow(row)
    finally:
        rf.close()
        wf.close()
