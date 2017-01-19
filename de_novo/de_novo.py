import csv
from _csv import QUOTE_NONE
from sortedcontainers import SortedDict

from config.settings import BASE_DIR

CHROM = 0; POS = 1; ID = 2; REF = 3; ALT = 4; QUAL = 5; FILTER = 6; INFO = 7; FORMAT = 8; G = 9
CHR = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
       '20', '21', '22', 'X', 'Y']
HEADER = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'G']


def de_novo(children_files, output_name, mother_file=None, father_file=None):

    header = []
    de_novo = dict()
    sorted_m_depth = dict()
    sorted_f_depth = dict()

    if mother_file:
        header.append(get_name(mother_file) + '_DP')
        m_variant, m_depth = get_variant_and_depth(mother_file)
        for chro in CHR:
            sorted_m_depth[chro] = SortedDict((key, value) for key, value in m_depth[chro].items())
    if father_file:
        header.append(get_name(father_file) + '_DP')
        f_variant, f_depth = get_variant_and_depth(father_file)
        for chro in CHR:
            sorted_f_depth[chro] = SortedDict((key, value) for key, value in f_depth[chro].items())

    for child_file in children_files:
        c_variant, var_count = get_variant_and_count(child_file)
        for chro in CHR:
            if mother_file:
                de_novo[chro] = c_variant[chro].difference(m_variant[chro])
            if father_file:
                de_novo[chro] = c_variant[chro].difference(f_variant[chro])

        export_vcf(child_file, de_novo, sorted_m_depth, sorted_f_depth, var_count, output_name, header)


def export_vcf(child_file, de_novo, sorted_m_depth, sorted_f_depth, var_count, output_name, header):
    output_path = BASE_DIR + '/output/' + output_name + '.vcf'
    de_novo_count = 0
    dont_have_DP = False
    with open(output_path, 'w') as vcfFile:
        data_writer = csv.writer(vcfFile, delimiter="\t", lineterminator="\n", quotechar='', quoting=QUOTE_NONE)
        read_en = False
        rf = open(child_file, "r")
        reader = csv.reader(rf, delimiter="\t")
        for words in reader:
            if read_en:
                output_row = get_all_info(words, de_novo, dont_have_DP)
                pos = int(words[POS])
                if len(output_row) != 0:
                    try:
                        output_row.append(get_dp_from_dict(words[CHROM][3:], pos, sorted_m_depth))
                    except:
                        print("skip mother depth")
                    try:
                        output_row.append(get_dp_from_dict(words[CHROM][3:], pos, sorted_f_depth))
                    except:
                        print("skip father depth")
                    data_writer.writerow(output_row)
                    de_novo_count += 1
            if words[CHROM] == "#CHROM":
                read_en = True
                if 'DP' in words:
                    data_writer.writerow(words + header)
                else:
                    data_writer.writerow(words + ['DP'] + header)
                    dont_have_DP = True
            if read_en == False and words[CHROM].find("##") != -1:
                data_writer.writerow(words)
        data_writer.writerow(['variant', de_novo_count, var_count])


def get_all_info(words, de_novo, dont_have_DP):
    output_row = []
    if words[QUAL] != '.':
        chro = words[CHROM][3:]
        if int(words[POS]) in de_novo[chro]:
            output_row.extend(words)
            if dont_have_DP:
                output_row.append(get_dp(words[INFO], words[G]))
    return output_row


def get_all_col(words, de_novo):
    output_row = []
    if words[QUAL] != '.':
        chro = words[CHROM][3:]
        if int(words[POS]) in de_novo[chro]:
            output_row.extend(words)
    return output_row


def get_variant_and_count(filename):
    read_en = False
    var_count = 0
    variant = dict()
    for chro in CHR:
        variant[chro] = set()
    for line in list(open(filename, "r")):
        words = line.strip().split()
        if read_en and words[QUAL] != '.':
            chro = words[CHROM][3:]
            variant[chro].add(int(words[POS]))
            var_count += 1
        if words[CHROM] == "#CHROM":
            read_en = True
    return variant, var_count


def get_variant_and_depth(filename):
    read_en = False
    variant = dict()
    depth = dict()
    for chro in CHR:
        variant[chro] = set()
        depth[chro] = dict()
    for line in list(open(filename, "r")):
        words = line.strip().split()
        if read_en:
            chro = words[CHROM][3:]
            pos = int(words[POS])
            if words[QUAL] != '.':
                variant[chro].add(pos)
            try:
                depth[chro][pos] = get_dp(words[INFO], words[G])
            except KeyError:
                pass
        if words[CHROM] == "#CHROM":
            read_en = True
    return variant, depth


def get_dp_from_dict(chro, pos, sorted_dp_dict):
    position = int(pos)
    if position in sorted_dp_dict[chro].keys():
        # print("found")
        return int(sorted_dp_dict[chro][pos])
    else:
        index = sorted_dp_dict[chro].bisect(pos)
        key = sorted_dp_dict[chro].iloc[index - 1]
        # print('not found', 'chr', chro, 'position', position, 'use', key, 'instead')
    return int(sorted_dp_dict[chro][key])


def get_dp(info, g):
    start = info.find('DP=')
    if start != -1:
        start += 3
        end = info.find(';', start)
    else:
        start = g.find(':') + 1
        end = g.find(':', start)
    return int(info[start:end])


def get_ac(info):
    start = info.find('AC=')
    start += 3
    end = info.find(';', start)
    return int(info[start:end])


def get_name(filename):
    start = filename.rfind('\\')
    if start == -1:
        start = 0
    else:
        start += 1
    print(start)
    end = filename.find('.', start)
    return filename[start:end]

