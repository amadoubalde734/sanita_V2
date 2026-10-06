from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from stock.models.medicaments import (
    FamilleMedicament,
    Medicament,
)


# ============================================================
# FAMILLE DE MÉDICAMENT
# ============================================================

class FamilleMedicamentForm(forms.ModelForm):

    class Meta:
        model = FamilleMedicament

        fields = [
            "code",
            "nom",
            "description",
            "actif",
            "statut",
        ]

        widgets = {
            "code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex. ANT",
                }
            ),

            "nom": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nom de la famille",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Description de la famille...",
                }
            ),

            "actif": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "statut": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def clean_code(self):
        code = self.cleaned_data.get("code")

        if code:
            code = code.strip().upper()

        return code

    def clean_nom(self):
        nom = self.cleaned_data.get("nom")

        if nom:
            nom = nom.strip()

        return nom

    def save(self, commit=True):
        instance = super().save(commit=False)

        if not instance.slug:
            instance.slug = slugify(
                f"{instance.code}-{instance.nom}"
            )

        if commit:
            instance.save()

        return instance


# ============================================================
# MÉDICAMENT
# ============================================================

class MedicamentForm(forms.ModelForm):

    class Meta:
        model = Medicament

        fields = [
            "code",
            "code_cip",
            "code_barre",
            "nom",
            "famille",
            "description",
            "forme",
            "dosage",
            "unite",
            "contenu",
            "seuil",
            "prix_reference",
            "dernier_prix_achat",
            "actif",
            "statut",
        ]

        widgets = {

            # ------------------------------------------------
            # IDENTIFICATION
            # ------------------------------------------------

            "code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Généré automatiquement",
                    "readonly": "readonly",
                }
            ),

            "code_cip": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Code CIP",
                }
            ),

            "code_barre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Code-barres",
                }
            ),

            "nom": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nom du médicament",
                }
            ),

            # ------------------------------------------------
            # CLASSIFICATION
            # ------------------------------------------------

            "famille": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "forme": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            # ------------------------------------------------
            # CARACTÉRISTIQUES
            # ------------------------------------------------

            "dosage": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex. 500 mg",
                }
            ),

            "unite": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex. comprimé, ml, mg...",
                }
            ),

            "contenu": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex. 20 comprimés",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Description du médicament...",
                }
            ),

            # ------------------------------------------------
            # STOCK / PRIX
            # ------------------------------------------------

            "seuil": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "0",
                }
            ),

            "prix_reference": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "0",
                }
            ),

            "dernier_prix_achat": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "0",
                }
            ),

            # ------------------------------------------------
            # ÉTAT
            # ------------------------------------------------

            "actif": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "statut": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

        labels = {
            "code": "Référence médicament",
            "code_cip": "Code CIP",
            "code_barre": "Code-barres",
            "nom": "Médicament",
            "famille": "Famille",
            "forme": "Forme",
            "dosage": "Dosage",
            "unite": "Unité",
            "contenu": "Contenu",
            "seuil": "Seuil d'alerte",
            "prix_reference": "Prix de référence",
            "dernier_prix_achat": "Dernier prix d'achat",
            "description": "Description",
            "actif": "Actif",
            "statut": "Statut",
        }

        help_texts = {
            "code": (
                "Référence générée automatiquement à partir "
                "du code de la famille."
            ),
            "code_cip": "Code CIP du médicament, s'il existe.",
            "code_barre": (
                "Code-barres utilisé pour l'identification du produit."
            ),
            "dosage": "Ex. 500 mg, 1 g, 10 mg/ml...",
            "unite": "Unité de référence du médicament.",
            "contenu": "Contenu ou conditionnement de référence.",
            "seuil": (
                "Seuil à partir duquel une alerte de stock "
                "peut être générée."
            ),
            "prix_reference": "Prix de référence du médicament.",
            "dernier_prix_achat": "Dernier prix d'achat enregistré.",
        }

    # ========================================================
    # INITIALISATION
    # ========================================================

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["code"].required = False

        self.fields["famille"].queryset = (
            FamilleMedicament.objects
            .filter(
                actif=True,
                statut="actif",
            )
            .order_by("nom")
        )

        self.fields["famille"].empty_label = (
            "Sélectionner une famille"
        )

        self.fields["forme"].empty_label = (
            "Sélectionner une forme"
        )

    # ========================================================
    # CODE
    # ========================================================

    def clean_code(self):
        code = self.cleaned_data.get("code")

        if code:
            code = code.strip().upper()

        return code

    # ========================================================
    # CIP
    # ========================================================

    def clean_code_cip(self):
        code_cip = self.cleaned_data.get("code_cip")

        if code_cip:
            code_cip = code_cip.strip()

        return code_cip

    # ========================================================
    # CODE-BARRES
    # ========================================================

    def clean_code_barre(self):
        code_barre = self.cleaned_data.get("code_barre")

        if code_barre:
            code_barre = code_barre.strip()

        return code_barre

    # ========================================================
    # NOM
    # ========================================================

    def clean_nom(self):
        nom = self.cleaned_data.get("nom")

        if nom:
            nom = nom.strip()

        if not nom:
            raise ValidationError(
                "Le nom du médicament est obligatoire."
            )

        return nom

    # ========================================================
    # FAMILLE
    # ========================================================

    def clean_famille(self):
        famille = self.cleaned_data.get("famille")

        if not famille:
            raise ValidationError(
                "La famille du médicament est obligatoire."
            )

        if not famille.actif or famille.statut != "actif":
            raise ValidationError(
                "La famille sélectionnée n'est pas active."
            )

        return famille

    # ========================================================
    # SEUIL
    # ========================================================

    def clean_seuil(self):
        seuil = self.cleaned_data.get("seuil")

        if seuil is not None and seuil < Decimal("0"):
            raise ValidationError(
                "Le seuil d'alerte ne peut pas être négatif."
            )

        return seuil

    # ========================================================
    # PRIX DE RÉFÉRENCE
    # ========================================================

    def clean_prix_reference(self):
        prix = self.cleaned_data.get("prix_reference")

        if prix is not None and prix < Decimal("0"):
            raise ValidationError(
                "Le prix de référence ne peut pas être négatif."
            )

        return prix

    # ========================================================
    # DERNIER PRIX D'ACHAT
    # ========================================================

    def clean_dernier_prix_achat(self):
        prix = self.cleaned_data.get("dernier_prix_achat")

        if prix is not None and prix < Decimal("0"):
            raise ValidationError(
                "Le dernier prix d'achat ne peut pas être négatif."
            )

        return prix

    # ========================================================
    # VALIDATION GLOBALE
    # ========================================================

    def clean(self):
        cleaned_data = super().clean()

        prix_reference = cleaned_data.get(
            "prix_reference"
        )

        dernier_prix_achat = cleaned_data.get(
            "dernier_prix_achat"
        )

        if (
            prix_reference is not None
            and dernier_prix_achat is not None
        ):
            if (
                prix_reference > 0
                and dernier_prix_achat > 0
            ):
                pass

        return cleaned_data

    # ========================================================
    # GÉNÉRATION DE LA RÉFÉRENCE
    # ========================================================

    def _generer_reference(self, famille):
        """
        Génère la prochaine référence du médicament
        à partir du code de la famille.

        Exemple :
            ANT-00001
            ANT-00002
            ANT-00003
        """

        prefixe = famille.code.strip().upper()

        medicaments = (
            Medicament.objects
            .filter(
                famille=famille,
                code__startswith=f"{prefixe}-",
            )
            .values_list("code", flat=True)
        )

        dernier_numero = 0

        for code in medicaments:
            try:
                numero = int(
                    code.rsplit("-", 1)[1]
                )
            except (ValueError, IndexError):
                continue

            if numero > dernier_numero:
                dernier_numero = numero

        numero_suivant = dernier_numero + 1

        return f"{prefixe}-{numero_suivant:05d}"

    # ========================================================
    # SAVE
    # ========================================================

    def save(self, commit=True):
        instance = super().save(commit=False)

        # ----------------------------------------------------
        # NOUVEAU MÉDICAMENT
        # ----------------------------------------------------
        if not instance.pk:
            famille = instance.famille

            if not famille:
                raise ValidationError(
                    "Une famille est obligatoire pour générer "
                    "la référence du médicament."
                )

            instance.code = self._generer_reference(
                famille
            )

        # ----------------------------------------------------
        # SLUG
        # ----------------------------------------------------
        if not instance.slug:
            base_slug = slugify(
                f"{instance.code}-{instance.nom}"
            )

            slug = base_slug
            compteur = 2

            while Medicament.objects.filter(
                slug=slug
            ).exclude(
                pk=instance.pk
            ).exists():

                slug = f"{base_slug}-{compteur}"
                compteur += 1

            instance.slug = slug

        # ----------------------------------------------------
        # STATUT
        # ----------------------------------------------------
        if not instance.statut:
            instance.statut = "actif"

        if commit:
            instance.save()

        return instance

