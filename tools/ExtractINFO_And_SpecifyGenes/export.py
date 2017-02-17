from .function import *
from .extract import *
from config.settings import BASE_DIR


gl_file = BASE_DIR + "/tools/ExtractINFO_And_SpecifyGenes/Gene_List.csv"


def export_specify_gene(output_name, target_list, candidate_list):
    input_path = BASE_DIR + "/output/" + output_name + ".vcf"
    extract_info_out = BASE_DIR + "/output/" + output_name + "-extract-info.vcf"
    output_path = BASE_DIR + "/output/" + output_name + "-specify-gene.vcf"

    extract_and_write2(input_path, extract_info_out)
    specify_gene(extract_info_out, target_list, candidate_list, output_path)
