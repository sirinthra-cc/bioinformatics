from django.forms import formset_factory
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import CommonNovelForm, InputForm
from common_novel import common_novel


def index(request):
    InputFormSet = formset_factory(InputForm, extra=2)
    if request.method == 'POST':
        form = CommonNovelForm(request.POST)
        formset = InputFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            input_list = []
            for input_form in formset:
                input_list.append(input_form.cleaned_data['input'])
            output_name = form.cleaned_data['output_name']
            common_novel.common_novel(input_list, output_name=output_name)
            return HttpResponseRedirect('/common-novel/')
        else:
            print("invalid")
    else:
        form = CommonNovelForm()
        formset = InputFormSet()
    return render(request, 'common_novel/index.html', {'form': form, 'formset': formset})


