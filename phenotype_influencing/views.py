from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import PhenotypeForm


def index(request):
    if request.method == 'POST':
        form = PhenotypeForm(request.POST)
        if form.is_valid():
            child = form.cleaned_data['child']
            mother = form.cleaned_data['mother']
            father = form.cleaned_data['father']

            return HttpResponseRedirect('/phenotype-influencing/')
        else:
            print("invalid")
    else:
        form = PhenotypeForm()
    return render(request, 'phenotype/index.html', {'form': form})
