from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import CombineGvcfForm


def index(request):
    if request.method == 'POST':
        form = CombineGvcfForm(request.POST)
        if form.is_valid():
            input1 = form.cleaned_data['input1']
            input2 = form.cleaned_data['input2']

            # combined_gvcf.combine_gvcf(input1, input2)
            return HttpResponseRedirect('/combine-gvcf/')
        else:
            print("invalid")
    else:
        form = CombineGvcfForm()
    return render(request, 'combine_gvcf/index.html', {'form': form})
