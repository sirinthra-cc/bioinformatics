from django import forms


class CommonNovelForm(forms.Form):
    output_name = forms.CharField(label='Output name', max_length=100)


class InputForm(forms.Form):
    input = forms.CharField(label="Input file")
