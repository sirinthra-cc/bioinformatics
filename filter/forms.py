from django import forms


class FilterForm(forms.Form):
    input = forms.CharField(label="Input file")
    filter_by_exac = forms.BooleanField(label='Filter by ExAC', required=False)
    filter_by_thwes = forms.BooleanField(label='Filter by THWES153', required=False)
    filter_by_revel = forms.BooleanField(label='Filter by Revel', required=False)
    exac_max = forms.IntegerField(label='Max AC', initial=10, required=False)
    thwes_max = forms.IntegerField(label='Max AC', initial=1, required=False)
    revel_min = forms.FloatField(label='Min score', initial=0.05, required=False)
    output_name = forms.CharField(label='Output name', max_length=100)

    def clean_exac_max(self):
        filter_by_exac = self.cleaned_data['filter_by_exac']
        exac_max = self.cleaned_data['exac_max']
        if filter_by_exac and not exac_max:
            raise forms.ValidationError("Require")
        return exac_max

    def clean_thwes_max(self):
        filter_by_thwes = self.cleaned_data['filter_by_thwes']
        thwes_max = self.cleaned_data['thwes_max']
        if filter_by_thwes and not thwes_max:
            raise forms.ValidationError("Require")
        return thwes_max

    def clean_revel_min(self):
        filter_by_revel = self.cleaned_data['filter_by_revel']
        revel_min = self.cleaned_data['revel_min']
        if filter_by_revel and not revel_min:
            raise forms.ValidationError("Require")
        return revel_min
