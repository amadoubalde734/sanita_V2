from django.db import models

from .general import (
    TimeStampedModel,
    StatusModel,
    SlugModel,
    Ville,
    Site,
    UniteMedicale,
)
from .cliniques import EtablissementPartenaire


class Pharmacie(TimeStampedModel, StatusModel, SlugModel):

    TYPE_PHARMACIE_CHOICES = [
        ('interne_entreprise', "Pharmacie interne d'entreprise"),
        ('etablissement', "Pharmacie d'établissement de santé"),
        ('partenaire', "Pharmacie partenaire"),
        ('independante', "Pharmacie indépendante"),
        ('hospitaliere', "Pharmacie hospitalière"),
        ('autre', "Autre type de pharmacie"),
    ]

    STATUT_PARTENAIRE_CHOICES = [
        ('non_partenaire', "Non partenaire"),
        ('active', "Partenaire active"),
        ('inactive', "Partenaire inactive"),
        ('suspendue', "Partenariat suspendu"),
    ]

    # ============================================================
    # IDENTIFICATION
    # ============================================================

    nom = models.CharField(
        max_length=255,
        verbose_name="Nom de la pharmacie"
    )

    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Code pharmacie",
        help_text="Identifiant unique de la pharmacie."
    )

    type_pharmacie = models.CharField(
        max_length=30,
        choices=TYPE_PHARMACIE_CHOICES,
        default='independante',
        verbose_name="Type de pharmacie"
    )

    # ============================================================
    # RATTACHEMENTS
    # ============================================================

    site = models.ForeignKey(
        Site,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pharmacies',
        verbose_name="Site"
    )

    unite_medicale = models.ForeignKey(
        UniteMedicale,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pharmacies',
        verbose_name="Unité médicale"
    )

    etablissement_partenaire = models.ForeignKey(
        EtablissementPartenaire,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pharmacies',
        verbose_name="Établissement partenaire"
    )

    # ============================================================
    # LOCALISATION
    # ============================================================

    pays = models.CharField(
        max_length=100,
        default="Guinée",
        verbose_name="Pays"
    )

    ville = models.ForeignKey(
        Ville,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pharmacies',
        verbose_name="Ville"
    )

    quartier = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Quartier"
    )

    adresse = models.TextField(
        blank=True,
        null=True,
        verbose_name="Adresse"
    )

    # ============================================================
    # CONTACT
    # ============================================================

    telephone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Téléphone"
    )

    telephone_secondaire = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Téléphone secondaire"
    )

    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Adresse e-mail"
    )

    site_web = models.URLField(
        blank=True,
        null=True,
        verbose_name="Site web"
    )

    # ============================================================
    # RESPONSABLE
    # ============================================================

    nom_responsable = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Nom du responsable"
    )

    fonction_responsable = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Fonction du responsable"
    )

    numero_ordre_responsable = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Numéro d'ordre"
    )

    telephone_responsable = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Téléphone du responsable"
    )

    email_responsable = models.EmailField(
        blank=True,
        null=True,
        verbose_name="E-mail du responsable"
    )

    # ============================================================
    # INFORMATIONS REGLEMENTAIRES
    # ============================================================

    numero_agrement = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Numéro d'agrément"
    )

    numero_autorisation = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Numéro d'autorisation"
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

    # ============================================================
    # PARTENARIAT
    # ============================================================

    statut_partenaire = models.CharField(
        max_length=20,
        choices=STATUT_PARTENAIRE_CHOICES,
        default='non_partenaire',
        verbose_name="Statut du partenariat"
    )

    accepte_ordonnances_sanita = models.BooleanField(
        default=True,
        verbose_name="Accepte les ordonnances SANITA",
        help_text=(
            "Indique si la pharmacie peut recevoir et traiter "
            "les ordonnances émises depuis SANITA."
        )
    )

    date_debut_partenariat = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date de début du partenariat"
    )

    date_fin_partenariat = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date de fin du partenariat"
    )

    # ============================================================
    # INFORMATIONS GENERALES
    # ============================================================

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description"
    )

    logo = models.ImageField(
        upload_to='pharmacies/logos/',
        blank=True,
        null=True,
        verbose_name="Logo"
    )

    # ============================================================
    # CONFIGURATION
    # ============================================================

    gestion_stock_active = models.BooleanField(
        default=True,
        verbose_name="Gestion du stock active"
    )

    gestion_vente_active = models.BooleanField(
        default=True,
        verbose_name="Gestion des ventes active"
    )

    gestion_ordonnance_active = models.BooleanField(
        default=True,
        verbose_name="Gestion des ordonnances active"
    )

    gestion_lots_active = models.BooleanField(
        default=True,
        verbose_name="Gestion des lots active"
    )

    gestion_inventaire_active = models.BooleanField(
        default=True,
        verbose_name="Gestion des inventaires active"
    )

    actif = models.BooleanField(
        default=True,
        verbose_name="Pharmacie active"
    )

    # ============================================================
    # METHODES
    # ============================================================

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(
                self.nom,
                Pharmacie.objects
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.code})"

    class Meta:
        db_table = 'pharmacies'
        verbose_name = "Pharmacie"
        verbose_name_plural = "Pharmacies"
        ordering = ['nom']