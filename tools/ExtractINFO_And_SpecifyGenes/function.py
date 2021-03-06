import csv

def getEntrez(ref_file,Gene_list_file,output_file):
    reff = open(ref_file, 'r')
    gf = open(Gene_list_file, 'r')
    wf = open(output_file, 'w', newline='')

    try :
        ref_reader = csv.reader(reff)
        gl_reader = csv.reader(gf)
        writer = csv.writer(wf)

        read_en = False
        for row in ref_reader:
            if read_en:

                found_gene = False
                add_info = []
                gf.seek(0)
                for row2 in gl_reader:
                    if row[15] == row2[0]:
                        add_info.append(row2[3])
                        found_gene = True

                if not found_gene:
                    add_info.append("novel")

                writer.writerow(row + add_info)
            elif row[0] == "#CHROM":
                read_en = True
                # iter_row = iter(reader)
                add_header = ["gene_type"]
                writer.writerow(row + add_header)
                print("Found #CHROM")
            else:
                writer.writerow(row)
    finally:
        reff.close()
        gf.close()
        wf.close()


def specify_gene(ref_file, target_list, candidate_list, output_file):
    reff = open(ref_file, 'r')
    #gf = open(Gene_list_file, 'r')
    wf = open(output_file, 'w', newline='')
    hasANN = 0

    try:
        ref_reader = reff.readlines()
        #gl_reader = csv.reader(gf)
        #writer = csv.writer(wf)

        read_en = False
        for line in ref_reader:
            row = line.split('\t')
            row[len(row) - 1] = (row[len(row) - 1].split('\n'))[0]
            #row[len(row)-1].strip('\n')
            if read_en:

                found_target = False
                add_info = []
                #gf.seek(0)
                for t_gene in target_list:
                    if row[14 + hasANN] == t_gene:
                        add_info.append('target')
                        found_target = True

                if not found_target:
                    found_candidate = False
                    for c_gene in candidate_list:
                        if row[14 + hasANN] == c_gene:
                            add_info.append('candidate')
                            found_candidate = True
                    if not found_candidate:
                        add_info.append("novel")

                wf.writelines('\t'.join(row + add_info))
                wf.write('\n')
                #writer.writerow(row + add_info)
            elif row[0] == "#CHROM":
                read_en = True
                if row[12] == 'ANN':
                    hasANN = 1
                # iter_row = iter(reader)
                add_header = ["gene_type"]
                #print(row+add_header)
                wf.writelines('\t'.join(row + add_header))
                wf.write('\n')
                #writer.writerow(row + add_header)
                #print("Found #CHROM")
            else:
                wf.writelines('\t'.join(row))
                wf.write('\n')
    finally:
        reff.close()
        #gf.close()
        wf.close()


def specify_gene2(ref_file,Gene_list_file,output_file):
    reff = open(ref_file, 'r')
    gf = open(Gene_list_file, 'r')
    wf = open(output_file, 'w', newline='')
    hasANN = 0

    try:
        ref_reader = reff.readlines()
        gl_reader = csv.reader(gf)
        #writer = csv.writer(wf)

        read_en = False
        for line in ref_reader:
            row = line.split('\t')
            row[len(row) - 1] = (row[len(row) - 1].split('\n'))[0]
            #row[len(row)-1].strip('\n')
            if read_en:

                found_gene = False
                add_info = []
                gf.seek(0)
                for row2 in gl_reader:
                    if row[14 + hasANN] == row2[0]:
                        add_info.append(row2[3])
                        found_gene = True

                if not found_gene:
                    add_info.append("novel")

                wf.writelines('\t'.join(row + add_info))
                wf.write('\n')
                #writer.writerow(row + add_info)
            elif row[0] == "#CHROM":
                read_en = True
                if row[12] == 'ANN':
                    hasANN = 1
                # iter_row = iter(reader)
                add_header = ["gene_type"]
                #print(row+add_header)
                wf.writelines('\t'.join(row + add_header))
                wf.write('\n')
                #writer.writerow(row + add_header)
                #print("Found #CHROM")
            else:
                wf.writelines('\t'.join(row))
                wf.write('\n')
    finally:
        reff.close()
        gf.close()
        wf.close()