from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import CombineGvcfForm
from combine_gvcf import combine_gvcf


# ExAC = "D:/databases/ExAC.r0.3.1.sites.vep.csv"
# THWES154 = "D:/200_exomes/All_vcf_1607KHF-0023/154THWES_Ginger/all154.csv"
# THWES153 = "D:/200_exomes/All_vcf_1607KHF-0023/153THWES/variant.153.csv"


def index(request):
    if request.method == 'POST':
        form = CombineGvcfForm(request.POST)
        if form.is_valid():
            input1 = form.cleaned_data['input 1']
            input2 = form.cleaned_data['input 2']

            combine_gvcf.combine_gvcf([input1,input2])
            return HttpResponseRedirect('/combine-gvcf/')
        else:
            print("invalid")
    else:
        form = CombineGvcfForm()
    return render(request, 'combine_gvcf/index.html', {'form': form})
