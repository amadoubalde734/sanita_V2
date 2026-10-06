from django.conf import settings
from django.db import models


class SortieStock(models.Model):

    STATUT_CHOICES = [
        ("brouillon", "Brouillon"),
        ("validee", "Validée"),
        ("annulee", "Annulée"),
    ]

    MOTIF_CHOICES = [
        ("vente", "Vente"),
        ("ordonnance", "Ordonnance"),
        ("dispensation", "Dispensation"),
        ("consommation_interne", "Consommation interne"),
        ("perte", "Perte"),
        ("peremption", "Péremption"),
        ("casse", "Casse"),
        ("ajustement", "Ajustement"),
        ("autre", "Autre"),
    ]

    reference = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Référence sortie"
    )

    depot = models.ForeignKey(
        "stock.DepotStock",
        on_delete=models.PROTECT,
        related_name="sorties",
        verbose_name="Dépôt"
    )

    client = models.ForeignKey(
        "stock.Client",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="sorties_stock",
        verbose_name="Client"
    )

    # Référence temporaire vers une future ordonnance.
    # Le modèle Ordonnance sera développé séparément.
    ordonnance_id = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name="ID Ordonnance"
    )

    date_sortie = models.DateTimeField(
        verbose_name="Date de sortie"
    )

    motif_sortie = models.CharField(
        max_length=30,
        choices=MOTIF_CHOICES,
        default="autre",
        verbose_name="Motif de sortie"
    )

    nom_medecin = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Médecin prescripteur"
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
        related_name="sorties_stock",
        verbose_name="Utilisateur"
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "stock_sorties"
        verbose_name = "Sortie de stock"
        verbose_name_plural = "Sorties de stock"
        ordering = ["-date_sortie", "-id"]

    def __str__(self):
        return self.reference


class LigneSortieStock(models.Model):

    sortie = models.ForeignKey(
        SortieStock,
        on_delete=models.CASCADE,
        related_name="lignes",
        verbose_name="Sortie"
    )

    medicament = models.ForeignKey(
        "stock.Medicament",
        on_delete=models.PROTECT,
        related_name="lignes_sorties",
        verbose_name="Médicament"
    )

    quantite = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Quantité"
    )

    prix_unitaire = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Prix unitaire"
    )

    montant = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
        verbose_name="Montant"
    )

    class Meta:
        db_table = "stock_lignes_sorties"
        verbose_name = "Ligne de sortie"
        verbose_name_plural = "Lignes de sortie"

    def __str__(self):
        return f"{self.sortie.reference} - {self.medicament}"


class LigneSortieLot(models.Model):

    ligne_sortie = models.ForeignKey(
        LigneSortieStock,
        on_delete=models.CASCADE,
        related_name="lots_sorties",
        verbose_name="Ligne de sortie"
    )

    lot = models.ForeignKey(
        "stock.LotMedicament",
        on_delete=models.PROTECT,
        related_name="lignes_sorties_lots",
        verbose_name="Lot"
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

    class Meta:
        db_table = "stock_lignes_sorties_lots"
        verbose_name = "Lot sorti"
        verbose_name_plural = "Lots sortis"

    def __str__(self):
        return (
            f"{self.ligne_sortie.sortie.reference} - "
            f"{self.lot} - "
            f"{self.quantite}"
        )