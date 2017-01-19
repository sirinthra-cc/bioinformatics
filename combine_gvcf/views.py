from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from commons.output_combine_gvcf import get_output_list
from .forms import CombineGvcfForm

from .combined_gvcf import combined_gvcf


def index(request):
    if request.method == 'POST':
        form = CombineGvcfForm(request.POST)
        if form.is_valid():
            input1 = form.cleaned_data['input1']
            input2 = form.cleaned_data['input2']
            output_name = form.cleaned_data['output_name']

            combined_gvcf([input1, input2], output_name)
            return HttpResponseRedirect('/combine-gvcf/output/'+output_name)
        else:
            print("invalid")
    else:
        form = CombineGvcfForm()
    return render(request, 'combine_gvcf/index.html', {'form': form})


def output(request, output_name):
    output_list = get_output_list(output_name)
    return render(request, 'combine_gvcf/output.html', {'output_list': output_list})
