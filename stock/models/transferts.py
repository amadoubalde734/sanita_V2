from django.conf import settings
from django.db import models


class TransfertStock(models.Model):

    STATUT_CHOICES = [
        ("brouillon", "Brouillon"),
        ("valide", "Validé"),
        ("annule", "Annulé"),
        ("recu", "Reçu"),
    ]

    reference = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Référence transfert"
    )

    depot_depart = models.ForeignKey(
        "stock.DepotStock",
        on_delete=models.PROTECT,
        related_name="transferts_depart",
        verbose_name="Dépôt de départ"
    )

    depot_arrivee = models.ForeignKey(
        "stock.DepotStock",
        on_delete=models.PROTECT,
        related_name="transferts_arrivee",
        verbose_name="Dépôt d'arrivée"
    )

    date_transfert = models.DateTimeField(
        verbose_name="Date du transfert"
    )

    commentaire = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaire"
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default="brouillon",
        verbose_name="Statut"
    )

    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="transferts_stock",
        verbose_name="Utilisateur"
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )


    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True, verbose_name="Slug")
    class Meta:
        db_table = "stock_transferts"
        verbose_name = "Transfert de stock"
        verbose_name_plural = "Transferts de stock"
        ordering = ["-date_transfert", "-id"]

    def clean(self):
        from django.core.exceptions import ValidationError

        if (
            self.depot_depart_id
            and self.depot_arrivee_id
            and self.depot_depart_id == self.depot_arrivee_id
        ):
            raise ValidationError(
                "Le dépôt de départ et le dépôt d'arrivée doivent être différents."
            )

    def __str__(self):
        return self.reference


class LigneTransfertStock(models.Model):

    transfert = models.ForeignKey(
        TransfertStock,
        on_delete=models.CASCADE,
        related_name="lignes",
        verbose_name="Transfert"
    )

    medicament = models.ForeignKey(
        "stock.Medicament",
        on_delete=models.PROTECT,
        related_name="lignes_transferts",
        verbose_name="Médicament"
    )

    quantite = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Quantité"
    )


    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True, verbose_name="Slug")
    statut = models.CharField(max_length=20, default="actif", verbose_name="Statut")
    class Meta:
        db_table = "stock_lignes_transferts"
        verbose_name = "Ligne de transfert"
        verbose_name_plural = "Lignes de transfert"

    def __str__(self):
        return f"{self.transfert.reference} - {self.medicament}"


class LigneTransfertLot(models.Model):

    ligne_transfert = models.ForeignKey(
        LigneTransfertStock,
        on_delete=models.CASCADE,
        related_name="lots_transferts",
        verbose_name="Ligne de transfert"
    )

    lot_source = models.ForeignKey(
        "stock.LotMedicament",
        on_delete=models.PROTECT,
        related_name="transferts_lot_source",
        verbose_name="Lot source"
    )

    lot_destination = models.ForeignKey(
        "stock.LotMedicament",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="transferts_lot_destination",
        verbose_name="Lot destination"
    )

    quantite = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Quantité"
    )

    date_mouvement = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date du mouvement"
    )


    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True, verbose_name="Slug")
    statut = models.CharField(max_length=20, default="actif", verbose_name="Statut")
    class Meta:
        db_table = "stock_lignes_transferts_lots"
        verbose_name = "Lot transféré"
        verbose_name_plural = "Lots transférés"