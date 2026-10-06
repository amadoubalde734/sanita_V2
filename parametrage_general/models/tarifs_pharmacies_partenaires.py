from django.core.exceptions import ValidationError
from django.db import models

from .catalogue_pharmacies_partenaires import (
    CatalogueMedicamentPharmaciePartenaire,
)


class TarifMedicamentPharmaciePartenaire(models.Model):

    # ============================================================
    # RÉFÉRENCE TARIFAIRE
    # ============================================================

    reference = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Référence tarifaire",
        help_text=(
            "Référence unique permettant d'identifier le tarif."
        ),
    )

    # ============================================================
    # CATALOGUE
    # ============================================================

    catalogue = models.ForeignKey(
        CatalogueMedicamentPharmaciePartenaire,
        on_delete=models.PROTECT,
        related_name="tarifs",
        verbose_name="Médicament du catalogue",
    )

    # ============================================================
    # TARIFICATION
    # ============================================================

    prix = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Prix",
        help_text=(
            "Prix appliqué par la pharmacie partenaire "
            "pour le médicament et son conditionnement "
            "définis dans le catalogue."
        ),
    )

    devise = models.CharField(
        max_length=10,
        default="GNF",
        verbose_name="Devise",
        help_text="Devise dans laquelle le tarif est exprimé.",
    )

    # ============================================================
    # VALIDITÉ DU TARIF
    # ============================================================

    date_debut = models.DateField(
        verbose_name="Date de début de validité",
    )

    date_fin = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date de fin de validité",
        help_text=(
            "Laisser vide si le tarif reste valable "
            "jusqu'à nouvel ordre."
        ),
    )

    # ============================================================
    # ÉTAT
    # ============================================================

    actif = models.BooleanField(
        default=True,
        verbose_name="Tarif actif",
    )

    # ============================================================
    # MOTIF DE MODIFICATION
    # ============================================================

    MOTIF_CHOICES = [
        (
            "creation",
            "Création du tarif",
        ),
        (
            "revision",
            "Révision tarifaire",
        ),
        (
            "changement_conditionnement",
            "Changement de conditionnement",
        ),
        (
            "modification_prix_pharmacie",
            "Modification du prix par la pharmacie",
        ),
        (
            "renouvellement",
            "Renouvellement du tarif",
        ),
        (
            "autre",
            "Autre",
        ),
    ]

    motif = models.CharField(
        max_length=50,
        choices=MOTIF_CHOICES,
        default="creation",
        verbose_name="Motif",
    )

    # ============================================================
    # INFORMATIONS COMPLÉMENTAIRES
    # ============================================================

    commentaire = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaire",
    )

    # ============================================================
    # DATES SYSTÈME
    # ============================================================

    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création",
    )

    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification",
    )

    # ============================================================
    # VALIDATION
    # ============================================================

    def clean(self):

        errors = {}

        # --------------------------------------------------------
        # Prix
        # --------------------------------------------------------

        if self.prix is not None and self.prix <= 0:
            errors["prix"] = (
                "Le prix doit être strictement supérieur à zéro."
            )

        # --------------------------------------------------------
        # Devise
        # --------------------------------------------------------

        if self.devise:
            self.devise = self.devise.strip().upper()

            if not self.devise:
                errors["devise"] = (
                    "La devise est obligatoire."
                )

        # --------------------------------------------------------
        # Dates
        # --------------------------------------------------------

        if self.date_debut and self.date_fin:

            if self.date_fin < self.date_debut:
                errors["date_fin"] = (
                    "La date de fin doit être postérieure "
                    "ou égale à la date de début."
                )

        # --------------------------------------------------------
        # Catalogue obligatoire
        # --------------------------------------------------------

        if not self.catalogue_id:
            errors["catalogue"] = (
                "Le médicament du catalogue est obligatoire."
            )

        # --------------------------------------------------------
        # Aucun chevauchement de périodes
        # --------------------------------------------------------

        if (
            self.catalogue_id
            and self.date_debut
        ):

            tarifs_existants = (
                TarifMedicamentPharmaciePartenaire.objects
                .filter(
                    catalogue_id=self.catalogue_id,
                )
                .exclude(pk=self.pk)
            )

            for tarif in tarifs_existants:

                # Tarif sans date de fin
                if tarif.date_fin is None:

                    chevauchement = (
                        self.date_fin is None
                        or self.date_debut <= tarif.date_fin
                    )

                else:

                    if self.date_fin is None:

                        chevauchement = (
                            self.date_debut <= tarif.date_fin
                        )

                    else:

                        chevauchement = (
                            self.date_debut <= tarif.date_fin
                            and self.date_fin >= tarif.date_debut
                        )

                if chevauchement:

                    errors["date_debut"] = (
                        "La période de validité de ce tarif "
                        "chevauche celle d'un autre tarif "
                        "pour ce médicament du catalogue."
                    )

                    break

        if errors:
            raise ValidationError(errors)

    # ============================================================
    # SAVE
    # ============================================================

    def save(self, *args, **kwargs):

        if self.devise:
            self.devise = self.devise.strip().upper()

        super().save(*args, **kwargs)

    # ============================================================
    # STRING
    # ============================================================

    def __str__(self):

        return (
            f"{self.catalogue.pharmacie.nom} - "
            f"{self.catalogue.medicament.nom} - "
            f"{self.prix} {self.devise}"
        )

    # ============================================================
    # META
    # ============================================================

    class Meta:

        db_table = (
            "tarifs_medicaments_pharmacies_partenaires"
        )

        verbose_name = (
            "Tarif de médicament partenaire"
        )

        verbose_name_plural = (
            "Tarifs des médicaments partenaires"
        )

        ordering = [
            "catalogue__pharmacie__nom",
            "catalogue__medicament__nom",
            "-date_debut",
        ]

        indexes = [

            models.Index(
                fields=[
                    "catalogue",
                    "actif",
                ]
            ),

            models.Index(
                fields=[
                    "date_debut",
                    "date_fin",
                ]
            ),

            models.Index(
                fields=[
                    "actif",
                ]
            ),

            models.Index(
                fields=[
                    "devise",
                ]
            ),
        ]