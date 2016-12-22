from django import forms


class CombineGvcfForm(forms.Form):
    input = forms.CharField(label="Input files")
    output_name = forms.CharField(label='Output name', max_length=100)
