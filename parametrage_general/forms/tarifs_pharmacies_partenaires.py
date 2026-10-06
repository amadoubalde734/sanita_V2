from django import forms

from ..models.pharmacie_partenaire import PharmaciePartenaire
from ..models.catalogue_pharmacies_partenaires import (
    CatalogueMedicamentPharmaciePartenaire,
)
from ..models.tarifs_pharmacies_partenaires import (
    TarifMedicamentPharmaciePartenaire,
)


class TarifMedicamentPharmaciePartenaireForm(forms.ModelForm):

    # ============================================================
    # PHARMACIE PARTENAIRE
    # Champ de travail du formulaire.
    # Il ne correspond PAS à un champ du modèle Tarif.
    # ============================================================

    pharmacie = forms.ModelChoiceField(
        queryset=PharmaciePartenaire.objects.none(),
        required=True,
        label="Pharmacie partenaire",
        empty_label="Sélectionner une pharmacie partenaire",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_pharmacie_tarif",
            }
        ),
    )

    class Meta:

        model = TarifMedicamentPharmaciePartenaire

        fields = [
            "pharmacie",
            "catalogue",
            "reference",
            "prix",
            "devise",
            "date_debut",
            "date_fin",
            "actif",
            "motif",
            "commentaire",
        ]

        labels = {
            "pharmacie": "Pharmacie partenaire",
            "catalogue": "Médicament du catalogue",
            "reference": "Référence tarifaire",
            "prix": "Prix",
            "devise": "Devise",
            "date_debut": "Début de validité",
            "date_fin": "Fin de validité",
            "actif": "Tarif actif",
            "motif": "Motif",
            "commentaire": "Commentaire",
        }

        widgets = {

            "catalogue": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_catalogue_tarif",
                }
            ),

            "reference": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex. TAR-PHA-000001",
                }
            ),

            "prix": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex. 25000",
                    "step": "0.01",
                    "min": "0.01",
                }
            ),

            "devise": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex. GNF",
                    "maxlength": "10",
                }
            ),

            "date_debut": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "date_fin": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "actif": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "motif": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "commentaire": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": (
                        "Informations complémentaires "
                        "sur ce tarif..."
                    ),
                }
            ),
        }

    # ============================================================
    # INITIALISATION
    # ============================================================

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # --------------------------------------------------------
        # PHARMACIES PARTENAIRES DISPONIBLES
        # --------------------------------------------------------

        self.fields["pharmacie"].queryset = (
            PharmaciePartenaire.objects
            .filter(
                actif=True,
                gestion_catalogue_active=True,
                gestion_tarifs_active=True,
            )
            .order_by("nom")
        )

        # --------------------------------------------------------
        # CATALOGUE
        #
        # Par défaut aucun catalogue n'est affiché.
        # Il sera chargé en fonction de la pharmacie sélectionnée.
        # --------------------------------------------------------

        self.fields["catalogue"].queryset = (
            CatalogueMedicamentPharmaciePartenaire.objects.none()
        )

        # --------------------------------------------------------
        # MODIFICATION
        #
        # Lorsqu'on ouvre un tarif existant, on récupère sa pharmacie
        # et on limite le catalogue à cette pharmacie.
        # --------------------------------------------------------

        if self.instance.pk and self.instance.catalogue_id:

            pharmacie_id = (
                self.instance.catalogue.pharmacie_id
            )

            self.fields["pharmacie"].initial = pharmacie_id

            self.fields["catalogue"].queryset = (
                CatalogueMedicamentPharmaciePartenaire.objects
                .select_related(
                    "pharmacie",
                    "medicament",
                )
                .filter(
                    pharmacie_id=pharmacie_id,
                    actif=True,
                )
                .order_by(
                    "medicament__nom",
                )
            )

        # --------------------------------------------------------
        # VALEUR PAR DÉFAUT DE LA DEVISE
        # --------------------------------------------------------

        if not self.instance.pk:
            self.fields["devise"].initial = "GNF"

    # ============================================================
    # LIBELLÉ DU CATALOGUE
    # ============================================================

    @staticmethod
    def _libelle_catalogue(catalogue):

        medicament = catalogue.medicament.nom

        if catalogue.conditionnement:

            return (
                f"{medicament} — "
                f"{catalogue.conditionnement}"
            )

        return medicament

    # ============================================================
    # VALIDATION RÉFÉRENCE
    # ============================================================

    def clean_reference(self):

        reference = self.cleaned_data.get(
            "reference"
        )

        if reference:
            reference = reference.strip().upper()

        return reference

    # ============================================================
    # VALIDATION DEVISE
    # ============================================================

    def clean_devise(self):

        devise = self.cleaned_data.get(
            "devise"
        )

        if devise:
            devise = devise.strip().upper()

        return devise

    # ============================================================
    # VALIDATION GLOBALE
    # ============================================================

    def clean(self):

        cleaned_data = super().clean()

        pharmacie = cleaned_data.get(
            "pharmacie"
        )

        catalogue = cleaned_data.get(
            "catalogue"
        )

        actif = cleaned_data.get(
            "actif"
        )

        # --------------------------------------------------------
        # Vérification pharmacie
        # --------------------------------------------------------

        if pharmacie:

            if not pharmacie.actif:

                self.add_error(
                    "pharmacie",
                    (
                        "Cette pharmacie partenaire "
                        "est inactive."
                    ),
                )

            if not pharmacie.gestion_tarifs_active:

                self.add_error(
                    "pharmacie",
                    (
                        "La gestion des tarifs est désactivée "
                        "pour cette pharmacie partenaire."
                    ),
                )

        # --------------------------------------------------------
        # Vérification catalogue
        # --------------------------------------------------------

        if catalogue:

            if not catalogue.actif:

                self.add_error(
                    "catalogue",
                    (
                        "Le médicament sélectionné est "
                        "désactivé dans le catalogue partenaire."
                    ),
                )

            if actif and not catalogue.dispensation_active:

                self.add_error(
                    "catalogue",
                    (
                        "La dispensation est désactivée "
                        "pour ce médicament dans le catalogue."
                    ),
                )

            # ----------------------------------------------------
            # Vérifier que le catalogue appartient bien
            # à la pharmacie sélectionnée.
            # ----------------------------------------------------

            if pharmacie:

                if catalogue.pharmacie_id != pharmacie.pk:

                    self.add_error(
                        "catalogue",
                        (
                            "Le médicament sélectionné "
                            "n'appartient pas à la pharmacie "
                            "partenaire choisie."
                        ),
                    )

        # --------------------------------------------------------
        # Une pharmacie est obligatoire avant le catalogue.
        # --------------------------------------------------------

        if pharmacie and not catalogue:

            self.add_error(
                "catalogue",
                (
                    "Sélectionnez un médicament dans le "
                    "catalogue de cette pharmacie partenaire."
                ),
            )

        return cleaned_data