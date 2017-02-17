import os
from tools.ExtractINFO_And_SpecifyGenes.export import export_specify_gene


class ExomiserOutput:
    chrom = None
    pos = None
    ref = None
    alt = None
    ann = None
    dp = None
    gene_name = None
    gene_type = None
    gene_combined_score = None
    gene_pheno_score = None
    gene_variant_score = None
    variant_score = None

    def __init__(self, chrom, pos, ref, alt, ann, dp, gene_name, gene_type, gene_combined_score, gene_pheno_score,
                 gene_variant_score, variant_score):
        self.chrom = chrom
        self.pos = pos
        self.ref = ref
        self.alt = alt
        self.ann = ann
        self.dp = dp
        self.gene_name = gene_name
        self.gene_type = gene_type
        self.gene_combined_score = gene_combined_score
        self.gene_pheno_score = gene_pheno_score
        self.gene_variant_score = gene_variant_score
        self.variant_score = variant_score


CHROM = 0; POS = 1; ID = 2; REF = 3; ALT = 4; QUAL = 5; FILTER = 6; INFO = 7; FORMAT = 8; G = 9
ANN = None; DP = None; EXOMISER_GENE = None; GENE_TYPE = None
EXOMISER_GENE_COMBINED_SCORE = None
EXOMISER_GENE_PHENO_SCORE = None
EXOMISER_GENE_VARIANT_SCORE = None
EXOMISER_VARIANT_SCORE = None


def get_output_list(output_name, targets, candidates):
    output_list = []
    read_en = False
    file_path = 'output/' + output_name + '-specify-gene.vcf'
    if not os.path.exists(file_path):
        export_specify_gene(output_name, targets, candidates)
    for row in list(open(file_path, "r")):
        words = row.strip().split()
        if read_en:
            if ANN != -1:
                ann = words[ANN]
            else:
                ann = None
            hiphive_output = ExomiserOutput(chrom=words[CHROM],
                                            pos=words[POS],
                                            ref=words[REF],
                                            alt=words[ALT],
                                            ann=ann,
                                            dp=words[DP],
                                            gene_name=words[EXOMISER_GENE],
                                            gene_type=words[GENE_TYPE],
                                            gene_combined_score=words[EXOMISER_GENE_COMBINED_SCORE],
                                            gene_pheno_score=words[EXOMISER_GENE_PHENO_SCORE],
                                            gene_variant_score=words[EXOMISER_GENE_VARIANT_SCORE],
                                            variant_score=words[EXOMISER_VARIANT_SCORE]
                                            )
            output_list.append(hiphive_output)
        if words[CHROM] == "#CHROM":
            try:
                ANN = words.index("ANN", 9)
            except:
                ANN = -1
            DP = words.index("DP", 9)
            EXOMISER_GENE = words.index("EXOMISER_GENE", 9)
            GENE_TYPE = words.index("gene_type", 9)
            EXOMISER_GENE_COMBINED_SCORE = words.index("EXOMISER_GENE_COMBINED_SCORE", 9)
            EXOMISER_GENE_PHENO_SCORE = words.index("EXOMISER_GENE_PHENO_SCORE", 9)
            EXOMISER_GENE_VARIANT_SCORE = words.index("EXOMISER_GENE_VARIANT_SCORE", 9)
            EXOMISER_VARIANT_SCORE = words.index("EXOMISER_VARIANT_SCORE", 9)
            read_en = True

    return output_list
