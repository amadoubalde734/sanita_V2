from django.db import models


class Fournisseur(models.Model):

    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Code fournisseur"
    )

    nom = models.CharField(
        max_length=255,
        verbose_name="Nom du fournisseur"
    )

    contact = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Contact"
    )

    adresse = models.TextField(
        blank=True,
        null=True,
        verbose_name="Adresse"
    )

    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="E-mail"
    )

    telephone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Téléphone"
    )

    numero_fiscal = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Numéro fiscal"
    )

    registre_commerce = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Registre de commerce"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description"
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
        db_table = "stock_fournisseurs"
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        ordering = ["nom"]

    def __str__(self):
        return self.nom