from .function import *
from .extract import *
from config.settings import BASE_DIR


# ref_file = "/Users/pitchayut/Documents/Workspace/Individual Study/EntrezID_FromGenesList/data/G4974_Exomised.vcf"
# ref_file_out = "/Users/pitchayut/Documents/Workspace/Individual Study/EntrezID_FromGenesList/output/In_Test35.vcf"
gl_file = BASE_DIR + "/tools/ExtractINFO_And_SpecifyGenes/Gene_List.csv"
# output_file = "/Users/pitchayut/Documents/Workspace/Individual Study/EntrezID_FromGenesList/output/Test35.vcf"

# getEntrez(ref_file,gl_file,output_file)


def export_specify_gene(output_name):
    input_path = BASE_DIR + "/output/" + output_name + ".vcf"
    extract_info_out = BASE_DIR + "/output/" + output_name + "-extract-info.vcf"
    output_path = BASE_DIR + "/output/" + output_name + "-specify-gene.vcf"

    extract_and_write2(input_path, extract_info_out)
    specify_gene(extract_info_out, gl_file, output_path)
