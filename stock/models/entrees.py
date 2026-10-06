from django.conf import settings
from django.db import models


class EntreeStock(models.Model):

    STATUT_CHOICES = [
        ("brouillon", "Brouillon"),
        ("validee", "Validée"),
        ("annulee", "Annulée"),
    ]

    reference = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Référence"
    )

    depot = models.ForeignKey(
        "stock.DepotStock",
        on_delete=models.PROTECT,
        related_name="entrees",
        verbose_name="Dépôt"
    )

    fournisseur = models.ForeignKey(
        "stock.Fournisseur",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="entrees",
        verbose_name="Fournisseur"
    )

    date_entree = models.DateField(
        verbose_name="Date d'entrée"
    )

    origine = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Origine"
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

    utilisateur_creation = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="entrees_stock_creees",
        verbose_name="Créé par"
    )

    date_validation = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Date de validation"
    )

    utilisateur_validation = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="entrees_stock_validees",
        verbose_name="Validé par"
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    date_modification = models.DateTimeField(
        auto_now=True
    )


    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True, verbose_name="Slug")
    class Meta:
        db_table = "stock_entrees"
        verbose_name = "Entrée de stock"
        verbose_name_plural = "Entrées de stock"
        ordering = ["-date_entree", "-id"]

    def __str__(self):
        return self.reference


class LigneEntreeStock(models.Model):

    entree = models.ForeignKey(
        EntreeStock,
        on_delete=models.CASCADE,
        related_name="lignes",
        verbose_name="Entrée"
    )

    medicament = models.ForeignKey(
        "stock.Medicament",
        on_delete=models.PROTECT,
        related_name="lignes_entrees",
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

    montant_ht = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
        verbose_name="Montant HT"
    )

    numero_lot = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Numéro de lot"
    )

    date_peremption = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date de péremption"
    )

    lot = models.ForeignKey(
        "stock.LotMedicament",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ligne_entree",
        verbose_name="Lot"
    )


    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True, verbose_name="Slug")
    statut = models.CharField(max_length=20, default="actif", verbose_name="Statut")
    class Meta:
        db_table = "stock_lignes_entrees"
        verbose_name = "Ligne d'entrée"
        verbose_name_plural = "Lignes d'entrée"

    def __str__(self):
        return f"{self.entree.reference} - {self.medicament}"