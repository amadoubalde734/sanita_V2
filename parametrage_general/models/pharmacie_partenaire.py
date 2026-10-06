from django.db import models

from .general import (
    TimeStampedModel,
    StatusModel,
    SlugModel,
    Ville,
)


class PharmaciePartenaire(TimeStampedModel, StatusModel, SlugModel):

    STATUT_PARTENARIAT_CHOICES = [
        ('active', "Partenariat actif"),
        ('inactive', "Partenariat inactif"),
        ('suspendue', "Partenariat suspendu"),
    ]

    # ============================================================
    # IDENTIFICATION
    # ============================================================

    nom = models.CharField(
        max_length=191,
        verbose_name="Nom de la pharmacie"
    )

    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Code pharmacie",
        help_text="Identifiant unique de la pharmacie partenaire."
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
        related_name="pharmacies_partenaires",
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
    # INFORMATIONS RÉGLEMENTAIRES
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

    identifiant_administratif = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Identifiant administratif"
    )

    # ============================================================
    # PARTENARIAT SANITA
    # ============================================================

    statut_partenariat = models.CharField(
        max_length=20,
        choices=STATUT_PARTENARIAT_CHOICES,
        default='active',
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
    # INFORMATIONS GÉNÉRALES
    # ============================================================

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description"
    )

    logo = models.ImageField(
        upload_to='pharmacies_partenaires/logos/',
        blank=True,
        null=True,
        verbose_name="Logo"
    )

    observations = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observations"
    )

    # ============================================================
    # CONFIGURATION
    # ============================================================

    gestion_catalogue_active = models.BooleanField(
        default=True,
        verbose_name="Gestion du catalogue active"
    )

    gestion_tarifs_active = models.BooleanField(
        default=True,
        verbose_name="Gestion des tarifs active"
    )

    gestion_stock_active = models.BooleanField(
        default=True,
        verbose_name="Gestion du stock active"
    )

    gestion_ordonnance_active = models.BooleanField(
        default=True,
        verbose_name="Gestion des ordonnances active"
    )

    gestion_dispensation_active = models.BooleanField(
        default=True,
        verbose_name="Gestion de la dispensation active"
    )

    # ============================================================
    # MÉTHODES
    # ============================================================

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(
                self.nom,
                PharmaciePartenaire.objects
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.code})"

    # ============================================================
    # META
    # ============================================================

    class Meta:
        db_table = 'pharmacies_partenaires'
        verbose_name = "Pharmacie partenaire"
        verbose_name_plural = "Pharmacies partenaires"
        ordering = ['nom']