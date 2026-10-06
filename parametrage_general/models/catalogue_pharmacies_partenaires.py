from django.core.exceptions import ValidationError
from django.db import models

from .pharmacie_partenaire import PharmaciePartenaire
from stock.models.medicaments import Medicament


class CatalogueMedicamentPharmaciePartenaire(models.Model):

    # ============================================================
    # PHARMACIE / MEDICAMENT
    # ============================================================

    pharmacie = models.ForeignKey(
        PharmaciePartenaire,
        on_delete=models.PROTECT,
        related_name="catalogue_medicaments",
        verbose_name="Pharmacie partenaire"
    )

    medicament = models.ForeignKey(
        Medicament,
        on_delete=models.PROTECT,
        related_name="catalogues_pharmacies_partenaires",
        verbose_name="Médicament"
    )

    # ============================================================
    # IDENTIFICATION DANS LE CATALOGUE
    # ============================================================

    reference_interne = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Référence interne",
        help_text=(
            "Référence utilisée par la pharmacie pour ce médicament."
        )
    )

    nom_commercial = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Nom commercial",
        help_text=(
            "Nom commercial utilisé par la pharmacie, "
            "si différent du référentiel SANITA."
        )
    )

    # ============================================================
    # DISPONIBILITÉ
    # ============================================================

    disponible = models.BooleanField(
        default=True,
        verbose_name="Disponible"
    )

    sur_commande = models.BooleanField(
        default=False,
        verbose_name="Disponible sur commande"
    )

    # ============================================================
    # INFORMATIONS COMMERCIALES
    # ============================================================

    unite_vente = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Unité de vente",
        help_text=(
            "Exemple : boîte, flacon, tube, plaquette."
        )
    )

    conditionnement = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Conditionnement"
    )

    # ============================================================
    # CONFIGURATION
    # ============================================================

    accepte_ordonnance = models.BooleanField(
        default=True,
        verbose_name="Nécessite une ordonnance"
    )

    dispensation_active = models.BooleanField(
        default=True,
        verbose_name="Dispensation active"
    )

    actif = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )

    # ============================================================
    # INFORMATIONS COMPLÉMENTAIRES
    # ============================================================

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description"
    )

    observations = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observations"
    )

    # ============================================================
    # DATES
    # ============================================================

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    date_modification = models.DateTimeField(
        auto_now=True
    )

    # ============================================================
    # VALIDATION
    # ============================================================

    def clean(self):

        errors = {}

        if self.pharmacie_id and self.medicament_id:

            existe = (
                CatalogueMedicamentPharmaciePartenaire.objects
                .filter(
                    pharmacie_id=self.pharmacie_id,
                    medicament_id=self.medicament_id
                )
                .exclude(pk=self.pk)
                .exists()
            )

            if existe:
                errors["medicament"] = (
                    "Ce médicament existe déjà dans le catalogue "
                    "de cette pharmacie partenaire."
                )

        if errors:
            raise ValidationError(errors)

    # ============================================================
    # STRING
    # ============================================================

    def __str__(self):
        return f"{self.pharmacie.nom} - {self.medicament.nom}"

    # ============================================================
    # META
    # ============================================================

    class Meta:

        db_table = "catalogue_medicaments_pharmacies_partenaires"

        verbose_name = (
            "Médicament du catalogue partenaire"
        )

        verbose_name_plural = (
            "Médicaments des catalogues partenaires"
        )

        ordering = [
            "pharmacie__nom",
            "medicament__nom",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["pharmacie", "medicament"],
                name="unique_catalogue_pharmacie_medicament"
            )
        ]

        indexes = [
            models.Index(
                fields=["pharmacie", "actif"]
            ),
            models.Index(
                fields=["medicament", "actif"]
            ),
        ]