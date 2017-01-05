import csv
from sortedcontainers import SortedDict


CHROM = 0; POS = 1; ID = 2; REF = 3; ALT = 4; QUAL = 5; FILTER = 6; INFO = 7; FORMAT = 8; G = 9
CHR = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
       '20', '21', '22', 'X', 'Y']
HEADER = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'G', 'C_DP']


def de_novo(children_files, mother_file=None, father_file=None,
         exac_file=None, exac_ac=None,
         thwes_file=None, thwes_ac=None):

    if not check_ac(exac_file, exac_ac, thwes_file, thwes_ac):
        return

    de_novo = dict()
    sorted_m_depth = dict()
    sorted_f_depth = dict()

    if mother_file:
        HEADER.append('M_DP')
        m_variant, m_depth = get_variant_and_depth(mother_file)
        for chro in CHR:
            sorted_m_depth[chro] = SortedDict((key, value) for key, value in m_depth[chro].items())
    if father_file:
        HEADER.append('F_DP')
        f_variant, f_depth = get_variant_and_depth(father_file)
        for chro in CHR:
            sorted_f_depth[chro] = SortedDict((key, value) for key, value in f_depth[chro].items())

    for child_file in children_files:
        c_variant, var_count = get_variant_and_count(child_file)

        for chro in CHR:
            if mother_file: de_novo[chro] = c_variant[chro].difference(m_variant[chro])
            if father_file: de_novo[chro] = c_variant[chro].difference(f_variant[chro])

        if exac_file:
            de_novo = filter_by_exac(de_novo, exac_file, exac_ac)
        if thwes_file:
            de_novo = filter_by_thwes(de_novo, thwes_file, thwes_ac)

        export_csv(child_file, de_novo, sorted_m_depth, sorted_f_depth, var_count)


def filter_by_exac(de_novo, exac_file, max_ac):
    read_en = False
    f = open(exac_file, "r")
    count = 0
    for row in csv.reader(iter(f.readline, '')):
        srow = "".join(row)
        words = srow.split()
        if read_en:
            chro = words[CHROM]
            pos = int(words[POS])
            ac = get_ac(words[INFO])
            if ac > max_ac:
                try:
                    de_novo[chro].remove(pos)
                    count += 1
                    print('removed by exac', chro, pos)
                except KeyError:
                    pass
        if words[CHROM] == '#CHROM':
            read_en = True
    print("filtered by thwes", count)
    return de_novo


def filter_by_thwes(de_novo, thwes_file, max_ac):
    read_en = False
    f = open(thwes_file, "rb")
    # f = codecs.open(thwes_file, 'rU', 'utf-8')
    count = 0
    for row in csv.reader(iter(f.readline, '')):
        srow = "".join(row)
        words = srow.split()
        if read_en:
            chro = words[CHROM][3:]
            pos = int(words[POS])
            ac = get_ac(words[INFO])
            if ac > max_ac:
                try:
                    de_novo[chro].remove(pos)
                    count += 1
                    print("removed by thwes", chro, pos)
                except KeyError:
                    pass
        if words[CHROM] == '#CHROM':
            read_en = True
    print("filtered by thwes", count)
    return de_novo


def export_csv(child_file, de_novo, sorted_m_depth, sorted_f_depth, var_count):
    name = get_name(child_file) + "-filtered"
    de_novo_count = 0
    with open(name+'.csv', 'wb') as csvfile:
        data_writer = csv.writer(csvfile)
        read_en = False
        header_row = HEADER
        data_writer.writerow(header_row)
        for row in list(open(child_file, "rb")):
            words = row.strip().split()
            if read_en:
                output_row = get_all_info(words, de_novo)
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
        data_writer.writerow(['variant', de_novo_count, var_count])


def get_all_info(words, de_novo):
    output_row = []
    if words[QUAL] != '.':
        chro = words[CHROM][3:]
        if int(words[POS]) in de_novo[chro]:
            output_row.extend(words)
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
    for row in list(open(filename, "rb")):
        words = row.strip().split()
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
    for row in list(open(filename, "r")):
        words = row.strip().split()
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
    # i = bisect_left(a, x)
    # if i != len(a) and a[i] == x:
    #     return i
    if position in sorted_dp_dict[chro].keys():
        print("found")
        return int(sorted_dp_dict[chro][pos])
    else:
        index = sorted_dp_dict[chro].bisect(pos)
        key = sorted_dp_dict[chro].iloc[index - 1]
        print('not found', 'chr', chro, 'position', position, 'use', key, 'instead')
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
    start = filename.find('G')
    end = filename.find('.', start)
    return filename[start:end]


def check_ac(exac_file=None, exac_ac=None,
             thwes_file=None, thwes_ac=None):
    if exac_file and not exac_ac:
        print("Please input upper bound of AC of ExAC filtering")
        return False
    if thwes_file and not thwes_ac:
        print("Please input upper bound of AC of THWES filtering")
        return False
    return True
