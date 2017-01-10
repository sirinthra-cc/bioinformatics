from django import forms


class HiPhiveForm(forms.Form):
    input = forms.CharField(label="Input file")
    hpo = forms.CharField(label='HPO IDs', widget=forms.Textarea)
    output_name = forms.CharField(label='Output name', max_length=100)


class HPOSearchForm(forms.Form):
    search_string = forms.CharField(label="Symptom")
