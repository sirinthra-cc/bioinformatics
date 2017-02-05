import csv
from _csv import QUOTE_NONE
from sortedcontainers import SortedDict

from config.settings import BASE_DIR

CHROM = 0; POS = 1; ID = 2; REF = 3; ALT = 4; QUAL = 5; FILTER = 6; INFO = 7; FORMAT = 8; G = 9
CHR = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
       '20', '21', '22', 'X', 'Y']


def common_novel(input_list, output_name):

    common_novel = dict()
    files = 0

    for input_file in input_list:
        c_variant = get_novel_variants(input_file)
        for chro in CHR:
            if files == 0:
                common_novel[chro] = c_variant[chro]
            else:
                common_novel[chro].intersection_update(c_variant[chro])
        files += 1

    export_vcf(input_list[0], common_novel, output_name)


def export_vcf(input_file, common_novel, output_name):
    output_path = BASE_DIR + '/output/' + output_name + '.vcf'
    common_novel_count = 0
    with open(output_path, 'w') as vcfFile:
        data_writer = csv.writer(vcfFile, delimiter="\t", lineterminator="\n", quotechar='', quoting=QUOTE_NONE)
        read_en = False
        rf = open(input_file, "r")
        reader = csv.reader(rf, delimiter="\t")
        for words in reader:
            if read_en:
                output_row = get_all_info(words, common_novel)
                if len(output_row) != 0:
                    data_writer.writerow(output_row)
                    common_novel_count += 1
            if words[CHROM] == "#CHROM":
                read_en = True
                data_writer.writerow(words)
            if read_en == False and words[CHROM].find("##") != -1:
                data_writer.writerow(words)
        data_writer.writerow(['variant', common_novel_count])


def get_all_info(words, common_novel):
    output_row = []
    chro = words[CHROM][3:]
    if int(words[POS]) in common_novel[chro]:
        output_row.extend(words)
    return output_row


def get_novel_variants(filename):
    read_en = False
    variant = dict()
    gene_type = 0
    for chro in CHR:
        variant[chro] = set()
        depth[chro] = dict()
    for line in list(open(filename, "r")):
        words = line.strip().split()
        if read_en:
            chro = words[CHROM][3:]
            pos = int(words[POS])
            if words[gene_type] == 'novel':
                variant[chro].add(pos)
        if words[CHROM] == "#CHROM":
            read_en = True
            for word in words:
                if word == "GENE TYPE":
                    break
                gene_type += 1
    return variant
