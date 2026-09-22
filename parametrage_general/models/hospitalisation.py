from django.core.exceptions import ValidationError
from django.db import models

from .general import ConfigurationEtablissement, UniteMedicale


class TypeSejour(models.Model):
    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Code"
    )
    nom = models.CharField(
        max_length=150,
        verbose_name="Nom"
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
        db_table = 'parametrage_types_sejours'
        ordering = ['ordre', 'nom']
        verbose_name = "Type de séjour"
        verbose_name_plural = "Types de séjour"

    def __str__(self):
        return f'{self.code} - {self.nom}'


class TypeChambre(models.Model):
    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Code"
    )
    nom = models.CharField(
        max_length=150,
        verbose_name="Nom"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    capacite = models.PositiveIntegerField(
        default=1,
        verbose_name="Capacité"
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
        db_table = 'parametrage_types_chambres'
        ordering = ['ordre', 'nom']
        verbose_name = "Type de chambre"
        verbose_name_plural = "Types de chambre"

    def __str__(self):
        return f'{self.code} - {self.nom}'


class Chambre(models.Model):
    etablissement = models.ForeignKey(
        ConfigurationEtablissement,
        on_delete=models.PROTECT,
        related_name='chambres',
        verbose_name="Établissement"
    )
    unite = models.ForeignKey(
        UniteMedicale,
        on_delete=models.PROTECT,
        related_name='chambres',
        verbose_name="Unité médicale"
    )
    type_chambre = models.ForeignKey(
        TypeChambre,
        on_delete=models.PROTECT,
        related_name='chambres',
        verbose_name="Type de chambre"
    )
    code = models.CharField(
        max_length=50,
        verbose_name="Code"
    )
    nom = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Nom"
    )
    etage = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Étage"
    )
    localisation = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Localisation"
    )
    capacite = models.PositiveIntegerField(
        default=1,
        verbose_name="Capacité"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    actif = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parametrage_chambres'
        ordering = ['code']
        verbose_name = "Chambre"
        verbose_name_plural = "Chambres"
        constraints = [
            models.UniqueConstraint(
                fields=['etablissement', 'code'],
                name='unique_chambre_etablissement_code'
            )
        ]

    def __str__(self):
        if self.nom:
            return f'{self.code} - {self.nom}'
        return self.code


class Lit(models.Model):
    class Statut(models.TextChoices):
        DISPONIBLE = 'disponible', 'Disponible'
        OCCUPE = 'occupe', 'Occupé'
        RESERVE = 'reserve', 'Réservé'
        MAINTENANCE = 'maintenance', 'Maintenance'
        INACTIF = 'inactif', 'Inactif'

    chambre = models.ForeignKey(
        Chambre,
        on_delete=models.PROTECT,
        related_name='lits',
        verbose_name="Chambre"
    )
    code = models.CharField(
        max_length=50,
        verbose_name="Code"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.DISPONIBLE,
        verbose_name="Statut"
    )
    actif = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parametrage_lits'
        ordering = ['code']
        verbose_name = "Lit"
        verbose_name_plural = "Lits"
        constraints = [
            models.UniqueConstraint(
                fields=['chambre', 'code'],
                name='unique_lit_chambre_code'
            )
        ]

    def __str__(self):
        return f'{self.chambre.code} - {self.code}'


class TypeSoin(models.Model):
    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Code"
    )
    nom = models.CharField(
        max_length=150,
        verbose_name="Nom"
    )
    categorie = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Catégorie"
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
        db_table = 'parametrage_types_soins'
        ordering = ['ordre', 'nom']
        verbose_name = "Type de soin"
        verbose_name_plural = "Types de soins"

    def __str__(self):
        return f'{self.code} - {self.nom}'


class RegimeAlimentaire(models.Model):
    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Code"
    )
    nom = models.CharField(
        max_length=150,
        verbose_name="Nom"
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
        db_table = 'parametrage_regimes_alimentaires'
        ordering = ['ordre', 'nom']
        verbose_name = "Régime alimentaire"
        verbose_name_plural = "Régimes alimentaires"

    def __str__(self):
        return f'{self.code} - {self.nom}'


class MotifHospitalisation(models.Model):
    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Code"
    )
    nom = models.CharField(
        max_length=191,
        verbose_name="Nom"
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
        db_table = 'parametrage_motifs_hospitalisation'
        ordering = ['ordre', 'nom']
        verbose_name = "Motif d'hospitalisation"
        verbose_name_plural = "Motifs d'hospitalisation"

    def __str__(self):
        return f'{self.code} - {self.nom}'


class TypeSortie(models.Model):
    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Code"
    )
    nom = models.CharField(
        max_length=150,
        verbose_name="Nom"
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
        db_table = 'parametrage_types_sortie'
        ordering = ['ordre', 'nom']
        verbose_name = "Type de sortie"
        verbose_name_plural = "Types de sortie"

    def __str__(self):
        return f'{self.code} - {self.nom}'


class TarifSejour(models.Model):
    etablissement = models.ForeignKey(
        ConfigurationEtablissement,
        on_delete=models.PROTECT,
        related_name='tarifs_sejours',
        verbose_name="Établissement"
    )
    type_sejour = models.ForeignKey(
        TypeSejour,
        on_delete=models.PROTECT,
        related_name='tarifs',
        verbose_name="Type de séjour"
    )
    type_chambre = models.ForeignKey(
        TypeChambre,
        on_delete=models.PROTECT,
        related_name='tarifs_sejours',
        null=True,
        blank=True,
        verbose_name="Type de chambre"
    )
    montant = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Montant"
    )
    unite_facturation = models.CharField(
        max_length=50,
        default='jour',
        verbose_name="Unité de facturation"
    )
    date_debut = models.DateField(
        verbose_name="Date de début"
    )
    date_fin = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de fin"
    )
    actif = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parametrage_tarifs_sejours'
        ordering = ['-date_debut']
        verbose_name = "Tarif de séjour"
        verbose_name_plural = "Tarifs des séjours"

    def __str__(self):
        return f'{self.type_sejour.nom} - {self.montant}'

    def clean(self):
        if self.date_fin and self.date_fin < self.date_debut:
            raise ValidationError({
                'date_fin': "La date de fin doit être postérieure ou égale à la date de début."
            })

        if self.montant < 0:
            raise ValidationError({
                'montant': "Le montant ne peut pas être négatif."
            })

        if not self.actif:
            return

        queryset = TarifSejour.objects.filter(
            etablissement=self.etablissement,
            type_sejour=self.type_sejour,
            type_chambre=self.type_chambre,
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
                    "Un tarif actif existe déjà pour cette combinaison sur une période qui se chevauche."
                )

