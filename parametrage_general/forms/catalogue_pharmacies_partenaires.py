from django import forms

from ..models.catalogue_pharmacies_partenaires import (
    CatalogueMedicamentPharmaciePartenaire,
)


class CatalogueMedicamentPharmaciePartenaireForm(forms.ModelForm):

    class Meta:
        model = CatalogueMedicamentPharmaciePartenaire

        fields = [
            "pharmacie",
            "medicament",
            "reference_interne",
            "nom_commercial",
            "disponible",
            "sur_commande",
            "unite_vente",
            "conditionnement",
            "accepte_ordonnance",
            "dispensation_active",
            "actif",
            "description",
            "observations",
        ]

        labels = {
            "pharmacie": "Pharmacie partenaire",
            "medicament": "Médicament",
            "reference_interne": "Référence interne",
            "nom_commercial": "Nom commercial",
            "disponible": "Disponible",
            "sur_commande": "Disponible sur commande",
            "unite_vente": "Unité de vente",
            "conditionnement": "Conditionnement",
            "accepte_ordonnance": "Nécessite une ordonnance",
            "dispensation_active": "Dispensation active",
            "actif": "Actif",
            "description": "Description",
            "observations": "Observations",
        }

        widgets = {
            "pharmacie": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "medicament": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "reference_interne": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Référence interne de la pharmacie",
                }
            ),

            "nom_commercial": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nom commercial",
                }
            ),

            "disponible": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "sur_commande": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "unite_vente": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex. boîte, flacon, comprimé...",
                }
            ),

            "conditionnement": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex. boîte de 20 comprimés",
                }
            ),

            "accepte_ordonnance": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "dispensation_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "actif": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": (
                        "Description du médicament dans le catalogue..."
                    ),
                }
            ),

            "observations": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Observations...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["pharmacie"].queryset = (
            self.fields["pharmacie"]
            .queryset
            .filter(actif=True)
            .order_by("nom")
        )

        self.fields["medicament"].queryset = (
            self.fields["medicament"]
            .queryset
            .filter(actif=True)
            .order_by("nom")
        )