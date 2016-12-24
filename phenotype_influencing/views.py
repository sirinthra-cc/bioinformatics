import os

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import PhenotypeForm
import subprocess
from config.settings import BASE_DIR


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
compile_list = ['java','-Xms2g','-Xmx4g','-jar',
                BASE_DIR+'\\tools\\exomiser-cli-7.2.1\\exomiser-cli-7.2.1.jar',
                '--prioritiser=hiphive','-I','AD','-F','1', '--full-analysis','true','-f','VCF',
                '--output-pass-variants-only','true','--hpo-ids']


def index(request):
    if request.method == 'POST':
        form = PhenotypeForm(request.POST)
        if form.is_valid():
            input_file = form.cleaned_data['input']
            hpo = form.cleaned_data['hpo']
            output_name = form.cleaned_data['output_name']
            compile_list.append(hpo)
            compile_list.append('-v')
            compile_list.append(input_file)
            compile_list.append('-o')
            compile_list.append(BASE_DIR+'\\output\\'+output_name)
            print(compile_list)
            # subprocess.call(compile_list)
            return HttpResponseRedirect('/phenotype/')
        else:
            print("invalid")
    else:
        form = PhenotypeForm()
    return render(request, 'phenotype/index.html', {'form': form})
