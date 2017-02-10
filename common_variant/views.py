from django.forms import formset_factory
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from commons.output_common_variant import get_output_list
from .forms import CombineGvcfForm, InputForm

from .common_variant import find_common_variant


def index(request):
    InputFormSet = formset_factory(InputForm, extra=2)
    if request.method == 'POST':
        form = CombineGvcfForm(request.POST)
        formset = InputFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            input_list = []
            for input_form in formset:
                input_list.append(input_form.cleaned_data['input'])
            output_name = form.cleaned_data['output_name']
            print(input_list)
            find_common_variant(input_list, output_name)
            return HttpResponseRedirect('/common-variant/output/'+output_name)
        else:
            print("invalid")
    else:
        form = CombineGvcfForm()
        formset = InputFormSet()
    return render(request, 'common_variant/index.html', {'form': form, 'formset': formset})


def output(request, output_name):
    output_list = get_output_list(output_name)
    return render(request, 'common_variant/output.html', {'output_list': output_list})
