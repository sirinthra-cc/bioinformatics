from django import forms


class ExomeWalkerForm(forms.Form):
    input = forms.CharField(label="Input file")
    entrez = forms.CharField(label='Entrez ID', widget=forms.Textarea)
    output_name = forms.CharField(label='Output name', max_length=100)