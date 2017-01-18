from django import forms


class FilterForm(forms.Form):
    input = forms.CharField(label="Input file")
    filter_by_exac = forms.BooleanField(label='Filter by ExAC', required=False)
    filter_by_thwes = forms.BooleanField(label='Filter by THWES153', required=False)
    filter_by_revel = forms.BooleanField(label='Filter by Revel', required=False)
    output_name = forms.CharField(label='Output name', max_length=100)
