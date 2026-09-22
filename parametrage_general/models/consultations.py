from django.core.exceptions import ValidationError
from django.db import models

from .general import ConfigurationEtablissement


class TypeConsultation(models.Model):
    CATEGORIE_CHOICES = [
        ('generale', 'Consultation générale'),
        ('specialisee', 'Consultation spécialisée'),
        ('urgence', 'Urgence'),
        ('suivi', 'Suivi et contrôle'),
        ('preventive', 'Prévention'),
        ('travail', 'Médecine du travail'),
        ('teleconsultation', 'Téléconsultation'),
        ('autre', 'Autre consultation'),
    ]

    nom = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Nom'
    )
    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Code'
    )
    categorie = models.CharField(
        max_length=30,
        choices=CATEGORIE_CHOICES,
        default='generale',
        verbose_name='Catégorie'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description'
    )
    ordre = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordre d'affichage"
    )
    actif = models.BooleanField(
        default=True,
        verbose_name='Actif'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parametrage_types_consultations'
        ordering = ['ordre', 'nom']
        verbose_name = 'Type de consultation'
        verbose_name_plural = 'Types de consultation'

    def __str__(self):
        return f'{self.code} - {self.nom}'


class TarifConsultation(models.Model):
    type_consultation = models.ForeignKey(
        TypeConsultation,
        on_delete=models.PROTECT,
        related_name='tarifs',
        verbose_name='Type de consultation'
    )
    etablissement = models.ForeignKey(
        ConfigurationEtablissement,
        on_delete=models.PROTECT,
        related_name='tarifs_consultations',
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
        default=True,
        verbose_name='Actif'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parametrage_tarifs_consultations'
        ordering = ['-date_debut']
        verbose_name = 'Tarif de consultation'
        verbose_name_plural = 'Tarifs des consultations'

    def clean(self):
        if self.date_debut and self.date_fin and self.date_fin < self.date_debut:
            raise ValidationError(
                "La date de fin ne peut pas être antérieure à la date de début."
            )

        if (
            self.actif
            and self.type_consultation_id
            and self.etablissement_id
            and self.date_debut
        ):
            tarifs = TarifConsultation.objects.filter(
                type_consultation=self.type_consultation,
                etablissement=self.etablissement,
                actif=True
            ).exclude(pk=self.pk)

            for tarif in tarifs:
                chevauchement = (
                    self.date_debut <= (tarif.date_fin or self.date_debut)
                    and (
                        not self.date_fin
                        or not tarif.date_fin
                        or self.date_fin >= tarif.date_debut
                    )
                )

                if chevauchement:
                    raise ValidationError(
                        "Un tarif actif existe déjà pour ce type de consultation "
                        "sur cette période, pour cet établissement."
                    )

    def __str__(self):
        return f'{self.type_consultation.nom} - {self.montant}'


class MotifConsultation(models.Model):
    motif = models.CharField(
        max_length=191,
        verbose_name='Motif'
    )
    actif = models.BooleanField(
        default=True,
        verbose_name='Actif'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parametrage_motifs_consultation'
        ordering = ['motif']
        verbose_name = 'Motif de consultation'
        verbose_name_plural = 'Motifs de consultation'

    def __str__(self):
        return self.motif


class Posologie(models.Model):
    libelle = models.CharField(
        max_length=191,
        verbose_name='Posologie'
    )
    actif = models.BooleanField(
        default=True,
        verbose_name='Actif'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parametrage_posologies'
        ordering = ['libelle']
        verbose_name = 'Posologie'
        verbose_name_plural = 'Posologies'

    def __str__(self):
        return self.libelle
    
class VoieAdministration(models.Model):
    nom = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nom"
    )
    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Code"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    ordre = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordre d'affichage"
    )
    actif = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parametrage_voies_administration'
        ordering = ['ordre', 'nom']
        verbose_name = "Voie d'administration"
        verbose_name_plural = "Voies d'administration"

    def __str__(self):
        return f'{self.code} - {self.nom}'


class Dosage(models.Model):
    nom = models.CharField(
        max_length=191,
        unique=True,
        verbose_name="Dosage"
    )
    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Code"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    ordre = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordre d'affichage"
    )
    actif = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parametrage_dosages'
        ordering = ['ordre', 'nom']
        verbose_name = "Dosage"
        verbose_name_plural = "Dosages"

    def __str__(self):
        return f'{self.code} - {self.nom}'


class Forme(models.Model):
    nom = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nom"
    )
    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Code"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    ordre = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordre d'affichage"
    )
    actif = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parametrage_formes'
        ordering = ['ordre', 'nom']
        verbose_name = "Forme pharmaceutique"
        verbose_name_plural = "Formes pharmaceutiques"

    def __str__(self):
        return f'{self.code} - {self.nom}'

    