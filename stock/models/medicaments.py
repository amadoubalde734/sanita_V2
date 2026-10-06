from django.db import models
from django.utils.text import slugify


class FamilleMedicament(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Code"
    )

    nom = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nom"
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

    slug = models.SlugField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Slug"
    )

    statut = models.CharField(
        max_length=20,
        default="actif",
        verbose_name="Statut"
    )

    class Meta:
        db_table = "stock_familles_medicaments"
        verbose_name = "Famille de médicament"
        verbose_name_plural = "Familles de médicaments"
        ordering = ["nom"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.nom}"


class Medicament(models.Model):

    FORME_CHOICES = [
        ("comprime", "Comprimé"),
        ("gelule", "Gélule"),
        ("sirop", "Sirop"),
        ("injectable", "Injectable"),
        ("pommade", "Pommade"),
        ("creme", "Crème"),
        ("solution", "Solution"),
        ("suspension", "Suspension"),
        ("suppositoire", "Suppositoire"),
        ("gouttes", "Gouttes"),
        ("autre", "Autre"),
    ]

    # Référence interne SANITA.
    # Elle sera générée automatiquement à partir du code de la famille.
    # Exemple : ANT-00001
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Référence médicament"
    )

    code_cip = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_index=True,
        verbose_name="Code CIP"
    )

    code_barre = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_index=True,
        verbose_name="Code-barres"
    )

    nom = models.CharField(
        max_length=255,
        verbose_name="Médicament"
    )

    famille = models.ForeignKey(
        FamilleMedicament,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="medicaments",
        verbose_name="Famille"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description"
    )

    forme = models.CharField(
        max_length=50,
        choices=FORME_CHOICES,
        blank=True,
        null=True,
        verbose_name="Forme"
    )

    dosage = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Dosage"
    )

    unite = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Unité"
    )

    contenu = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Contenu"
    )

    seuil = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
        verbose_name="Seuil d'alerte"
    )

    prix_reference = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Prix de référence"
    )

    dernier_prix_achat = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Dernier prix d'achat"
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

    slug = models.SlugField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Slug"
    )

    statut = models.CharField(
        max_length=20,
        default="actif",
        verbose_name="Statut"
    )

    class Meta:
        db_table = "stock_medicaments"
        verbose_name = "Médicament"
        verbose_name_plural = "Médicaments"
        ordering = ["nom"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

