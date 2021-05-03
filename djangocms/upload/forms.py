from django import forms
from django.forms import ModelForm


class ElasticForm(forms.Form):

    roles = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Roles")
    titulo = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Titulos")
    descripcion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Descripcion")

    class Meta:
        fields = ['roles', 'titulo', 'descripcion']
