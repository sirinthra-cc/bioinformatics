from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import DeNovoForm
from de_novo import de_novo


def index(request):
    if request.method == 'POST':
        form = DeNovoForm(request.POST)
        if form.is_valid():
            child = form.cleaned_data['child']
            mother = form.cleaned_data['mother']
            father = form.cleaned_data['father']
            output_name = form.cleaned_data['output_name']
            de_novo.de_novo([child, ], mother_file=mother, father_file=father, output_name=output_name)
            return HttpResponseRedirect('/de-novo/')
        else:
            print("invalid")
    else:
        form = DeNovoForm()
    return render(request, 'de_novo/index.html', {'form': form})


