from django import forms

from ..models.pharmacie_partenaire import PharmaciePartenaire


class PharmaciePartenaireForm(forms.ModelForm):

    class Meta:
        model = PharmaciePartenaire

        fields = [
            # ====================================================
            # IDENTIFICATION
            # ====================================================

            'nom',
            'code',

            # ====================================================
            # LOCALISATION
            # ====================================================

            'pays',
            'ville',
            'quartier',
            'adresse',

            # ====================================================
            # CONTACT
            # ====================================================

            'telephone',
            'telephone_secondaire',
            'email',
            'site_web',

            # ====================================================
            # RESPONSABLE
            # ====================================================

            'nom_responsable',
            'fonction_responsable',
            'numero_ordre_responsable',
            'telephone_responsable',
            'email_responsable',

            # ====================================================
            # INFORMATIONS RÉGLEMENTAIRES
            # ====================================================

            'numero_agrement',
            'numero_autorisation',
            'numero_fiscal',
            'registre_commerce',
            'identifiant_administratif',

            # ====================================================
            # PARTENARIAT SANITA
            # ====================================================

            'statut_partenariat',
            'accepte_ordonnances_sanita',
            'date_debut_partenariat',
            'date_fin_partenariat',

            # ====================================================
            # INFORMATIONS GÉNÉRALES
            # ====================================================

            'description',
            'logo',
            'observations',

            # ====================================================
            # CONFIGURATION
            # ====================================================

            'gestion_catalogue_active',
            'gestion_tarifs_active',
            'gestion_stock_active',
            'gestion_ordonnance_active',
            'gestion_dispensation_active',

            # ====================================================
            # STATUT GÉNÉRAL
            # ====================================================

            'actif',
        ]

        widgets = {

            # ====================================================
            # IDENTIFICATION
            # ====================================================

            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la pharmacie',
                'autocomplete': 'organization',
            }),

            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex. PH-PART-001',
                'autocomplete': 'off',
            }),

            # ====================================================
            # LOCALISATION
            # ====================================================

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

            # ====================================================
            # CONTACT
            # ====================================================

            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Téléphone principal',
                'autocomplete': 'tel',
            }),

            'telephone_secondaire': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Téléphone secondaire',
                'autocomplete': 'tel',
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse e-mail',
                'autocomplete': 'email',
            }),

            'site_web': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://...',
                'autocomplete': 'url',
            }),

            # ====================================================
            # RESPONSABLE
            # ====================================================

            'nom_responsable': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom complet du responsable',
                'autocomplete': 'name',
            }),

            'fonction_responsable': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex. Pharmacien titulaire',
            }),

            'numero_ordre_responsable': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Numéro d'ordre",
            }),

            'telephone_responsable': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Téléphone du responsable',
                'autocomplete': 'tel',
            }),

            'email_responsable': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-mail du responsable',
                'autocomplete': 'email',
            }),

            # ====================================================
            # INFORMATIONS RÉGLEMENTAIRES
            # ====================================================

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

            'identifiant_administratif': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Identifiant administratif',
            }),

            # ====================================================
            # PARTENARIAT SANITA
            # ====================================================

            'statut_partenariat': forms.Select(attrs={
                'class': 'form-select',
            }),

            'accepte_ordonnances_sanita': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),

            'date_debut_partenariat': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'date_fin_partenariat': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            # ====================================================
            # INFORMATIONS GÉNÉRALES
            # ====================================================

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': (
                    'Description de la pharmacie partenaire'
                ),
            }),

            'logo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),

            'observations': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Observations',
            }),

            # ====================================================
            # CONFIGURATION
            # ====================================================

            'gestion_catalogue_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),

            'gestion_tarifs_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),

            'gestion_stock_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),

            'gestion_ordonnance_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),

            'gestion_dispensation_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),

            # ====================================================
            # STATUT GÉNÉRAL
            # ====================================================

            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

        labels = {

            # ====================================================
            # IDENTIFICATION
            # ====================================================

            'nom': 'Nom de la pharmacie',
            'code': 'Code pharmacie',

            # ====================================================
            # LOCALISATION
            # ====================================================

            'pays': 'Pays',
            'ville': 'Ville',
            'quartier': 'Quartier',
            'adresse': 'Adresse',

            # ====================================================
            # CONTACT
            # ====================================================

            'telephone': 'Téléphone',
            'telephone_secondaire': 'Téléphone secondaire',
            'email': 'Adresse e-mail',
            'site_web': 'Site web',

            # ====================================================
            # RESPONSABLE
            # ====================================================

            'nom_responsable': 'Nom du responsable',
            'fonction_responsable': 'Fonction',
            'numero_ordre_responsable': "Numéro d'ordre",
            'telephone_responsable': 'Téléphone du responsable',
            'email_responsable': 'E-mail du responsable',

            # ====================================================
            # RÉGLEMENTAIRE
            # ====================================================

            'numero_agrement': "Numéro d'agrément",
            'numero_autorisation': "Numéro d'autorisation",
            'numero_fiscal': 'Numéro fiscal',
            'registre_commerce': 'Registre de commerce',
            'identifiant_administratif': (
                'Identifiant administratif'
            ),

            # ====================================================
            # PARTENARIAT
            # ====================================================

            'statut_partenariat': 'Statut du partenariat',

            'accepte_ordonnances_sanita': (
                'Accepte les ordonnances SANITA'
            ),

            'date_debut_partenariat': (
                'Date de début du partenariat'
            ),

            'date_fin_partenariat': (
                'Date de fin du partenariat'
            ),

            # ====================================================
            # GÉNÉRAL
            # ====================================================

            'description': 'Description',
            'logo': 'Logo',
            'observations': 'Observations',

            # ====================================================
            # CONFIGURATION
            # ====================================================

            'gestion_catalogue_active': (
                'Gestion du catalogue'
            ),

            'gestion_tarifs_active': (
                'Gestion des tarifs'
            ),

            'gestion_stock_active': (
                'Gestion du stock'
            ),

            'gestion_ordonnance_active': (
                'Gestion des ordonnances'
            ),

            'gestion_dispensation_active': (
                'Gestion de la dispensation'
            ),

            # ====================================================
            # STATUT
            # ====================================================

            'actif': 'Pharmacie active',
        }

        help_texts = {

            'code': (
                "Identifiant unique utilisé pour identifier "
                "la pharmacie partenaire dans SANITA."
            ),

            'accepte_ordonnances_sanita': (
                "Autorise la réception et le traitement des "
                "ordonnances émises depuis SANITA."
            ),

            'gestion_catalogue_active': (
                "Permet de gérer le catalogue des médicaments "
                "de la pharmacie partenaire."
            ),

            'gestion_tarifs_active': (
                "Permet de gérer les tarifs appliqués par "
                "la pharmacie partenaire."
            ),

            'gestion_stock_active': (
                "Active la gestion du stock de la pharmacie."
            ),

            'gestion_ordonnance_active': (
                "Active la réception et le traitement des "
                "ordonnances SANITA."
            ),

            'gestion_dispensation_active': (
                "Active la validation et la dispensation "
                "des médicaments aux patients."
            ),
        }

    # ============================================================
    # VALIDATIONS
    # ============================================================

    def clean(self):
        cleaned_data = super().clean()

        date_debut = cleaned_data.get(
            'date_debut_partenariat'
        )

        date_fin = cleaned_data.get(
            'date_fin_partenariat'
        )

        if date_debut and date_fin and date_fin < date_debut:
            self.add_error(
                'date_fin_partenariat',
                (
                    "La date de fin du partenariat ne peut pas "
                    "être antérieure à la date de début."
                )
            )

        return cleaned_data