from django import forms


class DeNovoForm(forms.Form):
    child = forms.CharField(label="Child file")
    mother = forms.CharField(label="Mother file")
    father = forms.CharField(label="Father file")
    output_name = forms.CharField(label='Output name', max_length=100)
