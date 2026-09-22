from django.core.exceptions import ValidationError
from django.db import models

from .general import ConfigurationEtablissement


class CategorieExamen(models.Model):
    code = models.CharField(max_length=30, unique=True, verbose_name="Code")
    nom = models.CharField(max_length=150, unique=True, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parametrage_categories_examens'
        ordering = ['ordre', 'nom']
        verbose_name = "Catégorie d'examen"
        verbose_name_plural = "Catégories d'examens"

    def __str__(self):
        return f'{self.code} - {self.nom}'


class TypeExamen(models.Model):
    categorie = models.ForeignKey(
        CategorieExamen,
        on_delete=models.PROTECT,
        related_name='types_examens',
        verbose_name="Catégorie"
    )
    code = models.CharField(max_length=30, unique=True, verbose_name="Code")
    nom = models.CharField(max_length=150, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parametrage_types_examens'
        ordering = ['categorie__ordre', 'ordre', 'nom']
        verbose_name = "Type d'examen"
        verbose_name_plural = "Types d'examens"
        constraints = [
            models.UniqueConstraint(
                fields=['categorie', 'nom'],
                name='unique_type_examen_categorie_nom'
            )
        ]

    def __str__(self):
        return f'{self.code} - {self.nom}'


class Examen(models.Model):
    type_examen = models.ForeignKey(
        TypeExamen,
        on_delete=models.PROTECT,
        related_name='examens',
        verbose_name="Type d'examen"
    )
    code = models.CharField(max_length=50, unique=True, verbose_name="Code")
    libelle = models.CharField(max_length=255, verbose_name="Libellé")
    description = models.TextField(blank=True, verbose_name="Description")
    unite = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Unité"
    )
    valeur_reference = models.TextField(
        blank=True,
        verbose_name="Valeur de référence"
    )
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parametrage_examens'
        ordering = [
            'type_examen__categorie__ordre',
            'type_examen__ordre',
            'ordre',
            'libelle'
        ]
        verbose_name = "Examen"
        verbose_name_plural = "Examens"

    def __str__(self):
        return f'{self.code} - {self.libelle}'


class TarifExamen(models.Model):
    examen = models.ForeignKey(
        Examen,
        on_delete=models.PROTECT,
        related_name='tarifs',
        verbose_name="Examen"
    )
    etablissement = models.ForeignKey(
        ConfigurationEtablissement,
        on_delete=models.PROTECT,
        related_name='tarifs_examens',
        verbose_name="Établissement"
    )
    montant = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Montant"
    )
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de fin"
    )
    actif = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parametrage_tarifs_examens'
        ordering = ['-date_debut']
        verbose_name = "Tarif d'examen"
        verbose_name_plural = "Tarifs des examens"

    def __str__(self):
        return f'{self.examen.libelle} - {self.montant}'

    def clean(self):
        if self.date_fin and self.date_fin < self.date_debut:
            raise ValidationError({
                'date_fin': "La date de fin doit être postérieure ou égale à la date de début."
            })

        if not self.actif:
            return

        queryset = TarifExamen.objects.filter(
            examen=self.examen,
            etablissement=self.etablissement,
            actif=True
        ).exclude(pk=self.pk)

        for tarif in queryset:
            if (
                self.date_fin is None
                or tarif.date_fin is None
                or (
                    self.date_debut <= tarif.date_fin
                    and self.date_fin >= tarif.date_debut
                )
            ):
                raise ValidationError(
                    "Un tarif actif existe déjà pour cet examen et cet établissement sur une période qui se chevauche."
                )

