import os
from tools.ExtractINFO_And_SpecifyGenes.export import export_specify_gene


class ExomiserOutput:
    chrom = None
    pos = None
    ref = None
    alt = None
    dp = None

    def __init__(self, chrom, pos, ref, alt, dp):
        self.chrom = chrom
        self.pos = pos
        self.ref = ref
        self.alt = alt
        self.dp = dp


CHROM = 0; POS = 1; ID = 2; REF = 3; ALT = 4; QUAL = 5; FILTER = 6; INFO = 7; FORMAT = 8; G = 9


def get_output_list(output_name):
    output_list = []
    read_en = False
    file_path = 'output/' + output_name + '.vcf'
    if not os.path.exists(file_path):
        export_specify_gene(output_name)
    for row in list(open(file_path, "r")):
        words = row.strip().split()
        if read_en:
            hiphive_output = ExomiserOutput(chrom=words[CHROM],
                                            pos=words[POS],
                                            ref=words[REF],
                                            alt=words[ALT],
                                            dp=words[DP],
                                            )
            output_list.append(hiphive_output)
        if words[CHROM] == "#CHROM":
            DP = words.index("DP", 9)
            read_en = True

    return output_list
