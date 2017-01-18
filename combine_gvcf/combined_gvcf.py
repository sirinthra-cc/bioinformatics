import os


# sort tuple by chromosome
from config.settings import BASE_DIR


def byChromosome(tup):
    if tup[0] == 'X':
        return 23 * 10000000000 + int(tup[1])
    elif tup[0] == 'Y':
        return 24 * 10000000000 + int(tup[1])
    elif tup[0] == 'M':
        return 0 + tup[1]
    elif len(tup[0][3:]) > 2: # A very strange case at the bottom of gcvf file
        return 100 * 10000000000 + int(tup[1])
    else:
        return int(tup[0]) * 10000000000 + int(tup[1])


# combined gvcf function
# flist = list of gvcf file to be combined
# outname = name of output file (default is 'combined.vcf')
def combined_gvcf(flist, outname):
    Diff = set()
    cacheGene = set()
    # Find intersected differences
    fileNumber = 1

    for file in flist:
        with open(file) as f:
            for line in f:
                if line[:3] == "chr": # chromosome data
                    s = line.split("\t")
                    if s[4] != '<NON_REF>':
                        if fileNumber == 1:
                            Diff.add((s[0][3:], s[1]))
                        else:
                            cacheGene.add((s[0][3:], s[1]))
        if fileNumber != 1:
            Diff = Diff.intersection(cacheGene)
            cacheGene = set()
        fileNumber = fileNumber + 1

    ## print("sorting data")

    Diff = list(Diff)
    Diff = sorted(Diff, key=byChromosome)

    ## print("Generating output")

    # Generate list of differences from each file
    #
    # Writing Header

    # generate data in memory(RAM)
    fileNumber = 1
    iterate = 0
    for file in flist:
        with open(file) as f:
            for line in f:
                if line[:3] == "chr":
                    s = line.split('\t')
                    if Diff[iterate][0] == s[0][3:] and Diff[iterate][1] == s[1]:
                        if fileNumber == 1:
                            Diff[iterate] = list(Diff[iterate]) + [s[2]] + [s[3]] # + id and reference
                        getFormat = s[8].split(':')
                        data = s[9].split(':')
                        
                        #GT
                        if (s[4][-9:] == '<NON_REF>'):
                            Diff[iterate] = Diff[iterate][:(3+fileNumber)] + [s[3] + "/" + s[4][:-10]] + Diff[iterate][(3+fileNumber):]
                        else:
                            Diff[iterate] = Diff[iterate][:(3+fileNumber)] + [s[3] + "/" + s[4][:]] + Diff[iterate][(3+fileNumber):]
                        
                        #GT_1
                        try:
                            Diff[iterate] = Diff[iterate][:(3+fileNumber * 2)] + [data[getFormat.index("GT")]] + Diff[iterate][(3+fileNumber * 2):]
                        except ValueError:
                            Diff[iterate] = Diff[iterate][:(3+fileNumber * 2)] + ["NULL"] + Diff[iterate][(3+fileNumber * 2):]
                        
                        #DP
                        start = info.find('DP=')
                        start = start + 3
                        end = info.find(';',start)
                        try:
                            Diff[iterate] = Diff[iterate][:(3+fileNumber * 3)] + [int(info[start:end])] + Diff[iterate][(3+fileNumber * 3):]
                        except ValueError:
                            Diff[iterate] = Diff[iterate][:(3+fileNumber * 3)] + ["NULL"] + Diff[iterate][(3+fileNumber * 3):]
                        #AD
                        try:
                            Diff[iterate] = Diff[iterate][:(3+fileNumber * 4)] + [data[getFormat.index("AD")]] + Diff[iterate][(3+fileNumber * 4):]
                        except ValueError:
                            Diff[iterate] = Diff[iterate][:(3+fileNumber * 4)] + ["NULL"] + Diff[iterate][(3+fileNumber * 4):]
                        
                        iterate = iterate + 1
                        if iterate >= len(Diff):
                            iterate = 0

        iterate = 0
        fileNumber = fileNumber + 1

    ## print("writing to file")
    if outname[-4:] != '.vcf':
        outname = BASE_DIR + '/output/' + outname + '.vcf'
    else:
        outname = BASE_DIR + '/output/' + outname

    out = open(outname, 'w')

    # writing header
    outdata = ["CHROM", "POS", "ID", "REF"]
    fileNumber = 1
    for file in flist:
        with open(file) as f:
            filename = os.path.basename(f.name)
            filename = os.path.splitext(filename)[0]
            outdata.insert(3 + fileNumber,filename+".GT")
            outdata.insert(3 + fileNumber * 2,filename+".GT_1")
            outdata.insert(3 + fileNumber * 3,filename+".DP")
            outdata.insert(3 + fileNumber * 4,filename+".AD")
        fileNumber = fileNumber + 1

    out.write('\t'.join(outdata) + '\n')

    for line in Diff:
        outdata = 'chr'
        for data in line:
            outdata += str(data) + '\t'
        outdata = outdata[:-1] + '\n'
        out.write(outdata)
    out.close()