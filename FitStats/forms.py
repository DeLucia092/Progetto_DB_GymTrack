from django import forms
from .models import Integratore

class IntegratoreForm(forms.ModelForm):
    class Meta:
        model = Integratore
        fields = ['nome_integratore', 'descrizione', 'dosaggio']