from django.conf import settings
from django.db import models


class InventaireStock(models.Model):

    STATUT_CHOICES = [
        ("brouillon", "Brouillon"),
        ("valide", "Validé"),
        ("annule", "Annulé"),
    ]

    reference = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Référence"
    )

    depot = models.ForeignKey(
        "stock.DepotStock",
        on_delete=models.PROTECT,
        related_name="inventaires",
        verbose_name="Dépôt"
    )

    date_inventaire = models.DateTimeField(
        verbose_name="Date d'inventaire"
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
        related_name="inventaires_stock",
        verbose_name="Utilisateur"
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )


    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True, verbose_name="Slug")
    class Meta:
        db_table = "stock_inventaires"
        verbose_name = "Inventaire de stock"
        verbose_name_plural = "Inventaires de stock"
        ordering = ["-date_inventaire"]

    def __str__(self):
        return self.reference


class LigneInventaireStock(models.Model):

    inventaire = models.ForeignKey(
        InventaireStock,
        on_delete=models.CASCADE,
        related_name="lignes",
        verbose_name="Inventaire"
    )

    medicament = models.ForeignKey(
        "stock.Medicament",
        on_delete=models.PROTECT,
        related_name="lignes_inventaires",
        verbose_name="Médicament"
    )

    quantite_theorique = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Quantité théorique"
    )

    quantite_comptee = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Quantité comptée"
    )

    ecart = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Écart"
    )

    commentaire = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaire"
    )


    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True, verbose_name="Slug")
    statut = models.CharField(max_length=20, default="actif", verbose_name="Statut")
    class Meta:
        db_table = "stock_lignes_inventaires"
        verbose_name = "Ligne d'inventaire"
        verbose_name_plural = "Lignes d'inventaire"

        constraints = [
            models.UniqueConstraint(
                fields=["inventaire", "medicament"],
                name="unique_ligne_inventaire_medicament"
            )
        ]

    def __str__(self):
        return f"{self.inventaire.reference} - {self.medicament}"