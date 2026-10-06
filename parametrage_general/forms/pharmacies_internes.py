from django import forms

from ..models import PharmacieInterne


class PharmacieInterneForm(forms.ModelForm):

    class Meta:
        model = PharmacieInterne

        fields = [
            # Identification
            "nom",
            "code",

            # Rattachement
            "site",
            "unite_medicale",

            # Localisation
            "localisation",

            # Contact
            "telephone",
            "email",

            # Responsable
            "nom_responsable",
            "fonction_responsable",
            "telephone_responsable",
            "email_responsable",

            # Stock
            "gestion_stock_active",
            "gestion_lots_active",
            "gestion_peremption_active",
            "gestion_inventaire_active",
            "gestion_transfert_active",

            # Dispensation
            "gestion_dispensation_active",

            # Informations générales
            "description",
            "observations",

            # Statut
            "actif",
        ]

        widgets = {

            # ----------------------------------------------------
            # Identification
            # ----------------------------------------------------

            "nom": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex. Pharmacie interne Site Conakry",
                }
            ),

            "code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex. PH-INT-CON-01",
                }
            ),

            # ----------------------------------------------------
            # Rattachement
            # ----------------------------------------------------

            "site": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "unite_medicale": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            # ----------------------------------------------------
            # Localisation
            # ----------------------------------------------------

            "localisation": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex. Bâtiment médical, rez-de-chaussée",
                }
            ),

            # ----------------------------------------------------
            # Contact
            # ----------------------------------------------------

            "telephone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Téléphone",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Adresse e-mail",
                }
            ),

            # ----------------------------------------------------
            # Responsable
            # ----------------------------------------------------

            "nom_responsable": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nom du responsable",
                }
            ),

            "fonction_responsable": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex. Pharmacien responsable",
                }
            ),

            "telephone_responsable": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Téléphone du responsable",
                }
            ),

            "email_responsable": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "E-mail du responsable",
                }
            ),

            # ----------------------------------------------------
            # Informations générales
            # ----------------------------------------------------

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Description de la pharmacie interne",
                }
            ),

            "observations": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Observations",
                }
            ),

            # ----------------------------------------------------
            # Configuration
            # ----------------------------------------------------

            "gestion_stock_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "gestion_lots_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "gestion_peremption_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "gestion_inventaire_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "gestion_transfert_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "gestion_dispensation_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "actif": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

        labels = {
            "nom": "Nom de la pharmacie",
            "code": "Code pharmacie",
            "site": "Site",
            "unite_medicale": "Unité médicale",
            "localisation": "Localisation",
            "telephone": "Téléphone",
            "email": "Adresse e-mail",
            "nom_responsable": "Nom du responsable",
            "fonction_responsable": "Fonction du responsable",
            "telephone_responsable": "Téléphone du responsable",
            "email_responsable": "E-mail du responsable",
            "gestion_stock_active": "Gestion du stock",
            "gestion_lots_active": "Gestion des lots",
            "gestion_peremption_active": "Gestion des péremptions",
            "gestion_inventaire_active": "Gestion des inventaires",
            "gestion_transfert_active": "Gestion des transferts",
            "gestion_dispensation_active": "Gestion de la dispensation",
            "description": "Description",
            "observations": "Observations",
            "actif": "Pharmacie active",
        }

    # ============================================================
    # INITIALISATION
    # ============================================================

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # --------------------------------------------------------
        # Unités médicales : uniquement celles rattachées à un site
        # --------------------------------------------------------

        self.fields["unite_medicale"].queryset = (
            self.fields["unite_medicale"]
            .queryset
            .select_related("site")
            .order_by("nom")
        )

        self.fields["site"].queryset = (
            self.fields["site"]
            .queryset
            .filter(actif=True)
            .order_by("nom_site")
        )

        # --------------------------------------------------------
        # Champs obligatoires
        # --------------------------------------------------------

        self.fields["nom"].required = True
        self.fields["code"].required = True
        self.fields["site"].required = True

    # ============================================================
    # VALIDATION
    # ============================================================

    def clean(self):

        cleaned_data = super().clean()

        site = cleaned_data.get("site")
        unite_medicale = cleaned_data.get("unite_medicale")

        if site and unite_medicale:

            if unite_medicale.site_id != site.id:
                self.add_error(
                    "unite_medicale",
                    (
                        "L'unité médicale sélectionnée doit "
                        "appartenir au site choisi."
                    )
                )

        return cleaned_data