from django.conf import settings
from django.db import models


class MouvementStock(models.Model):

    TYPE_MOUVEMENT_CHOICES = [
        ("entree", "Entrée"),
        ("sortie", "Sortie"),
        ("transfert_depart", "Transfert départ"),
        ("transfert_arrivee", "Transfert arrivée"),
        ("ajustement", "Ajustement"),
    ]

    STATUT_CHOICES = [
        ("valide", "Validé"),
        ("annule", "Annulé"),
    ]

    depot = models.ForeignKey(
        "stock.DepotStock",
        on_delete=models.PROTECT,
        related_name="mouvements",
        verbose_name="Dépôt"
    )

    medicament = models.ForeignKey(
        "stock.Medicament",
        on_delete=models.PROTECT,
        related_name="mouvements",
        verbose_name="Médicament"
    )

    lot = models.ForeignKey(
        "stock.LotMedicament",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="mouvements",
        verbose_name="Lot"
    )

    type_mouvement = models.CharField(
        max_length=30,
        choices=TYPE_MOUVEMENT_CHOICES,
        verbose_name="Type de mouvement"
    )

    quantite = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Quantité mouvement"
    )

    quantite_avant = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Quantité avant"
    )

    quantite_apres = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Quantité après"
    )

    reference_operation = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Référence opération"
    )

    motif = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Motif"
    )

    commentaire = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaire"
    )

    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="mouvements_stock",
        verbose_name="Utilisateur"
    )

    date_mouvement = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date du mouvement"
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default="valide",
        verbose_name="Statut"
    )


    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True, verbose_name="Slug")
    class Meta:
        db_table = "stock_mouvements"
        verbose_name = "Mouvement de stock"
        verbose_name_plural = "Mouvements de stock"
        ordering = ["-date_mouvement"]

        indexes = [
            models.Index(
                fields=["depot", "medicament"]
            ),
            models.Index(
                fields=["type_mouvement"]
            ),
            models.Index(
                fields=["date_mouvement"]
            ),
            models.Index(
                fields=["reference_operation"]
            ),
        ]

    def __str__(self):
        return (
            f"{self.type_mouvement} - "
            f"{self.medicament} - "
            f"{self.quantite}"
        )