from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import DeNovoForm


def index(request):
    if request.method == 'POST':
        form = DeNovoForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')
    else:
        form = DeNovoForm()
    return render(request, 'de_novo/index.html', {'form': form})

