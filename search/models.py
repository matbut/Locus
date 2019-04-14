from django import forms


class UrlForm(forms.Form):
    duration = forms.CharField(label='Duration of simulated work in seconds', max_length=100)

