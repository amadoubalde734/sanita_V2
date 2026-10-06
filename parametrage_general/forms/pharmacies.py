from django import forms

from ..models import Pharmacie


class PharmacieForm(forms.ModelForm):

    class Meta:
        model = Pharmacie

        fields = [
            'nom',
            'code',
            'type_pharmacie',

            'site',
            'unite_medicale',
            'etablissement_partenaire',

            'pays',
            'ville',
            'quartier',
            'adresse',

            'telephone',
            'telephone_secondaire',
            'email',
            'site_web',

            'nom_responsable',
            'fonction_responsable',
            'numero_ordre_responsable',
            'telephone_responsable',
            'email_responsable',

            'numero_agrement',
            'numero_autorisation',
            'numero_fiscal',
            'registre_commerce',

            'statut_partenaire',
            'accepte_ordonnances_sanita',
            'date_debut_partenariat',
            'date_fin_partenariat',

            'description',
            'logo',

            'gestion_stock_active',
            'gestion_vente_active',
            'gestion_ordonnance_active',
            'gestion_lots_active',
            'gestion_inventaire_active',

            'actif',
        ]

        widgets = {
            'nom': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nom de la pharmacie',
                }
            ),

            'code': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex : PHAR-001',
                }
            ),

            'type_pharmacie': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'site': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'unite_medicale': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'etablissement_partenaire': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'pays': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),

            'ville': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'quartier': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Quartier',
                }
            ),

            'adresse': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Adresse complète',
                }
            ),

            'telephone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Téléphone',
                }
            ),

            'telephone_secondaire': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Téléphone secondaire',
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'contact@exemple.com',
                }
            ),

            'site_web': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'https://...',
                }
            ),

            'nom_responsable': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nom du responsable',
                }
            ),

            'fonction_responsable': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Pharmacien titulaire',
                }
            ),

            'numero_ordre_responsable': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Numéro d'ordre",
                }
            ),

            'telephone_responsable': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Téléphone du responsable',
                }
            ),

            'email_responsable': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'responsable@exemple.com',
                }
            ),

            'numero_agrement': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Numéro d'agrément",
                }
            ),

            'numero_autorisation': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Numéro d'autorisation",
                }
            ),

            'numero_fiscal': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Numéro fiscal',
                }
            ),

            'registre_commerce': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Registre de commerce',
                }
            ),

            'statut_partenaire': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'accepte_ordonnances_sanita': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),

            'date_debut_partenariat': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),

            'date_fin_partenariat': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Informations complémentaires',
                }
            ),

            'logo': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                }
            ),

            'gestion_stock_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),

            'gestion_vente_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),

            'gestion_ordonnance_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),

            'gestion_lots_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),

            'gestion_inventaire_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),

            'actif': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
        }

        labels = {
            'nom': 'Nom de la pharmacie',
            'code': 'Code pharmacie',
            'type_pharmacie': 'Type de pharmacie',

            'site': 'Site',
            'unite_medicale': 'Unité médicale',
            'etablissement_partenaire': 'Établissement partenaire',

            'pays': 'Pays',
            'ville': 'Ville',
            'quartier': 'Quartier',
            'adresse': 'Adresse',

            'telephone': 'Téléphone',
            'telephone_secondaire': 'Téléphone secondaire',
            'email': 'Adresse e-mail',
            'site_web': 'Site web',

            'nom_responsable': 'Nom du responsable',
            'fonction_responsable': 'Fonction du responsable',
            'numero_ordre_responsable': "Numéro d'ordre",
            'telephone_responsable': 'Téléphone du responsable',
            'email_responsable': 'E-mail du responsable',

            'numero_agrement': "Numéro d'agrément",
            'numero_autorisation': "Numéro d'autorisation",
            'numero_fiscal': 'Numéro fiscal',
            'registre_commerce': 'Registre de commerce',

            'statut_partenaire': 'Statut du partenariat',
            'accepte_ordonnances_sanita': 'Accepte les ordonnances SANITA',
            'date_debut_partenariat': 'Date de début du partenariat',
            'date_fin_partenariat': 'Date de fin du partenariat',

            'description': 'Description',
            'logo': 'Logo',

            'gestion_stock_active': 'Gestion du stock active',
            'gestion_vente_active': 'Gestion des ventes active',
            'gestion_ordonnance_active': 'Gestion des ordonnances active',
            'gestion_lots_active': 'Gestion des lots active',
            'gestion_inventaire_active': 'Gestion des inventaires active',

            'actif': 'Pharmacie active',
        }

        help_texts = {
            'code': (
                'Le code doit être unique pour chaque pharmacie.'
            ),

            'etablissement_partenaire': (
                "À renseigner lorsque la pharmacie est rattachée "
                "à un établissement partenaire."
            ),

            'accepte_ordonnances_sanita': (
                "Autorise la pharmacie à recevoir et traiter "
                "les ordonnances émises depuis SANITA."
            ),

            'gestion_stock_active': (
                "Active la gestion des stocks de médicaments."
            ),

            'gestion_lots_active': (
                "Active le suivi des lots et des dates d'expiration."
            ),
        }

    def clean_code(self):
        code = self.cleaned_data.get('code')

        if code:
            code = code.strip().upper()

        return code

    def clean(self):
        cleaned_data = super().clean()

        type_pharmacie = cleaned_data.get('type_pharmacie')
        statut_partenaire = cleaned_data.get('statut_partenaire')

        site = cleaned_data.get('site')
        unite_medicale = cleaned_data.get('unite_medicale')
        etablissement_partenaire = cleaned_data.get(
            'etablissement_partenaire'
        )

        date_debut = cleaned_data.get(
            'date_debut_partenariat'
        )

        date_fin = cleaned_data.get(
            'date_fin_partenariat'
        )

        # --------------------------------------------------------
        # Vérification des dates de partenariat
        # --------------------------------------------------------

        if date_debut and date_fin and date_fin < date_debut:
            self.add_error(
                'date_fin_partenariat',
                (
                    "La date de fin ne peut pas être antérieure "
                    "à la date de début."
                )
            )

        # --------------------------------------------------------
        # Cohérence pharmacie indépendante
        # --------------------------------------------------------

        if type_pharmacie == 'independante':
            if etablissement_partenaire:
                self.add_error(
                    'etablissement_partenaire',
                    (
                        "Une pharmacie indépendante ne doit pas "
                        "être rattachée à un établissement partenaire."
                    )
                )

        # --------------------------------------------------------
        # Pharmacie d'établissement / partenaire
        # --------------------------------------------------------

        if type_pharmacie in [
            'etablissement',
            'partenaire',
            'hospitaliere',
        ]:
            if not etablissement_partenaire and type_pharmacie != 'hospitaliere':
                self.add_error(
                    'etablissement_partenaire',
                    (
                        "Veuillez sélectionner l'établissement "
                        "auquel cette pharmacie est rattachée."
                    )
                )

        # --------------------------------------------------------
        # Cohérence partenariat
        # --------------------------------------------------------

        if statut_partenaire == 'non_partenaire':
            if date_debut or date_fin:
                self.add_error(
                    'date_debut_partenariat',
                    (
                        "Les dates de partenariat doivent être "
                        "vides pour une pharmacie non partenaire."
                    )
                )

        # --------------------------------------------------------
        # Site / unité médicale
        # --------------------------------------------------------

        if unite_medicale and site:
            if unite_medicale.site_id and (
                unite_medicale.site_id != site.id
            ):
                self.add_error(
                    'unite_medicale',
                    (
                        "L'unité médicale sélectionnée n'appartient "
                        "pas au site choisi."
                    )
                )

        return cleaned_data