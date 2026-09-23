from django import forms
from django.db.models import Q

from ..models import (
    TypeSejour,
    TypeChambre,
    Chambre,
    Lit,
    TypeSoin,
    RegimeAlimentaire,
    MotifHospitalisation,
    TypeSortie,
    TarifSejour,
    ConfigurationEtablissement,
    UniteMedicale,
)


class TypeSejourForm(forms.ModelForm):
    class Meta:
        model = TypeSejour
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
                'placeholder': 'Code du type de séjour',
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du type de séjour',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description',
            }),
            'ordre': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_code(self):
        code = self.cleaned_data['code'].strip().upper()

        if not code:
            raise forms.ValidationError(
                "Le code est obligatoire."
            )

        return code

    def clean_nom(self):
        nom = self.cleaned_data['nom'].strip()

        if not nom:
            raise forms.ValidationError(
                "Le nom est obligatoire."
            )

        return nom


class TypeChambreForm(forms.ModelForm):
    class Meta:
        model = TypeChambre
        fields = [
            'code',
            'nom',
            'description',
            'capacite',
            'ordre',
            'actif',
        ]
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Code du type de chambre',
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du type de chambre',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description',
            }),
            'capacite': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
            }),
            'ordre': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_code(self):
        return self.cleaned_data['code'].strip().upper()

    def clean_nom(self):
        return self.cleaned_data['nom'].strip()

    def clean_capacite(self):
        capacite = self.cleaned_data['capacite']

        if capacite < 1:
            raise forms.ValidationError(
                "La capacité doit être supérieure ou égale à 1."
            )

        return capacite


class ChambreForm(forms.ModelForm):
    class Meta:
        model = Chambre
        fields = [
            'etablissement',
            'unite',
            'type_chambre',
            'code',
            'nom',
            'etage',
            'localisation',
            'capacite',
            'description',
            'actif',
        ]
        widgets = {
            'etablissement': forms.Select(attrs={
                'class': 'form-select',
            }),
            'unite': forms.Select(attrs={
                'class': 'form-select',
            }),
            'type_chambre': forms.Select(attrs={
                'class': 'form-select',
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro ou code de la chambre',
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la chambre',
            }),
            'etage': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex. Rez-de-chaussée, 1er étage',
            }),
            'localisation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Localisation',
            }),
            'capacite': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        etablissement_qs = (
            ConfigurationEtablissement.objects
            .filter(actif=True)
            .order_by('nom_etablissement')
        )

        unite_qs = (
            UniteMedicale.objects
            .filter(actif=True)
            .select_related('site')
            .order_by('nom')
        )

        type_chambre_qs = (
            TypeChambre.objects
            .filter(actif=True)
            .order_by('ordre', 'nom')
        )

        if self.instance and self.instance.pk:
            if self.instance.etablissement_id:
                etablissement_qs = (
                    ConfigurationEtablissement.objects
                    .filter(
                        Q(actif=True) |
                        Q(pk=self.instance.etablissement_id)
                    )
                    .order_by('nom_etablissement')
                )

            if self.instance.unite_id:
                unite_qs = (
                    UniteMedicale.objects
                    .filter(
                        Q(actif=True) |
                        Q(pk=self.instance.unite_id)
                    )
                    .select_related('site')
                    .order_by('nom')
                )

            if self.instance.type_chambre_id:
                type_chambre_qs = (
                    TypeChambre.objects
                    .filter(
                        Q(actif=True) |
                        Q(pk=self.instance.type_chambre_id)
                    )
                    .order_by('ordre', 'nom')
                )

        self.fields['etablissement'].queryset = etablissement_qs
        self.fields['unite'].queryset = unite_qs
        self.fields['type_chambre'].queryset = type_chambre_qs

    def clean_code(self):
        return self.cleaned_data['code'].strip().upper()

    def clean_nom(self):
        return self.cleaned_data['nom'].strip()

    def clean_capacite(self):
        capacite = self.cleaned_data['capacite']

        if capacite < 1:
            raise forms.ValidationError(
                "La capacité doit être supérieure ou égale à 1."
            )

        return capacite

    def clean(self):
        cleaned_data = super().clean()

        etablissement = cleaned_data.get('etablissement')
        unite = cleaned_data.get('unite')

        if etablissement and unite:
            if hasattr(unite, 'etablissement_id'):
                if unite.etablissement_id != etablissement.id:
                    self.add_error(
                        'unite',
                        "L’unité sélectionnée n’appartient pas à l’établissement choisi."
                    )

        return cleaned_data


class LitForm(forms.ModelForm):
    class Meta:
        model = Lit
        fields = [
            'chambre',
            'code',
            'description',
            'statut',
            'actif',
        ]
        widgets = {
            'chambre': forms.Select(attrs={
                'class': 'form-select',
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro ou code du lit',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description',
            }),
            'statut': forms.Select(attrs={
                'class': 'form-select',
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['chambre'].queryset = (
            Chambre.objects
            .filter(
                actif=True,
                etablissement__actif=True,
                unite__actif=True,
            )
            .select_related(
                'etablissement',
                'unite',
                'type_chambre',
            )
            .order_by(
                'etablissement__nom_etablissement',
                'unite__nom',
                'code',
            )
        )

    def clean_code(self):
        return self.cleaned_data['code'].strip().upper()


class TypeSoinForm(forms.ModelForm):
    class Meta:
        model = TypeSoin
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
                'placeholder': 'Code du soin',
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du soin',
            }),
            'categorie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Catégorie du soin',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description',
            }),
            'ordre': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_code(self):
        return self.cleaned_data['code'].strip().upper()

    def clean_nom(self):
        return self.cleaned_data['nom'].strip()

    def clean_categorie(self):
        return self.cleaned_data['categorie'].strip()


class RegimeAlimentaireForm(forms.ModelForm):
    class Meta:
        model = RegimeAlimentaire
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
                'placeholder': 'Code du régime',
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du régime',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description',
            }),
            'ordre': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_code(self):
        return self.cleaned_data['code'].strip().upper()

    def clean_nom(self):
        return self.cleaned_data['nom'].strip()


class MotifHospitalisationForm(forms.ModelForm):
    class Meta:
        model = MotifHospitalisation
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
                'placeholder': 'Code du motif',
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du motif',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description',
            }),
            'ordre': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_code(self):
        return self.cleaned_data['code'].strip().upper()

    def clean_nom(self):
        return self.cleaned_data['nom'].strip()


class TypeSortieForm(forms.ModelForm):
    class Meta:
        model = TypeSortie
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
                'placeholder': 'Code du type de sortie',
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du type de sortie',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description',
            }),
            'ordre': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_code(self):
        return self.cleaned_data['code'].strip().upper()

    def clean_nom(self):
        return self.cleaned_data['nom'].strip()


class TarifSejourForm(forms.ModelForm):
    class Meta:
        model = TarifSejour
        fields = [
            'etablissement',
            'type_sejour',
            'type_chambre',
            'montant',
            'unite_facturation',
            'date_debut',
            'date_fin',
            'actif',
        ]
        widgets = {
            'etablissement': forms.Select(attrs={
                'class': 'form-select',
            }),
            'type_sejour': forms.Select(attrs={
                'class': 'form-select',
            }),
            'type_chambre': forms.Select(attrs={
                'class': 'form-select',
            }),
            'montant': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': '0.01',
                'placeholder': 'Montant',
            }),
            'unite_facturation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex. jour, nuit, séjour',
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

        self.fields['etablissement'].queryset = (
            ConfigurationEtablissement.objects
            .filter(actif=True)
            .order_by('nom_etablissement')
        )

        self.fields['type_sejour'].queryset = (
            TypeSejour.objects
            .filter(actif=True)
            .order_by('ordre', 'nom')
        )

        self.fields['type_chambre'].queryset = (
            TypeChambre.objects
            .filter(actif=True)
            .order_by('ordre', 'nom')
        )

    def clean_montant(self):
        montant = self.cleaned_data['montant']

        if montant < 0:
            raise forms.ValidationError(
                "Le montant ne peut pas être négatif."
            )

        return montant

    def clean_unite_facturation(self):
        unite = self.cleaned_data['unite_facturation'].strip()

        if not unite:
            raise forms.ValidationError(
                "L’unité de facturation est obligatoire."
            )

        return unite

    def clean(self):
        cleaned_data = super().clean()

        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')

        if date_debut and date_fin and date_fin < date_debut:
            self.add_error(
                'date_fin',
                "La date de fin doit être postérieure ou égale à la date de début."
            )

        return cleaned_data