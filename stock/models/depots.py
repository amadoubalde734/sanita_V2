from django.db import models


class DepotStock(models.Model):

    pharmacie = models.ForeignKey(
        "parametrage_general.Pharmacie",
        on_delete=models.PROTECT,
        related_name="depots_stock",
        verbose_name="Pharmacie"
    )

    code = models.CharField(
        max_length=50,
        verbose_name="Code dépôt"
    )

    nom = models.CharField(
        max_length=150,
        verbose_name="Nom du dépôt"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description"
    )

    lieu = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Lieu"
    )

    est_principal = models.BooleanField(
        default=False,
        verbose_name="Dépôt principal"
    )

    actif = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    date_modification = models.DateTimeField(
        auto_now=True
    )


    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True, verbose_name="Slug")
    statut = models.CharField(max_length=20, default="actif", verbose_name="Statut")
    class Meta:
        db_table = "stock_depots"
        verbose_name = "Dépôt de stock"
        verbose_name_plural = "Dépôts de stock"
        ordering = ["nom"]

        constraints = [
            models.UniqueConstraint(
                fields=["pharmacie", "code"],
                name="unique_depot_pharmacie_code"
            )
        ]

    def __str__(self):
        return f"{self.nom} - {self.pharmacie}"