import os


# file list
# flist = ["../200_exomes/G2227-PJ.g.vcf", "../200_exomes/G2228-M.g.vcf"]


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

db = "null"
Diff = set()
cacheGene = set()

# Find intersected differences
isFirstFile = True
print("Finding common variant...")

for file in flist:
    with open(file) as f:
        for line in f:
            if line[:11] == "#reference" and db == "null": db = line[11:]
            elif line[:11] == "#reference" and db != "null" and db != line[11:]:
                print("Warning, Unmatch reference detected. Found: " + line[11:] + ", Expected: " + db)
            elif line[:3] == "chr": # chromosome data
                s = line.split("\t")
                if s[4] != '<NON_REF>':
                    if isFirstFile:
                        Diff.add((s[0][3:], s[1]))
                    else:
                        cacheGene.add((s[0][3:], s[1]))
    if isFirstFile:
        isFirstFile = False
    else:
        Diff = Diff.intersection(cacheGene)
        cacheGene = set()

print("sorting data")
Diff = list(Diff)
Diff = sorted(Diff, key=byChromosome)
# debug
# print(Diff)
# end of debug

print("Generating output")
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
                    Diff[iterate] = Diff[iterate][:(3+fileNumber)] + [s[3] + "/" + s[4][:-10]] + Diff[iterate][(3+fileNumber):]
                    try:
                        Diff[iterate] = Diff[iterate][:(3+fileNumber * 2)] + [data[getFormat.index("GT")]] + Diff[iterate][(3+fileNumber * 2):]
                    except ValueError:
                        Diff[iterate] = Diff[iterate][:(3+fileNumber * 2)] + ["NULL"] + Diff[iterate][(3+fileNumber * 2):]

                    try:
                        Diff[iterate] = Diff[iterate][:(3+fileNumber * 3)] + [int(data[getFormat.index("DP")])] + Diff[iterate][(3+fileNumber * 3):]
                    except ValueError:
                        Diff[iterate] = Diff[iterate][:(3+fileNumber * 3)] + ["NULL"] + Diff[iterate][(3+fileNumber * 3):]

                    try:
                        Diff[iterate] = Diff[iterate][:(3+fileNumber * 4)] + [data[getFormat.index("AD")]] + Diff[iterate][(3+fileNumber * 4):]
                    except ValueError:
                        Diff[iterate] = Diff[iterate][:(3+fileNumber * 4)] + ["NULL"] + Diff[iterate][(3+fileNumber * 4):]

                    iterate += iterate
                    if iterate >= len(Diff):
                        iterate = 0
    iterate = 0
    fileNumber += fileNumber

print("writing to file")
out = open('combined.vcf', 'w')

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
    fileNumber += fileNumber

out.write('\t'.join(outdata) + '\n')

for line in Diff:
    outdata = 'chr'
    for data in line:
        outdata += str(data) + '\t'
    outdata = outdata[:-1] + '\n'
    out.write(outdata)
out.close()
