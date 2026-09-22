from django import forms

from ..models import (
    CategorieExamen,
    TypeExamen,
    Examen,
    TarifExamen,
)


class CategorieExamenForm(forms.ModelForm):
    class Meta:
        model = CategorieExamen
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
                'placeholder': 'Code de la catégorie'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la catégorie'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description'
            }),
            'ordre': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean_code(self):
        code = self.cleaned_data['code'].strip().upper()
        if not code:
            raise forms.ValidationError("Le code est obligatoire.")
        return code

    def clean_nom(self):
        nom = self.cleaned_data['nom'].strip()
        if not nom:
            raise forms.ValidationError("Le nom est obligatoire.")
        return nom


class TypeExamenForm(forms.ModelForm):
    class Meta:
        model = TypeExamen
        fields = [
            'categorie',
            'code',
            'nom',
            'description',
            'ordre',
            'actif',
        ]
        widgets = {
            'categorie': forms.Select(attrs={
                'class': 'form-select'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Code du type'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du type'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description'
            }),
            'ordre': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['categorie'].queryset = (
            CategorieExamen.objects
            .filter(actif=True)
            .order_by('ordre', 'nom')
        )

    def clean_code(self):
        code = self.cleaned_data['code'].strip().upper()
        if not code:
            raise forms.ValidationError("Le code est obligatoire.")
        return code

    def clean_nom(self):
        nom = self.cleaned_data['nom'].strip()
        if not nom:
            raise forms.ValidationError("Le nom est obligatoire.")
        return nom


class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = [
            'type_examen',
            'code',
            'libelle',
            'description',
            'unite',
            'valeur_reference',
            'ordre',
            'actif',
        ]
        widgets = {
            'type_examen': forms.Select(attrs={
                'class': 'form-select'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Code de l’examen'
            }),
            'libelle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Libellé de l’examen'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description'
            }),
            'unite': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex. mg/dL, g/dL, mmol/L'
            }),
            'valeur_reference': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Valeur de référence'
            }),
            'ordre': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['type_examen'].queryset = (
            TypeExamen.objects
            .filter(
                actif=True,
                categorie__actif=True
            )
            .select_related('categorie')
            .order_by(
                'categorie__ordre',
                'categorie__nom',
                'ordre',
                'nom'
            )
        )

    def clean_code(self):
        code = self.cleaned_data['code'].strip().upper()
        if not code:
            raise forms.ValidationError("Le code est obligatoire.")
        return code

    def clean_libelle(self):
        libelle = self.cleaned_data['libelle'].strip()
        if not libelle:
            raise forms.ValidationError("Le libellé est obligatoire.")
        return libelle

    def clean_unite(self):
        return self.cleaned_data['unite'].strip()

    def clean_valeur_reference(self):
        return self.cleaned_data['valeur_reference'].strip()


class TarifExamenForm(forms.ModelForm):
    class Meta:
        model = TarifExamen
        fields = [
            'examen',
            'etablissement',
            'montant',
            'date_debut',
            'date_fin',
            'actif',
        ]
        widgets = {
            'examen': forms.Select(attrs={
                'class': 'form-select'
            }),
            'etablissement': forms.Select(attrs={
                'class': 'form-select'
            }),
            'montant': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': '0.01',
                'placeholder': 'Montant'
            }),
            'date_debut': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'date_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['examen'].queryset = (
            Examen.objects
            .filter(
                actif=True,
                type_examen__actif=True,
                type_examen__categorie__actif=True
            )
            .select_related(
                'type_examen',
                'type_examen__categorie'
            )
            .order_by(
                'type_examen__categorie__ordre',
                'type_examen__categorie__nom',
                'type_examen__ordre',
                'type_examen__nom',
                'ordre',
                'libelle'
            )
        )

    def clean_montant(self):
        montant = self.cleaned_data['montant']

        if montant < 0:
            raise forms.ValidationError(
                "Le montant ne peut pas être négatif."
            )

        return montant

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

