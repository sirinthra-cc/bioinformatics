from config.settings import BASE_DIR


class Output:
    column_list = []

    def __init__(self, column_list):
        self.column_list = column_list


CHROM = 0


def get_output_list(output_name):
    output_list = []
    read_en = False
    file_path = BASE_DIR + '/output/' + output_name + '.vcf'
    count = 0
    for row in list(open(file_path, "r")):
        words = row.strip().split()
        if count == 500:
            break
        if read_en:
            output = Output(column_list=words)
            output_list.append(output)
            count += 1
        # if read_en == False:
        if words[CHROM] == "CHROM":
            read_en = True
            output = Output(column_list=words)
            output_list.append(output)
    print(output_list[0].column_list)
    return output_list
