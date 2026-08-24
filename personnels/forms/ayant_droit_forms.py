from django import forms
from ..models.ayant_droit import AyantDroit


class AyantDroitForm(forms.ModelForm):
    class Meta:
        model = AyantDroit
        fields = [
            'employe',
            'type',
            'nom',
            'prenoms',
            'date_naissance',
            'lien_parente',
            'photo',
        ]
        widgets = {
            'employe': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenoms': forms.TextInput(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'lien_parente': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
