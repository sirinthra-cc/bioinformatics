import csv
import codecs
import time
from collections import defaultdict
#from sortedcontainers import SortedDict


CHROM = 0; POS = 1; ID = 2; REF = 3; ALT = 4; QUAL = 5; FILTER = 6; INFO = 7; FORMAT = 8; G = 9
CHR = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
       '20', '21', '22', 'X', 'Y']
HEADER = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'G']
HEADER_ROW = []


def extract_info(filename):
    f = open(filename, 'r')

    try:
        reader = csv.reader(f)
        read_en = False  # creates the reader object
        add_col = defaultdict(list)
        for row in reader:  # iterates the rows of the file in orders
            # words = row.strip().split()
            if read_en:
                sep_info = row[7].split(";")
                for s in sep_info:
                    sep_s = s.split("=")
                    if(len(sep_s) == 2):
                        add_col[sep_s[0]].append(sep_s[1])
            if row[0] == "#CHROM":
                read_en = True
                print("Found #CHROM")
    finally:
        f.close()  # closing
    return add_col


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

def extract_and_write(inputfile, outputfile):
    rf = open(inputfile, 'r')
    wf = open(outputfile, 'w',newline='')
    #key_list = add_column.keys()

    try:
        writer = csv.writer(wf)
        reader = csv.reader(rf)
        read_en = False
        for row in reader:  # iterates the rows of the file in orders
            # words = row.strip().split()
            if read_en:
                #for value in add_column:
                #for key in key_list:
                #    row.append(add_column[key][count])
                #writer.writerows(row)
                #count = count + 1
                sep_info = row[7].split(";")
                add_info = []
                count = 0;
                for s in sep_info:
                    sep_s = s.split("=")
                    if count < 10:
                        if (len(sep_s) == 2):
                            add_info.append(sep_s[1])
                        else : add_info.append(s)
                    count = count + 1
                writer.writerow(row + add_info)
            elif row[0] == "#CHROM":
                read_en = True
                #iter_row = iter(reader)
                row2 = next(reader)
                sep = row2[7].split(";")
                add_header = []
                count2 = 0
                for s in sep:
                    sep_s = s.split("=")
                    if count2 < 10:
                        if (len(sep_s) == 2):
                            add_header.append(sep_s[0])
                    count2 = count2+1
                writer.writerow(row + add_header)
                print("Found #CHROM")
            else :
                writer.writerow(row)
    finally:
        rf.close()
        wf.close()# closing

def extract_and_write2(inputfile, outputfile):
    rf = open(inputfile, 'r')
    wf = open(outputfile, 'w',newline='')
    #key_list = add_column.keys()

    try:
        #writer = csv.writer(wf)
        reader = rf.readlines()
        read_en = False
        at_header = False
        info_count = 9
        for line in reader:  # iterates the rows of the file in orders
            # words = row.strip().split()
            row = line.split('\t')
            row[len(row)-1] = (row[len(row)-1].split('\n'))[0]
            #row[len(row) - 1].strip('\n')
            if read_en:
                #for value in add_column:
                #for key in key_list:
                #    row.append(add_column[key][count])
                #writer.writerows(row)
                #count = count + 1
                if count3 == 0:
                    sep = row[7].split(";")
                    #print(row[7])
                    #print(sep)
                    if (sep[2].split('=')[0]) == 'ANN':
                        info_count = 10
                    add_header = []
                    count2 = 0
                    for s in sep:
                       sep_s = s.split("=")
                       if count2 < info_count:
                           if (len(sep_s) == 2):
                               add_header.append(sep_s[0])
                       count2 = count2 + 1
                    # print(row+add_header)
                    wf.write('\t'.join(HEADER_ROW + add_header))
                    wf.write('\n')
                    count3 = 10

                sep_info = row[7].split(";")
                add_info = []
                count = 0;
                for s in sep_info:
                    sep_s = s.split("=")
                    if count < info_count:
                        if (len(sep_s) == 2):
                            add_info.append(sep_s[1])
                        else : add_info.append(s)
                    count = count + 1
                    #print(row + add_info)
                wf.write('\t'.join(row + add_info))
                wf.write('\n')
            elif row[0] == "#CHROM":
                read_en = True
                count3 = 0
                HEADER_ROW = row
                #sep = row[7].split(";")
                #print(row[7])
                #print(sep)
                #add_header = []
                #count2 = 0
                #for s in sep:
                #    sep_s = s.split("=")
                #    if count2 < 9:
                #        if (len(sep_s) == 2):
                #            add_header.append(sep_s[0])
                #    count2 = count2 + 1
                #print(add_header)
                #add_header = ['AC1', 'AF1','ANN', 'DP', 'DP4', 'EXOMISER_GENE', 'EXOMISER_GENE_COMBINED_SCORE', 'EXOMISER_GENE_PHENO_SCORE', 'EXOMISER_GENE_VARIANT_SCORE', 'EXOMISER_VARIANT_SCORE']
                #print(row+add_header)
                #wf.write('\t'.join(row + add_header))
                #wf.write('\n')
                #at_header = False
                #print("Found #CHROM")
                #iter_row = iter(reader)


            else :
                wf.write('\t'.join(row))
                wf.write('\n')
    finally:
        rf.close()
        wf.close()# closing