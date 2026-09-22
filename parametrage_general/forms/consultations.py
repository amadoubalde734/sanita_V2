from django import forms
from django.core.exceptions import ValidationError

from ..models import (
    TypeConsultation,
    TarifConsultation,
    MotifConsultation,
    Posologie,
    VoieAdministration,
    Dosage,
    Forme,
    ConfigurationEtablissement,
)


class TypeConsultationForm(forms.ModelForm):
    class Meta:
        model = TypeConsultation
        fields = [
            'code',
            'nom',
            'categorie',
            'description',
            'ordre',
            'actif',
        ]
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Code du type de consultation',
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du type de consultation',
            }),
            'categorie': forms.Select(attrs={
                'class': 'form-select',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description',
            }),
            'ordre': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': "Ordre d'affichage",
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_code(self):
        code = self.cleaned_data.get('code', '').strip().upper()
        qs = TypeConsultation.objects.filter(code__iexact=code)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(
                "Un type de consultation avec ce code existe déjà."
            )

        return code

    def clean_nom(self):
        nom = self.cleaned_data.get('nom', '').strip()
        qs = TypeConsultation.objects.filter(nom__iexact=nom)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(
                "Un type de consultation avec ce nom existe déjà."
            )

        return nom

    def clean_ordre(self):
        ordre = self.cleaned_data.get('ordre')

        if ordre is not None and ordre < 0:
            raise ValidationError(
                "L'ordre d'affichage ne peut pas être négatif."
            )

        return ordre


class TarifConsultationForm(forms.ModelForm):
    class Meta:
        model = TarifConsultation
        fields = [
            'type_consultation',
            'etablissement',
            'montant',
            'date_debut',
            'date_fin',
            'actif',
        ]
        widgets = {
            'type_consultation': forms.Select(attrs={
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

        self.fields['type_consultation'].queryset = (
            TypeConsultation.objects.filter(actif=True)
        )

        self.fields['etablissement'].queryset = (
            ConfigurationEtablissement.objects.filter(actif=True)
        )

        self.fields['date_fin'].required = False

    def clean_montant(self):
        montant = self.cleaned_data.get('montant')

        if montant is not None and montant < 0:
            raise ValidationError(
                "Le montant ne peut pas être négatif."
            )

        return montant

    def clean(self):
        cleaned_data = super().clean()

        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        type_consultation = cleaned_data.get('type_consultation')
        etablissement = cleaned_data.get('etablissement')
        actif = cleaned_data.get('actif')

        if date_debut and date_fin and date_fin < date_debut:
            raise ValidationError(
                "La date de fin ne peut pas être antérieure à la date de début."
            )

        if (
            actif
            and type_consultation
            and etablissement
            and date_debut
        ):
            qs = TarifConsultation.objects.filter(
                type_consultation=type_consultation,
                etablissement=etablissement,
                actif=True,
            )

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            for tarif in qs:
                tarif_debut = tarif.date_debut
                tarif_fin = tarif.date_fin

                chevauchement = (
                    date_debut <= (tarif_fin or date_debut)
                    and (
                        not date_fin
                        or not tarif_fin
                        or date_fin >= tarif_debut
                    )
                )

                if chevauchement:
                    raise ValidationError(
                        "Un tarif actif existe déjà pour ce type de consultation "
                        "sur cette période, pour cet établissement."
                    )

        return cleaned_data


class MotifConsultationForm(forms.ModelForm):
    class Meta:
        model = MotifConsultation
        fields = [
            'motif',
            'actif',
        ]
        widgets = {
            'motif': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Motif de consultation',
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_motif(self):
        motif = self.cleaned_data.get('motif', '').strip()

        qs = MotifConsultation.objects.filter(
            motif__iexact=motif
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(
                "Ce motif de consultation existe déjà."
            )

        return motif


class PosologieForm(forms.ModelForm):
    class Meta:
        model = Posologie
        fields = [
            'libelle',
            'actif',
        ]
        widgets = {
            'libelle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Posologie',
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_libelle(self):
        libelle = self.cleaned_data.get('libelle', '').strip()

        qs = Posologie.objects.filter(
            libelle__iexact=libelle
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(
                "Cette posologie existe déjà."
            )

        return libelle


class VoieAdministrationForm(forms.ModelForm):
    class Meta:
        model = VoieAdministration
        fields = [
            'code',
            'nom',
            'description',
            'ordre',
            'actif',
        ]
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Code de la voie d'administration",
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Nom de la voie d'administration",
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description',
            }),
            'ordre': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': "Ordre d'affichage",
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_code(self):
        code = self.cleaned_data.get('code', '').strip().upper()

        qs = VoieAdministration.objects.filter(
            code__iexact=code
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(
                "Une voie d'administration avec ce code existe déjà."
            )

        return code

    def clean_nom(self):
        nom = self.cleaned_data.get('nom', '').strip()

        qs = VoieAdministration.objects.filter(
            nom__iexact=nom
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(
                "Cette voie d'administration existe déjà."
            )

        return nom

    def clean_ordre(self):
        ordre = self.cleaned_data.get('ordre')

        if ordre is not None and ordre < 0:
            raise ValidationError(
                "L'ordre d'affichage ne peut pas être négatif."
            )

        return ordre


class DosageForm(forms.ModelForm):
    class Meta:
        model = Dosage
        fields = [
            'code',
            'nom',
            'description',
            'ordre',
            'actif',
        ]
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Code du dosage',
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dosage',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description',
            }),
            'ordre': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': "Ordre d'affichage",
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_code(self):
        code = self.cleaned_data.get('code', '').strip().upper()

        qs = Dosage.objects.filter(
            code__iexact=code
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(
                "Un dosage avec ce code existe déjà."
            )

        return code

    def clean_nom(self):
        nom = self.cleaned_data.get('nom', '').strip()

        qs = Dosage.objects.filter(
            nom__iexact=nom
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(
                "Ce dosage existe déjà."
            )

        return nom

    def clean_ordre(self):
        ordre = self.cleaned_data.get('ordre')

        if ordre is not None and ordre < 0:
            raise ValidationError(
                "L'ordre d'affichage ne peut pas être négatif."
            )

        return ordre


class FormeForm(forms.ModelForm):
    class Meta:
        model = Forme
        fields = [
            'code',
            'nom',
            'description',
            'ordre',
            'actif',
        ]
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Code de la forme',
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Forme pharmaceutique',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description',
            }),
            'ordre': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': "Ordre d'affichage",
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_code(self):
        code = self.cleaned_data.get('code', '').strip().upper()

        qs = Forme.objects.filter(
            code__iexact=code
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(
                "Une forme avec ce code existe déjà."
            )

        return code

    def clean_nom(self):
        nom = self.cleaned_data.get('nom', '').strip()

        qs = Forme.objects.filter(
            nom__iexact=nom
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(
                "Cette forme pharmaceutique existe déjà."
            )

        return nom

    def clean_ordre(self):
        ordre = self.cleaned_data.get('ordre')

        if ordre is not None and ordre < 0:
            raise ValidationError(
                "L'ordre d'affichage ne peut pas être négatif."
            )

        return ordre

