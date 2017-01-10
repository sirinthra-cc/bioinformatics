import json
import os

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from commons.output import get_output_list
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
            output_name = form.cleaned_data['output_name']
            # subprocess.call(compile_list)
            # return HttpResponseRedirect('/exomewalker/output/'+output_name)
        else:
            print("exomewalker form invalid")
    else:
        form = FilterForm()
    return render(request, 'filter/index.html', {'form': form})


# def output(request, output_name):
    # output_list = get_output_list(output_name)
    # return render(request, 'exomewalker/output.html', {'output_list': output_list})
