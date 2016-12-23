from django import forms


class CombineGvcfForm(forms.Form):
    input1 = forms.CharField(label="Input file 1")
    input2 = forms.CharField(label="Input file 2")
    output_name = forms.CharField(label='Output name', max_length=100)
