from django import forms
from django.core.exceptions import ValidationError

from ..models import (
    CategorieActe,
    ActeMedical,
    TarifActe,
)


# =========================
# Formulaire Catégorie d'acte
# =========================
class CategorieActeForm(forms.ModelForm):
    class Meta:
        model = CategorieActe
        fields = ['nom', 'description', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la catégorie',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description',
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        qs = CategorieActe.objects.filter(nom__iexact=nom)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Une catégorie avec ce nom existe déjà.")
        return nom


# =========================
# Formulaire Acte médical
# =========================
class ActeMedicalForm(forms.ModelForm):
    class Meta:
        model = ActeMedical
        fields = [
            'code',
            'libelle',
            'categorie',
            'description',
            'necessite_medicament',
            'actif',
        ]
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Code de l'acte",
            }),
            'libelle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Libellé de l'acte",
            }),
            'categorie': forms.Select(attrs={
                'class': 'form-select',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description',
            }),
            'necessite_medicament': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categorie'].queryset = CategorieActe.objects.filter(actif=True)

    def clean_code(self):
        code = self.cleaned_data.get('code', '').strip()
        qs = ActeMedical.objects.filter(code__iexact=code)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Un acte avec ce code existe déjà.")
        return code

    def clean_libelle(self):
        libelle = self.cleaned_data.get('libelle', '').strip()
        qs = ActeMedical.objects.filter(libelle__iexact=libelle)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Un acte avec ce libellé existe déjà.")
        return libelle


# =========================
# Formulaire Tarif d'acte
# =========================
class TarifActeForm(forms.ModelForm):
    class Meta:
        model = TarifActe
        fields = [
            'acte',
            'etablissement',
            'montant',
            'date_debut',
            'date_fin',
            'actif',
        ]
        widgets = {
            'acte': forms.Select(attrs={
                'class': 'form-select',
            }),
            'etablissement': forms.Select(attrs={
                'class': 'form-select',
            }),
            'montant': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Montant en GNF',
            }),
            'date_debut': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'date_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['acte'].queryset = ActeMedical.objects.filter(actif=True)
        self.fields['date_fin'].required = False

    def clean_montant(self):
        montant = self.cleaned_data.get('montant')
        if montant is not None and montant < 0:
            raise ValidationError("Le montant ne peut pas être négatif.")
        return montant

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        acte = cleaned_data.get('acte')
        etablissement = cleaned_data.get('etablissement')

        if date_debut and date_fin and date_fin < date_debut:
            raise ValidationError("La date de fin ne peut pas être antérieure à la date de début.")

        if acte and etablissement and date_debut:
            qs = TarifActe.objects.filter(
                acte=acte,
                etablissement=etablissement,
                actif=True,
            )
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            for tarif in qs:
                autre_fin = tarif.date_fin or date_debut
                if date_debut <= autre_fin and (not date_fin or date_fin >= tarif.date_debut):
                    raise ValidationError(
                        "Un tarif actif existe déjà pour cet acte sur cette période, "
                        "pour cet établissement."
                    )

        return cleaned_data