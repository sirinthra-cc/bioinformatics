# Generate .ped file from data
# input: datas -  list of data need to make .ped file, outname = name of output file
# each member of list must contain the following order: [sample ID, family ID, father ID, mother ID, sex, phenotype]
                                                        # where
                                                        # sample ID = ID that appears in .vcf file
                                                        # family ID = indicate that which family do that user belongs to (must be the same if they're in the same family)
                                                        # father ID = ID of father of that user (0 if that ID doesn't have father)
                                                        # mother ID = ID of mother of that user (0 if that ID doesn't have mother)
                                                        # Note: ID MUST NOT CONTAIN SPACEBAR OR TAB
                                                        # sex = gender of that ID (male, female, unknown)
                                                        # phenotype = indicate that if that users affected from disease or not (affected, unaffected, unknown)
                                                        # For example: data = [['g227', 'fam1', 'g228', 'g229', 'unknown', 'affected'], ['g228', 'fam1', 0, 0, 'male', 'unaffected'], ['g229', 'fam1', 0, 0, 'female', 'unaffected']]
# output: .ped file
import sys
                                                        
def check(list):
    for member in list:
        for element in member:
            if ' ' in member or '\t' in member:
                return true
    return false

def generate_ped(datas, outname):
    if (outname[-4:] != '.ped'):
        outname += '.ped'
    if (check(member)):
        print ("Error: ID contain space you suck")
        sys.exit()
    out = open(outname,'w')
    for member in datas:
        writeData = ''
        writeData += member[1] + '\t' # Family ID
        writeData += member[0] + '\t' # sample ID
        writeData += member[2] + '\t' # father ID
        writeData += member[3] + '\t' # mother ID
        if (member[4].lower() == 'male' or member[4].lower() == 'm'):
            writeData += '1\t'
        else if (member[4].lower() == 'female' or member[4].lower() == 'f'):
            writeData += '2\t'
        else:
            writeData += '0\t'
            
        if (member[5].lower() == 'affected'):
            writeData += '2\n'
        else if (member[5].lower() == 'unaffected'):
            writeData += '1\n'
        else:
            writeData += '0\n'
        
        out.write(writeData)
    out.close()
    ## print ('Success!')
    