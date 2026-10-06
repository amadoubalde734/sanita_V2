from django.db import models


class LotMedicament(models.Model):

    STATUT_CHOICES = [
        ("actif", "Actif"),
        ("epuise", "Épuisé"),
        ("expire", "Expiré"),
        ("bloque", "Bloqué"),
        ("inactif", "Inactif"),
    ]

    medicament = models.ForeignKey(
        "stock.Medicament",
        on_delete=models.PROTECT,
        related_name="lots",
        verbose_name="Médicament"
    )

    depot = models.ForeignKey(
        "stock.DepotStock",
        on_delete=models.PROTECT,
        related_name="lots",
        verbose_name="Dépôt"
    )

    entree = models.ForeignKey(
        "stock.EntreeStock",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="lots",
        verbose_name="Entrée de stock"
    )

    numero_lot = models.CharField(
        max_length=100,
        verbose_name="Numéro de lot"
    )

    quantite_initiale = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Quantité initiale"
    )

    quantite_disponible = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Quantité disponible"
    )

    date_entree = models.DateField(
        verbose_name="Date d'entrée"
    )

    date_peremption = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date de péremption"
    )

    fournisseur = models.ForeignKey(
        "stock.Fournisseur",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="lots",
        verbose_name="Fournisseur"
    )

    prix_achat_unitaire = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Prix d'achat unitaire"
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default="actif",
        verbose_name="Statut"
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    date_modification = models.DateTimeField(
        auto_now=True
    )


    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True, verbose_name="Slug")
    class Meta:
        db_table = "stock_lots_medicaments"
        verbose_name = "Lot de médicament"
        verbose_name_plural = "Lots de médicaments"
        ordering = ["date_peremption", "numero_lot"]

        indexes = [
            models.Index(
                fields=["depot", "medicament"]
            ),
            models.Index(
                fields=["date_peremption"]
            ),
            models.Index(
                fields=["numero_lot"]
            ),
        ]

    def __str__(self):
        return f"{self.medicament} - Lot {self.numero_lot}"