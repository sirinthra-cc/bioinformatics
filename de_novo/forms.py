from django import forms


class DeNovoForm(forms.Form):

    children = forms.FileField(label='Children file')
    output_name = forms.CharField(label='Output name', max_length=100)
