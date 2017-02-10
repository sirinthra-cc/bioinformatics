import json
import os

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from commons.export_csv import get_streaming_response
from commons.output_exomiser import get_output_list
from .forms import ExomeWalkerForm, EntrezSearchForm
import subprocess
from config.settings import BASE_DIR

from .entrez_id import entrez_id_search


CHROM = 0; POS = 1; ID = 2; REF = 3; ALT = 4; QUAL = 5; FILTER = 6; INFO = 7; FORMAT = 8; G = 9

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
compile_list_1 = ['java', '-Xms2g', '-Xmx4g', '-jar', BASE_DIR+'\\tools\\exomiser-cli-7.2.1\\exomiser-cli-7.2.1.jar',
                  '--prioritiser', 'exomewalker', '-v']
compile_list_2 = ['-I', 'AD', '-F', '1', '--full-analysis', 'true', '-f', 'VCF', '--output-pass-variants-only', 'true',
                  '-S']
compile_list_ped = ['-p', 'pedfile.ped']
# --output-pass-variants-only true -p pedfile.ped -v input.vcf -o output.vcf -S ...


def index(request):
    exomewalker_form = None
    search_form = None
    if request.method == 'POST':
        if 'exomewalker' in request.POST:
            exomewalker_form = ExomeWalkerForm(request.POST, prefix="exomewalker")
            search_form = EntrezSearchForm(prefix='search')
            if exomewalker_form.is_valid():
                input_file = exomewalker_form.cleaned_data['input']
                entrez = exomewalker_form.cleaned_data['entrez']
                output_name = exomewalker_form.cleaned_data['output_name']

                targets = exomewalker_form.cleaned_data['targets'].split()
                candidates = exomewalker_form.cleaned_data['candidates'].split()

                compile_list_1.append(input_file)
                compile_list_1.append('-o')
                compile_list_1.append(BASE_DIR+'\\output\\'+output_name)
                compile_list = compile_list_1 + compile_list_2
                compile_list.append(entrez)
                subprocess.call(compile_list)

                request.session['targets'] = targets
                request.session['candidates'] = candidates

                return HttpResponseRedirect('/exomewalker/output/'+output_name)
            else:
                print("exomewalker form invalid")
        elif 'search-search_string' in request.POST:
            exomewalker_form = ExomeWalkerForm(prefix='exomewalker')
            search_form = EntrezSearchForm(request.POST, prefix='search')
            if search_form.is_valid():
                search_results = entrez_id_search(search_form.cleaned_data['search_string'])
                return HttpResponse(json.dumps({'search_results': search_results}))
            else:
                print("search form invalid")
    else:
        search_form = EntrezSearchForm(prefix='search')
        exomewalker_form = ExomeWalkerForm(prefix="exomewalker")
    return render(request, 'exomewalker/index.html', {'form': exomewalker_form,
                                                      'search_form': search_form})


def output(request, output_name):
    targets = request.session['targets']
    candidates = request.session['candidates']
    print(targets, candidates)
    output_list = get_output_list(output_name, targets, candidates)
    return render(request, 'exomewalker/output.html', {'output_list': output_list})


def export(request, output_name):
    output_path = BASE_DIR + '/output/' + output_name + '.vcf'
    return get_streaming_response(output_name, output_path)


    # 201, 213, 258, 265, 266, 401138, 395, 11101, 649, 9256, 152816, 10970, 1261, 26504, 1308, 1277, 1278, 10491, 1406, 1747, 1834, 1910, 10117, 54757, 9917, 56975, 286077, 60681, 10468, 2776, 3263, 387733, 3694, 9622, 3909, 3914, 3918, 4054, 9313, 64386, 4488, 4763, 54959, 64175, 64065, 5479, 5573, 5818, 27289, 79641, 6103, 51156, 5176, 871, 6505, 56796, 10568, 29986, 6522, 8671, 80320, 121340, 6786, 57620, 6899, 55858, 8626, 7286, 23335, 256764, 64175, 27289, 8626
    # HP: 0000705, HP: 0006284, HP: 0006310, HP: 0006325, HP: 0006327, HP: 0006331
