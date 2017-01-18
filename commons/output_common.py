from config.settings import BASE_DIR


class Output:
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


def get_dp(info, g):
    start = info.find('DP=')
    if start != -1:
        start += 3
        end = info.find(';', start)
    else:
        start = g.find(':') + 1
        end = g.find(':', start)
    return int(info[start:end])


def get_output_list(output_name):
    output_list = []
    read_en = False
    file_path = BASE_DIR + '/output/' + output_name + '.vcf'
    for row in list(open(file_path, "r")):
        words = row.strip().split()
        if read_en:
            output = Output(chrom=words[CHROM],
                            pos=words[POS],
                            ref=words[REF],
                            alt=words[ALT],
                            dp=get_dp(words[INFO], words[G]),
                            )
            output_list.append(output)
        if words[CHROM] == "#CHROM":
            read_en = True

    return output_list
