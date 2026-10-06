from django.db import models

from .general import (
    TimeStampedModel,
    StatusModel,
    SlugModel,
    Ville,
    Specialite,
)


class EtablissementPartenaire(TimeStampedModel, StatusModel, SlugModel):

    TYPE_PARTENAIRE_CHOICES = [
        ('clinique', 'Clinique privée'),
        ('hopital_public', 'Hôpital public'),
        ('hopital_prive', 'Hôpital privé'),
        ('polyclinique', 'Polyclinique'),
        ('centre_medical', 'Centre médical'),
        ('cabinet_medical', 'Cabinet médical'),
        ('cabinet_dentaire', 'Cabinet dentaire'),
        ('cabinet_ophtalmologique', 'Cabinet ophtalmologique'),
        ('laboratoire', 'Laboratoire'),
        ('centre_imagerie', "Centre d'imagerie"),
        ('centre_specialise', 'Centre spécialisé'),
        ('autre', 'Autre structure de santé'),
    ]

    STATUT_PARTENAIRE_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('suspendu', 'Suspendu'),
    ]

    # ============================================================
    # IDENTIFICATION
    # ============================================================

    nom = models.CharField(
        max_length=255,
        verbose_name="Nom de l'établissement",
    )

    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Code partenaire",
        help_text="Identifiant unique de l'établissement partenaire.",
    )

    type_partenaire = models.CharField(
        max_length=40,
        choices=TYPE_PARTENAIRE_CHOICES,
        default='clinique',
        verbose_name="Type de structure",
    )

    # ============================================================
    # LOCALISATION
    # ============================================================

    pays = models.CharField(
        max_length=100,
        default="Guinée",
        verbose_name="Pays",
    )

    ville = models.ForeignKey(
        Ville,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='etablissements_partenaires',
        verbose_name="Ville",
    )

    quartier = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Quartier",
    )

    adresse = models.TextField(
        blank=True,
        null=True,
        verbose_name="Adresse",
    )

    # ============================================================
    # CONTACT DE L'ETABLISSEMENT
    # ============================================================

    telephone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Téléphone",
    )

    telephone_secondaire = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Téléphone secondaire",
    )

    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Adresse e-mail",
    )

    site_web = models.URLField(
        blank=True,
        null=True,
        verbose_name="Site web",
    )

    # ============================================================
    # CONTACT PRINCIPAL
    # ============================================================

    nom_contact = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Nom du contact",
    )

    fonction_contact = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Fonction du contact",
    )

    telephone_contact = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Téléphone du contact",
    )

    email_contact = models.EmailField(
        blank=True,
        null=True,
        verbose_name="E-mail du contact",
    )

    # ============================================================
    # INFORMATIONS ADMINISTRATIVES
    # ============================================================

    numero_agrement = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Numéro d'agrément",
    )

    numero_autorisation = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Numéro d'autorisation",
    )

    numero_fiscal = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Numéro fiscal",
    )

    registre_commerce = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Registre de commerce",
    )

    # ============================================================
    # SPECIALITES
    # ============================================================

    specialites = models.ManyToManyField(
        Specialite,
        blank=True,
        related_name='etablissements_partenaires',
        verbose_name="Spécialités",
    )

    # ============================================================
    # INFORMATIONS COMPLEMENTAIRES
    # ============================================================

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
    )

    # ============================================================
    # RELATION PARTENAIRE
    # ============================================================

    accepte_orientation = models.BooleanField(
        default=True,
        verbose_name="Accepte les orientations",
        help_text="Indique si l'établissement accepte les patients orientés par SANITA.",
    )

    statut_partenaire = models.CharField(
        max_length=20,
        choices=STATUT_PARTENAIRE_CHOICES,
        default='actif',
        verbose_name="Statut du partenariat",
    )

    date_debut_partenariat = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date de début du partenariat",
    )

    date_fin_partenariat = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date de fin du partenariat",
    )

    # ============================================================
    # METHODES
    # ============================================================

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(
                self.nom,
                EtablissementPartenaire.objects
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.get_type_partenaire_display()})"

    # ============================================================
    # META
    # ============================================================

    class Meta:
        db_table = 'etablissements_partenaires'
        verbose_name = "Établissement partenaire"
        verbose_name_plural = "Établissements partenaires"
        ordering = ['nom']