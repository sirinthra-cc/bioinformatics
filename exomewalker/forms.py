from django import forms


class ExomeWalkerForm(forms.Form):
    input = forms.CharField(label="Input file")
    entrez = forms.CharField(label='Entrez ID', widget=forms.Textarea)
    targets = forms.CharField(label='Target List', widget=forms.Textarea)
    candidates = forms.CharField(label='Candidate List', widget=forms.Textarea)
    output_name = forms.CharField(label='Output name', max_length=100)

    # for ped


class EntrezSearchForm(forms.Form):
    search_string = forms.CharField(label="Gene Symbol")
