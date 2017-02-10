# find all possible ID from vcf file
# input: vcf - a vcf file
# output: list of sample ID that appears in vcf file


def find_possible_id(vcf):
    with open(vcf) as f:
        for line in f:
            if line[:6] == '#CHROM':
                data = line.split('\t')
                ret = data[9:]
                ret[len(ret)-1] = ret[len(ret)-1][:-1]  # remove \n from the last IDs
                return ret
