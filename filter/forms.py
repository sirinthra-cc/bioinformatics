from django import forms


class FilterForm(forms.Form):
    input = forms.CharField(label="Input file")
    output_name = forms.CharField(label='Output name', max_length=100)