from django import forms


class PhenotypeForm(forms.Form):
    input = forms.CharField(label="Input file")
    # output_path = forms.CharField(label="Output path")
    hpo = forms.CharField(label='HPO IDs', widget=forms.Textarea)
    output_name = forms.CharField(label='Output name', max_length=100)
