from django.db import models

from .general import ConfigurationEtablissement


class CategorieActe(models.Model):
    nom = models.CharField(
        max_length=150,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    actif = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = 'parametrage_categories_actes'
        ordering = ['nom']
        verbose_name = 'Catégorie d’acte'
        verbose_name_plural = 'Catégories d’actes'

    def __str__(self):
        return self.nom


class ActeMedical(models.Model):
    code = models.CharField(
        max_length=30,
        unique=True
    )

    libelle = models.CharField(
        max_length=255
    )

    categorie = models.ForeignKey(
        CategorieActe,
        on_delete=models.PROTECT,
        related_name='actes',
        verbose_name='Catégorie'
    )

    description = models.TextField(
        blank=True
    )

    necessite_medicament = models.BooleanField(
        default=False,
        verbose_name='Nécessite un médicament'
    )

    actif = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = 'parametrage_actes_medicaux'
        ordering = ['libelle']
        verbose_name = 'Acte médical'
        verbose_name_plural = 'Actes médicaux'

    def __str__(self):
        return f'{self.code} - {self.libelle}'


class TarifActe(models.Model):
    acte = models.ForeignKey(
        ActeMedical,
        on_delete=models.PROTECT,
        related_name='tarifs',
        verbose_name='Acte médical'
    )

    etablissement = models.ForeignKey(
        ConfigurationEtablissement,
        on_delete=models.PROTECT,
        related_name='tarifs_actes',
        verbose_name='Établissement'
    )

    montant = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Montant'
    )

    date_debut = models.DateField(
        verbose_name='Date de début'
    )

    date_fin = models.DateField(
        null=True,
        blank=True,
        verbose_name='Date de fin'
    )

    actif = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = 'parametrage_tarifs_actes'
        ordering = ['-date_debut']
        verbose_name = 'Tarif d’acte'
        verbose_name_plural = 'Tarifs des actes'

    def __str__(self):
        return f'{self.acte.libelle} - {self.montant}'