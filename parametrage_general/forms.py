from django import forms
from django.core.exceptions import ValidationError
from django_countries.widgets import CountrySelectWidget
from .models import (
    Societe,
    Ville,
    Site,
    Departement,
    Direction,
    Service,
    Fonction,
    Specialite,
    UniteMedicale,
    ConfigurationEtablissement,
)


class SocieteForm(forms.ModelForm):
    class Meta:
        model = Societe
        fields = ['libelle', 'date_integration', 'actif']
        widgets = {
            'date_integration': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'actif': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name != 'actif':
                field.widget.attrs.update({'class': 'form-control'})

    def clean_libelle(self):
        libelle = self.cleaned_data['libelle'].strip()
        qs = Societe.objects.filter(libelle__iexact=libelle)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "Une société avec ce nom existe déjà."
            )

        return libelle


class VilleForm(forms.ModelForm):
    class Meta:
        model = Ville
        fields = ['pays', 'libelle', 'actif']
        widgets = {
            'pays': CountrySelectWidget(
                attrs={'class': 'form-control'}
            ),
            'libelle': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'actif': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name != 'actif':
                field.widget.attrs.update({'class': 'form-control'})

    def clean_libelle(self):
        libelle = self.cleaned_data.get('libelle')
        pays = self.cleaned_data.get('pays')

        qs = Ville.objects.filter(
            libelle__iexact=libelle,
            pays=pays
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "Cette ville existe déjà pour ce pays."
            )

        return libelle


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['nom_site', 'adresse', 'description', 'actif']
        widgets = {
            'nom_site': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'adresse': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'actif': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name != 'actif':
                field.widget.attrs.update({'class': 'form-control'})

    def clean_nom_site(self):
        nom_site = self.cleaned_data.get('nom_site')

        qs = Site.objects.filter(
            nom_site__iexact=nom_site
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(
                "Un site avec ce nom existe déjà."
            )

        return nom_site

    def clean_adresse(self):
        adresse = self.cleaned_data.get('adresse')

        if adresse and len(adresse) < 5:
            raise ValidationError(
                "L'adresse est trop courte."
            )

        return adresse


class DirectionForm(forms.ModelForm):
    class Meta:
        model = Direction
        fields = ['nom', 'description', 'actif']
        widgets = {
            'nom': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'actif': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name != 'actif':
                field.widget.attrs.update({'class': 'form-control'})

    def clean_nom(self):
        nom = self.cleaned_data.get('nom')

        qs = Direction.objects.filter(
            nom__iexact=nom
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(
                "Une direction avec ce nom existe déjà."
            )

        return nom


class DepartementForm(forms.ModelForm):
    class Meta:
        model = Departement
        fields = ['nom', 'direction', 'description', 'actif']
        widgets = {
            'nom': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'direction': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'actif': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name != 'actif':
                field.widget.attrs.update({'class': 'form-control'})

        self.fields['direction'].queryset = Direction.objects.filter(
            actif=True
        )
        self.fields['direction'].required = False

    def clean_nom(self):
        nom = self.cleaned_data.get('nom')

        qs = Departement.objects.filter(
            nom__iexact=nom
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(
                "Un département avec ce nom existe déjà."
            )

        return nom


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['nom', 'departement', 'description', 'actif']
        widgets = {
            'nom': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'departement': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'actif': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['departement'].queryset = Departement.objects.filter(
            actif=True
        )

    def clean(self):
        cleaned_data = super().clean()

        nom = cleaned_data.get('nom')
        departement = cleaned_data.get('departement')

        if nom and departement:
            qs = Service.objects.filter(
                nom__iexact=nom,
                departement=departement
            )

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise ValidationError(
                    "Un service avec ce nom existe déjà dans ce département."
                )

        return cleaned_data


class FonctionForm(forms.ModelForm):
    class Meta:
        model = Fonction
        fields = ['nom', 'service', 'description', 'actif']
        widgets = {
            'nom': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'service': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'actif': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name != 'actif':
                field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()

        nom = cleaned_data.get('nom')
        service = cleaned_data.get('service')

        if nom and service:
            qs = Fonction.objects.filter(
                nom__iexact=nom,
                service=service
            )

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise ValidationError(
                    "Une fonction avec ce nom existe déjà dans ce service."
                )

        return cleaned_data


class SpecialiteForm(forms.ModelForm):
    class Meta:
        model = Specialite
        fields = ['nom', 'description', 'icone', 'actif']
        widgets = {
            'nom': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: Dentaire, Ophtalmologie...'
                }
            ),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'icone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: ri-tooth-line'
                }
            ),
            'actif': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name != 'actif':
                field.widget.attrs.update({'class': 'form-control'})

    def clean_nom(self):
        nom = self.cleaned_data.get('nom')

        qs = Specialite.objects.filter(
            nom__iexact=nom
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(
                "Une spécialité avec ce nom existe déjà."
            )

        return nom


class UniteMedicaleForm(forms.ModelForm):
    class Meta:
        model = UniteMedicale
        fields = [
            'nom',
            'type_unite',
            'site',
            'specialites',
            'description',
            'actif',
        ]
        widgets = {
            'nom': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: Infirmerie Conakry'
                }
            ),
            'type_unite': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'site': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'specialites': forms.SelectMultiple(
                attrs={
                    'class': 'form-select',
                    'size': 6
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Description de l’unité médicale'
                }
            ),
            'actif': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configuration = ConfigurationEtablissement.objects.first()

        self.fields['site'].queryset = (
            Site.objects
            .filter(actif=True)
            .order_by('nom_site')
        )
        self.fields['site'].required = False

        if self.configuration:
            self.fields['specialites'].queryset = (
                self.configuration.specialites
                .filter(actif=True)
                .order_by('nom')
            )
        else:
            self.fields['specialites'].queryset = (
                Specialite.objects.none()
            )

        self.fields['specialites'].required = False

    def clean_nom(self):
        nom = self.cleaned_data.get('nom')

        qs = UniteMedicale.objects.filter(
            nom__iexact=nom
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(
                "Une unité médicale avec ce nom existe déjà."
            )

        return nom

    def clean_specialites(self):
        specialites = self.cleaned_data.get('specialites')

        if not specialites:
            return specialites

        if not self.configuration:
            raise ValidationError(
                "Aucune configuration d'établissement n'est définie."
            )

        specialites_autorisees = set(
            self.configuration.specialites
            .filter(actif=True)
            .values_list('id', flat=True)
        )

        specialites_invalides = [
            specialite
            for specialite in specialites
            if specialite.id not in specialites_autorisees
        ]

        if specialites_invalides:
            raise ValidationError(
                "Une ou plusieurs spécialités sélectionnées "
                "ne sont pas déclarées dans l'établissement."
            )

        return specialites


class ConfigurationEtablissementForm(forms.ModelForm):
    class Meta:
        model = ConfigurationEtablissement

        fields = [
            'nom_etablissement',
            'code_etablissement',
            'type_etablissement',
            'specialites',
            'pays',
            'ville',
            'adresse',
            'boite_postale',
            'telephone',
            'telephone_secondaire',
            'email',
            'site_web',
            'logo',
            'numero_agrement',
            'numero_autorisation',
            'numero_fiscal',
            'registre_commerce',
            'identifiant_administratif',
            'devise',
            'fuseau_horaire',
            'module_prise_en_charge_actif',
            'module_conventions_actif',
            'actif',
        ]

        widgets = {
            'nom_etablissement': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: Clinique Sainte-Marie'
                }
            ),
            'code_etablissement': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: CSM-001'
                }
            ),
            'type_etablissement': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'specialites': forms.SelectMultiple(
                attrs={
                    'class': 'form-select',
                    'size': 6
                }
            ),
            'pays': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: Guinée'
                }
            ),
            'ville': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'adresse': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': "Adresse complète de l'établissement"
                }
            ),
            'boite_postale': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: BP 123'
                }
            ),
            'telephone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: +224 600 00 00 00'
                }
            ),
            'telephone_secondaire': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: +224 622 00 00 00'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'contact@etablissement.com'
                }
            ),
            'site_web': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'https://www.etablissement.com'
                }
            ),
            'logo': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),
            'numero_agrement': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Numéro d'agrément"
                }
            ),
            'numero_autorisation': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Numéro d'autorisation"
                }
            ),
            'numero_fiscal': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Numéro fiscal'
                }
            ),
            'registre_commerce': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Registre de commerce'
                }
            ),
            'identifiant_administratif': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Identifiant administratif'
                }
            ),
            'devise': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: GNF'
                }
            ),
            'fuseau_horaire': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: Africa/Conakry'
                }
            ),
            'module_prise_en_charge_actif': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'module_conventions_actif': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'actif': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['specialites'].queryset = (
            Specialite.objects
            .filter(actif=True)
            .order_by('nom')
        )
        self.fields['specialites'].required = False

        self.fields['ville'].queryset = (
            Ville.objects
            .filter(actif=True)
            .order_by('libelle')
        )
        self.fields['ville'].required = False

