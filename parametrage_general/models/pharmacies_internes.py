from django.core.exceptions import ValidationError
from django.db import models

from .general import (
    TimeStampedModel,
    StatusModel,
    SlugModel,
    Site,
    UniteMedicale,
)


class PharmacieInterne(TimeStampedModel, StatusModel, SlugModel):

    # ============================================================
    # IDENTIFICATION
    # ============================================================

    nom = models.CharField(
        max_length=191,
        verbose_name="Nom de la pharmacie"
    )

    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Code pharmacie",
        help_text="Identifiant unique de la pharmacie interne."
    )

    # ============================================================
    # RATTACHEMENT
    # ============================================================

    site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        related_name="pharmacies_internes",
        verbose_name="Site"
    )

    unite_medicale = models.ForeignKey(
        UniteMedicale,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="pharmacies_internes",
        verbose_name="Unité médicale",
        help_text=(
            "Unité médicale à laquelle la pharmacie interne "
            "est rattachée, par exemple une infirmerie."
        )
    )

    # ============================================================
    # LOCALISATION
    # ============================================================

    localisation = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Localisation"
    )

    # ============================================================
    # CONTACT
    # ============================================================

    telephone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Téléphone"
    )

    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Adresse e-mail"
    )

    # ============================================================
    # RESPONSABLE
    # ============================================================

    nom_responsable = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Nom du responsable"
    )

    fonction_responsable = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Fonction du responsable"
    )

    telephone_responsable = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Téléphone du responsable"
    )

    email_responsable = models.EmailField(
        blank=True,
        null=True,
        verbose_name="E-mail du responsable"
    )

    # ============================================================
    # CONFIGURATION STOCK
    # ============================================================

    gestion_stock_active = models.BooleanField(
        default=True,
        verbose_name="Gestion du stock active"
    )

    gestion_lots_active = models.BooleanField(
        default=True,
        verbose_name="Gestion des lots active"
    )

    gestion_peremption_active = models.BooleanField(
        default=True,
        verbose_name="Gestion des péremptions active"
    )

    gestion_inventaire_active = models.BooleanField(
        default=True,
        verbose_name="Gestion des inventaires active"
    )

    gestion_transfert_active = models.BooleanField(
        default=True,
        verbose_name="Gestion des transferts active"
    )

    # ============================================================
    # DISPENSATION
    # ============================================================

    gestion_dispensation_active = models.BooleanField(
        default=True,
        verbose_name="Gestion de la dispensation active"
    )

    # ============================================================
    # VENTE / CLIENT
    # ============================================================

    gestion_vente_active = models.BooleanField(
        default=False,
        editable=False,
        verbose_name="Gestion des ventes active"
    )

    gestion_client_active = models.BooleanField(
        default=False,
        editable=False,
        verbose_name="Gestion des clients active"
    )

    # ============================================================
    # INFORMATIONS GENERALES
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
    # VALIDATION
    # ============================================================

    def clean(self):

        errors = {}

        # --------------------------------------------------------
        # Cohérence unité médicale / site
        # --------------------------------------------------------

        if self.unite_medicale_id and self.site_id:

            if self.unite_medicale.site_id != self.site_id:
                errors["unite_medicale"] = (
                    "L'unité médicale sélectionnée doit "
                    "appartenir au site choisi."
                )

        # --------------------------------------------------------
        # L'unité doit être adaptée à une pharmacie interne
        # --------------------------------------------------------

        if self.unite_medicale_id:

            types_autorises = {
                "pharmacie",
                "infirmerie",
                "autre",
            }

            if self.unite_medicale.type_unite not in types_autorises:
                errors["unite_medicale"] = (
                    "L'unité médicale sélectionnée n'est pas "
                    "compatible avec une pharmacie interne."
                )

        # --------------------------------------------------------
        # Une pharmacie interne ne gère pas les clients
        # --------------------------------------------------------

        if self.gestion_client_active:

            errors["gestion_client_active"] = (
                "Une pharmacie interne ne peut pas gérer "
                "les clients de pharmacie."
            )

        # --------------------------------------------------------
        # Une pharmacie interne ne fait pas de vente
        # --------------------------------------------------------

        if self.gestion_vente_active:

            errors["gestion_vente_active"] = (
                "Une pharmacie interne ne peut pas gérer "
                "les ventes."
            )

        if errors:
            raise ValidationError(errors)

    # ============================================================
    # SAVE
    # ============================================================

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = self.generate_unique_slug(
                self.nom,
                PharmacieInterne.objects
            )

        super().save(*args, **kwargs)

    # ============================================================
    # STRING
    # ============================================================

    def __str__(self):
        return f"{self.nom} ({self.code})"

    # ============================================================
    # META
    # ============================================================

    class Meta:

        db_table = "pharmacies_internes"

        verbose_name = "Pharmacie interne"

        verbose_name_plural = "Pharmacies internes"

        ordering = ["nom"]

        indexes = [
            models.Index(fields=["actif"]),
        ]