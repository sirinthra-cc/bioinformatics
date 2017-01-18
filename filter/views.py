import os

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from multiprocessing import Process

from commons.output_exomiser import get_output_list
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
            filter_by_thwes = form.cleaned_data['filter_by_thwes']
            filter_by_revel = form.cleaned_data['filter_by_revel']
            output_name = form.cleaned_data['output_name']
            filtration(input_file, filter_by_revel, filter_by_exac, filter_by_thwes, output_name)
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
