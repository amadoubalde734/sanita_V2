from django.db import models


class Stock(models.Model):

    depot = models.ForeignKey(
        "stock.DepotStock",
        on_delete=models.PROTECT,
        related_name="stocks",
        verbose_name="Dépôt"
    )

    medicament = models.ForeignKey(
        "stock.Medicament",
        on_delete=models.PROTECT,
        related_name="stocks",
        verbose_name="Médicament"
    )

    quantite_disponible = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Quantité disponible"
    )

    quantite_reservee = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Quantité réservée"
    )

    date_mise_a_jour = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière mise à jour"
    )

    actif = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )


    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True, verbose_name="Slug")
    statut = models.CharField(max_length=20, default="actif", verbose_name="Statut")
    class Meta:
        db_table = "stock_disponibles"
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        ordering = ["medicament__nom"]

        constraints = [
            models.UniqueConstraint(
                fields=["depot", "medicament"],
                name="unique_stock_depot_medicament"
            )
        ]

    @property
    def quantite_reelle_disponible(self):
        return self.quantite_disponible - self.quantite_reservee

    def __str__(self):
        return f"{self.medicament} - {self.depot}"