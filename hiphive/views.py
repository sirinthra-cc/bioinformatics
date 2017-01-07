from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import HiPhiveForm, HPOSearchForm
import subprocess
from config.settings import BASE_DIR
from .restruct_HP import hp_id_search


CHROM = 0; POS = 1; ID = 2; REF = 3; ALT = 4; QUAL = 5; FILTER = 6; INFO = 7; FORMAT = 8; G = 9
compile_list = ['java', '-Xms2g', '-Xmx4g', '-jar', BASE_DIR+'\\tools\\exomiser-cli-7.2.1\\exomiser-cli-7.2.1.jar',
                '--prioritiser=hiphive', '-I', 'AD', '-F', '1',  '--full-analysis', 'true', '-f', 'VCF',
                '--output-pass-variants-only', 'true', '--hpo-ids']


def index(request):
    hiphive_form = None
    search_form = None
    search_results = []
    if request.method == 'POST':
        print("POST jaaaa"*50)
        if 'hiphive' in request.POST:
            hiphive_form = HiPhiveForm(request.POST, prefix='hiphive')
            search_form = HPOSearchForm(prefix='search')
            print("hiphive")
            if hiphive_form.is_valid():
                print("hiphive is valid")
                input_file = hiphive_form.cleaned_data['input']
                hpo = hiphive_form.cleaned_data['hpo']
                output_name = hiphive_form.cleaned_data['output_name']
                compile_list.append(hpo)
                compile_list.append('-v')
                compile_list.append(input_file)
                compile_list.append('-o')
                compile_list.append(BASE_DIR + '\\output\\' + output_name)
                subprocess.call(compile_list)
                return HttpResponseRedirect('/hiphive/output/' + output_name)
            else:
                print("hiphive form invalid")
        elif 'search' in request.POST:
            hiphive_form = HiPhiveForm(prefix='hiphive')
            search_form = HPOSearchForm(request.POST, prefix='search')
            if search_form.is_valid():
                search_results = hp_id_search(search_form.cleaned_data['search_string'])
                print(search_results)
            else:
                print("search form invalid")

    else:
        hiphive_form = HiPhiveForm(prefix='hiphive')
        search_form = HPOSearchForm(prefix='search')
    return render(request, 'hiphive/index.html', {'form': hiphive_form,
                                                  'search_form': search_form,
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
            hiphive_output = HiPhiveOutput(chrom, pos, ref, alt)
            output_list.append(hiphive_output)
        if words[CHROM] == "#CHROM":
            read_en = True
    return render(request, 'hiphive/output.html', {'output_list': output_list})


class HiPhiveOutput:
    chrom = None
    pos = None
    ref = None
    alt = None

    def __init__(self, chrom, pos, ref, alt):
        self.chrom = chrom
        self.pos = pos
        self.ref = ref
        self.alt = alt
