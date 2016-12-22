from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import CombineGvcfForm
# from combine_gvcf import combine_gvcf


# ExAC = "D:/databases/ExAC.r0.3.1.sites.vep.csv"
# THWES154 = "D:/200_exomes/All_vcf_1607KHF-0023/154THWES_Ginger/all154.csv"
# THWES153 = "D:/200_exomes/All_vcf_1607KHF-0023/153THWES/variant.153.csv"


def index(request):
    if request.method == 'POST':
        form = CombineGvcfForm(request.POST)
        if form.is_valid():
            input = form.cleaned_data['input']

            # de_novo.de_novo([input,], mother_file=mother, father_file=father, exac_file=ExAC, exac_ac=10,
            #                 thwes_file=THWES153, thwes_ac=1)
            return HttpResponseRedirect('/combine-gvcf/')
        else:
            print("invalid")
    else:
        form = CombineGvcfForm()
    return render(request, 'combine_gvcf/index.html', {'form': form})
