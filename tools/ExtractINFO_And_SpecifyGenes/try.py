from function import *
from extract import *

ref_file = "/Users/pitchayut/Documents/Workspace/Individual Study/EntrezID_FromGenesList/data/test1.vcf"
ref_file_out = "/Users/pitchayut/Documents/Workspace/Individual Study/EntrezID_FromGenesList/output/In_Test22.vcf"
gl_file = "/Users/pitchayut/Documents/Workspace/Individual Study/EntrezID_FromGenesList/data/Gene_List.csv"
output_file = "/Users/pitchayut/Documents/Workspace/Individual Study/EntrezID_FromGenesList/output/Test22.vcf"

#getEntrez(ref_file,gl_file,output_file)

extract_and_write2(ref_file,ref_file_out)
specify_gene(ref_file_out,gl_file,output_file)