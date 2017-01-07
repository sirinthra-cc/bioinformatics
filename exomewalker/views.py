import os

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import ExomeWalkerForm, EntrezSearchForm
import subprocess
from config.settings import BASE_DIR


CHROM = 0; POS = 1; ID = 2; REF = 3; ALT = 4; QUAL = 5; FILTER = 6; INFO = 7; FORMAT = 8; G = 9

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
compile_list_1 = ['java', '-Xms2g', '-Xmx4g', '-jar', BASE_DIR+'\\tools\\exomiser-cli-7.2.1\\exomiser-cli-7.2.1.jar',
                  '--prioritiser', 'exomewalker', '-v']
compile_list_2 = ['-I', 'AD', '-F', '1', '--full-analysis', 'true', '-f', 'VCF', '--output-pass-variants-only', 'true',
                  '-S']


def index(request):
    exomewalker_form = None
    search_form = None
    search_results = []
    if request.method == 'POST':
        if 'exomewalker' in request.POST:
            exomewalker_form = ExomeWalkerForm(request.POST, prefix="exomewalker")
            search_form = EntrezSearchForm(prefix='search')
            if exomewalker_form.is_valid():
                input_file = exomewalker_form.cleaned_data['input']
                entrez = exomewalker_form.cleaned_data['entrez']
                output_name = exomewalker_form.cleaned_data['output_name']
                compile_list_1.append(input_file)
                compile_list_1.append('-o')
                compile_list_1.append(BASE_DIR+'\\output\\'+output_name)
                compile_list = compile_list_1 + compile_list_2
                compile_list.append(entrez)
                subprocess.call(compile_list)
                return HttpResponseRedirect('/exomewalker/output/'+output_name)
            else:
                print("exomewalker form invalid")
        elif 'search' in request.POST:
            exomewalker_form = ExomeWalkerForm(request.POST, prefix='exomewalker')
            search_form = EntrezSearchForm(request.POST, prefix='search')
            if search_form.is_valid():
                # search_results = hp_id_search(search_form.cleaned_data['search_string'])
                search_results = ['TEST']
            else:
                print("search form invalid")
    else:
        search_form = EntrezSearchForm(prefix='search')
        exomewalker_form = ExomeWalkerForm(prefix="exomewalker")
    return render(request, 'exomewalker/index.html', {'form': exomewalker_form, 'search_form': search_form,
                                                      'search_results': search_results})


def output(request, output_name):
    output_list = []
    read_en = False
    for row in list(open('output/'+output_name+'.vcf', "r")):
        words = row.strip().split()
        if read_en:
            chrom = words[CHROM]
            pos = words[POS]
            ref = words[REF]
            alt = words[ALT]
            exomewalker_output = ExomeWalkerOutput(chrom, pos, ref, alt)
            output_list.append(exomewalker_output)
        if words[CHROM] == "#CHROM":
            read_en = True
    return render(request, 'exomewalker/output.html', {'output_list': output_list})


class ExomeWalkerOutput:
    chrom = None
    pos = None
    ref = None
    alt = None

    def __init__(self, chrom, pos, ref, alt):
        self.chrom = chrom
        self.pos = pos
        self.ref = ref
        self.alt = alt


    # 201, 213, 258, 265, 266, 401138, 395, 11101, 649, 9256, 152816, 10970, 1261, 26504, 1308, 1277, 1278, 10491, 1406, 1747, 1834, 1910, 10117, 54757, 9917, 56975, 286077, 60681, 10468, 2776, 3263, 387733, 3694, 9622, 3909, 3914, 3918, 4054, 9313, 64386, 4488, 4763, 54959, 64175, 64065, 5479, 5573, 5818, 27289, 79641, 6103, 51156, 5176, 871, 6505, 56796, 10568, 29986, 6522, 8671, 80320, 121340, 6786, 57620, 6899, 55858, 8626, 7286, 23335, 256764, 64175, 27289, 8626
    # HP: 0000705, HP: 0006284, HP: 0006310, HP: 0006325, HP: 0006327, HP: 0006331
