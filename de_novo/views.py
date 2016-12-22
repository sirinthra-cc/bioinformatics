from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import DeNovoForm
from de_novo import de_novo


ExAC = "D:/databases/ExAC.r0.3.1.sites.vep.csv"
THWES154 = "D:/200_exomes/All_vcf_1607KHF-0023/154THWES_Ginger/all154.csv"
THWES153 = "D:/200_exomes/All_vcf_1607KHF-0023/153THWES/variant.153.csv"


def index(request):
    if request.method == 'POST':
        form = DeNovoForm(request.POST)
        if form.is_valid():
            child = form.cleaned_data['child']
            mother = form.cleaned_data['mother']
            father = form.cleaned_data['father']

            de_novo.de_novo([child,], mother_file=mother, father_file=father, exac_file=ExAC, exac_ac=10,
                            thwes_file=THWES153, thwes_ac=1)
            return HttpResponseRedirect('/de-novo/')
        else:
            print("invalid")
    else:
        form = DeNovoForm()
    return render(request, 'de_novo/index.html', {'form': form})


