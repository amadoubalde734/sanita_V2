from django import forms

from ..models import EtablissementPartenaire


class EtablissementPartenaireForm(forms.ModelForm):
    """Formulaire d'ajout / modification d'un établissement partenaire."""

    class Meta:
        model = EtablissementPartenaire

        fields = [
            # Identification
            'nom',
            'code',
            'type_partenaire',

            # Localisation
            'pays',
            'ville',
            'quartier',
            'adresse',

            # Coordonnées
            'telephone',
            'telephone_secondaire',
            'email',
            'site_web',

            # Contact principal
            'nom_contact',
            'fonction_contact',
            'telephone_contact',
            'email_contact',

            # Informations administratives
            'numero_agrement',
            'numero_autorisation',
            'numero_fiscal',
            'registre_commerce',

            # Spécialités
            'specialites',

            # Partenariat
            'statut_partenaire',
            'date_debut_partenariat',
            'date_fin_partenariat',
            'accepte_orientation',
            'actif',

            # Informations complémentaires
            'description',
        ]

        widgets = {
            # ---------- Identification ----------
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Nom de l'établissement",
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex : CLIN-001',
                'style': 'text-transform: uppercase;',
            }),
            'type_partenaire': forms.Select(attrs={
                'class': 'form-select',
            }),

            # ---------- Localisation ----------
            'pays': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pays',
            }),
            'ville': forms.Select(attrs={
                'class': 'form-select',
            }),
            'quartier': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quartier',
            }),
            'adresse': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Adresse complète',
            }),

            # ---------- Coordonnées ----------
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Téléphone',
            }),
            'telephone_secondaire': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Téléphone secondaire',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contact@exemple.com',
            }),
            'site_web': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://...',
            }),

            # ---------- Contact principal ----------
            'nom_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du responsable',
            }),
            'fonction_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fonction du contact',
            }),
            'telephone_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Téléphone du contact',
            }),
            'email_contact': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email du contact',
            }),

            # ---------- Informations administratives ----------
            'numero_agrement': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Numéro d'agrément",
            }),
            'numero_autorisation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Numéro d'autorisation",
            }),
            'numero_fiscal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro fiscal',
            }),
            'registre_commerce': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Registre de commerce',
            }),

            # ---------- Spécialités ----------
            'specialites': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': 6,
            }),

            # ---------- Partenariat ----------
            'statut_partenaire': forms.Select(attrs={
                'class': 'form-select',
            }),
            # format='%Y-%m-%d' est OBLIGATOIRE pour un <input type="date">,
            # sinon la date est vide lors de la modification.
            'date_debut_partenariat': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d',
            ),
            'date_fin_partenariat': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d',
            ),
            'accepte_orientation': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),

            # ---------- Informations complémentaires ----------
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Informations complémentaires',
            }),
        }

        labels = {
            'nom': "Nom de l'établissement",
            'code': "Code partenaire",
            'type_partenaire': "Type de structure",
            'pays': "Pays",
            'ville': "Ville",
            'quartier': "Quartier",
            'adresse': "Adresse",
            'telephone': "Téléphone",
            'telephone_secondaire': "Téléphone secondaire",
            'email': "Adresse e-mail",
            'site_web': "Site web",
            'nom_contact': "Nom du contact",
            'fonction_contact': "Fonction du contact",
            'telephone_contact': "Téléphone du contact",
            'email_contact': "E-mail du contact",
            'numero_agrement': "Numéro d'agrément",
            'numero_autorisation': "Numéro d'autorisation",
            'numero_fiscal': "Numéro fiscal",
            'registre_commerce': "Registre de commerce",
            'specialites': "Spécialités",
            'statut_partenaire': "Statut du partenariat",
            'date_debut_partenariat': "Date de début du partenariat",
            'date_fin_partenariat': "Date de fin du partenariat",
            'accepte_orientation': "Accepte les orientations",
            'actif': "Établissement actif",
            'description': "Description",
        }

        help_texts = {
            'code': "Le code doit être unique pour chaque établissement partenaire.",
            'specialites': "Maintenez Ctrl (ou Cmd sur Mac) pour sélectionner plusieurs spécialités.",
            'accepte_orientation': "Indique si cet établissement accepte les patients orientés par SANITA.",
        }

    # ------------------------------------------------------------
    # INITIALISATION
    # ------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Texte affiché en tête des listes déroulantes
        if 'ville' in self.fields:
            self.fields['ville'].empty_label = "— Sélectionner une ville —"

        # Formats de date acceptés à la saisie
        for champ in ('date_debut_partenariat', 'date_fin_partenariat'):
            self.fields[champ].input_formats = ['%Y-%m-%d', '%d/%m/%Y']

    # ------------------------------------------------------------
    # VALIDATIONS
    # ------------------------------------------------------------
    def clean_code(self):
        """Code en majuscules, sans espaces, et unique."""
        code = (self.cleaned_data.get('code') or '').strip().upper()

        if code:
            doublon = EtablissementPartenaire.objects.filter(code__iexact=code)
            if self.instance.pk:
                doublon = doublon.exclude(pk=self.instance.pk)
            if doublon.exists():
                raise forms.ValidationError(
                    "Ce code est déjà utilisé par un autre établissement partenaire."
                )

        return code

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.strip().lower() if email else email

    def clean_email_contact(self):
        email = self.cleaned_data.get('email_contact')
        return email.strip().lower() if email else email

    def clean(self):
        cleaned_data = super().clean()

        date_debut = cleaned_data.get('date_debut_partenariat')
        date_fin = cleaned_data.get('date_fin_partenariat')

        if date_debut and date_fin and date_fin < date_debut:
            self.add_error(
                'date_fin_partenariat',
                "La date de fin ne peut pas être antérieure à la date de début.",
            )

        return cleaned_data