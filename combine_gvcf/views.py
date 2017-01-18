from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
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
            return HttpResponseRedirect('/combine-gvcf')
        else:
            print("invalid")
    else:
        form = CombineGvcfForm()
    return render(request, 'combine_gvcf/index.html', {'form': form})
