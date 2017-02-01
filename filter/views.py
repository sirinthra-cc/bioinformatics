import os

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from multiprocessing import Process

from commons.output_common import get_output_list
from .filtration import filtration
from .forms import FilterForm
import subprocess
from config.settings import BASE_DIR


CHROM = 0; POS = 1; ID = 2; REF = 3; ALT = 4; QUAL = 5; FILTER = 6; INFO = 7; FORMAT = 8; G = 9

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def index(request):
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            input_file = form.cleaned_data['input']

            filter_by_exac = form.cleaned_data['filter_by_exac']
            exac_max = form.cleaned_data['exac_max'] if filter_by_exac else None

            filter_by_thwes = form.cleaned_data['filter_by_thwes']
            thwes_max = form.cleaned_data['thwes_max'] if filter_by_thwes else None

            filter_by_revel = form.cleaned_data['filter_by_revel']
            revel_min = form.cleaned_data['revel_min'] if filter_by_revel else None

            output_name = form.cleaned_data['output_name']

            filtration(input_file, output_name, revel_min=revel_min, exac_max=exac_max, thwe_max=thwes_max)
            # if __name__ == '__main__':
            # p = Process(target=filtration,
            #             args=(input_file, filter_by_revel, filter_by_exac, filter_by_thwes, output_name))
            # p.start()
            # p.join()
            return HttpResponseRedirect('/filter/output/'+output_name)
        else:
            print("filter form invalid")
    else:
        form = FilterForm()
    return render(request, 'filter/index.html', {'form': form})


def output(request, output_name):
    output_list = get_output_list(output_name)
    return render(request, 'filter/output.html', {'output_list': output_list})
