from django.db import models
from django.utils.text import slugify
import uuid


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StatusModel(models.Model):
    actif = models.BooleanField(default=True)

    class Meta:
        abstract = True


class SlugModel(models.Model):
    slug = models.SlugField(max_length=191, unique=True, blank=True)

    def generate_unique_slug(self, field_value, queryset):
        base_slug = slugify(field_value)
        slug = base_slug
        counter = 1

        while queryset.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    class Meta:
        abstract = True


class Societe(TimeStampedModel, StatusModel, SlugModel):
    libelle = models.CharField(
        max_length=150,
        verbose_name='Nom de la société'
    )

    date_integration = models.DateField(
        verbose_name="Date d'intégration"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.libelle)

            if Societe.objects.filter(
                slug=self.slug
            ).exclude(pk=self.pk).exists():
                self.slug = f"{self.slug}-{str(uuid.uuid4())[:8]}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.libelle

    class Meta:
        db_table = 'societes'
        verbose_name = 'Société'
        verbose_name_plural = 'Sociétés'


class Ville(TimeStampedModel, StatusModel, SlugModel):
    pays = models.CharField(
        max_length=100,
        default="Guinée"
    )

    libelle = models.CharField(
        max_length=150,
        verbose_name='Ville'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(
                self.libelle,
                Ville.objects
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.libelle

    class Meta:
        db_table = 'villes'
        verbose_name = 'Ville'
        verbose_name_plural = 'Villes'


class Site(TimeStampedModel, StatusModel, SlugModel):
    nom_site = models.CharField(
        max_length=255
    )

    adresse = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(
                self.nom_site,
                Site.objects
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom_site

    class Meta:
        db_table = 'sites'
        verbose_name = 'Site'
        verbose_name_plural = 'Sites'


class Direction(TimeStampedModel, StatusModel, SlugModel):
    nom = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(
                self.nom,
                Direction.objects
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        db_table = 'directions'
        verbose_name = 'Direction'
        verbose_name_plural = 'Directions'


class Departement(TimeStampedModel, StatusModel, SlugModel):
    nom = models.CharField(
        max_length=100,
        unique=True
    )

    direction = models.ForeignKey(
        Direction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='departements',
        verbose_name='Direction'
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(
                self.nom,
                Departement.objects
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        db_table = 'departements'
        verbose_name = 'Département'
        verbose_name_plural = 'Départements'


class Service(TimeStampedModel, StatusModel, SlugModel):
    nom = models.CharField(
        max_length=100,
        unique=True
    )

    departement = models.ForeignKey(
        Departement,
        on_delete=models.CASCADE,
        related_name='services'
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(
                self.nom,
                Service.objects
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.departement.nom})"

    class Meta:
        db_table = 'services'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'


class Fonction(TimeStampedModel, StatusModel, SlugModel):
    nom = models.CharField(
        max_length=150,
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='fonctions'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(
                self.nom,
                Fonction.objects
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} - {self.service.nom}"

    class Meta:
        db_table = 'fonctions'
        verbose_name = 'Fonction'
        verbose_name_plural = 'Fonctions'


class Specialite(TimeStampedModel, StatusModel, SlugModel):
    nom = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom de la spécialité"
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    icone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Icône",
        help_text="Classe icône Remix Icon"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(
                self.nom,
                Specialite.objects
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        db_table = 'specialites'
        verbose_name = 'Spécialité'
        verbose_name_plural = 'Spécialités'
        ordering = ['nom']


class UniteMedicale(TimeStampedModel, StatusModel, SlugModel):
    TYPE_UNITE_CHOICES = [
        ('infirmerie', 'Infirmerie'),
        ('laboratoire', 'Laboratoire'),
        ('pharmacie', 'Pharmacie'),
        ('imagerie', 'Imagerie médicale'),
        ('consultation', 'Consultation'),
        ('urgences', 'Urgences'),
        ('hospitalisation', 'Hospitalisation'),
        ('autre', 'Autre unité médicale'),
    ]

    nom = models.CharField(
        max_length=150,
        verbose_name="Nom de l'unité"
    )

    type_unite = models.CharField(
        max_length=30,
        choices=TYPE_UNITE_CHOICES,
        verbose_name="Type d'unité"
    )

    site = models.ForeignKey(
        Site,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='unites_medicales',
        verbose_name="Site"
    )

    specialites = models.ManyToManyField(
        Specialite,
        blank=True,
        related_name='unites_medicales',
        verbose_name="Spécialités"
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(
                self.nom,
                UniteMedicale.objects
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        db_table = 'unites_medicales'
        verbose_name = 'Unité médicale'
        verbose_name_plural = 'Unités médicales'
        ordering = ['nom']


class EmailSettings(models.Model):
    email_backend = models.CharField(
        max_length=255,
        default='django.core.mail.backends.smtp.EmailBackend'
    )

    email_host = models.CharField(
        max_length=255,
        default='smtp.gmail.com'
    )

    email_port = models.PositiveIntegerField(
        default=587
    )

    email_use_tls = models.BooleanField(
        default=True
    )

    email_host_user = models.CharField(
        max_length=255
    )

    email_host_password = models.CharField(
        max_length=255
    )

    default_from_email = models.CharField(
        max_length=255
    )

    def __str__(self):
        return f"Email Settings ({self.email_host})"


class ConfigurationEtablissement(models.Model):
    TYPE_ETABLISSEMENT_CHOICES = [
        ('clinique', 'Clinique privée'),
        ('hopital_public', 'Hôpital public'),
        ('hopital_prive', 'Hôpital privé'),
        ('cabinet', 'Cabinet médical'),
        ('centre_sante', 'Centre de santé'),
        ('cabinet_dentaire', 'Cabinet dentaire'),
        ('cabinet_ophtalmologique', 'Cabinet ophtalmologique'),
        ('polyclinique', 'Polyclinique'),
        ('centre_imagerie', "Centre d'imagerie"),
        ('laboratoire', 'Laboratoire'),
        ('autre', 'Autre établissement de santé'),
    ]

    nom_etablissement = models.CharField(
        max_length=255,
        verbose_name="Nom de l'établissement"
    )

    code_etablissement = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Code établissement",
        help_text="Identifiant unique de l'établissement"
    )

    type_etablissement = models.CharField(
        max_length=30,
        choices=TYPE_ETABLISSEMENT_CHOICES,
        default='clinique',
        verbose_name="Type d'établissement"
    )

    specialites = models.ManyToManyField(
        Specialite,
        blank=True,
        related_name='etablissements',
        verbose_name="Spécialités",
        help_text="Spécialités médicales pratiquées dans l'établissement"
    )

    pays = models.CharField(
        max_length=100,
        default='Guinée',
        verbose_name="Pays"
    )

    ville = models.ForeignKey(
        Ville,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='etablissements',
        verbose_name="Ville"
    )

    adresse = models.TextField(
        blank=True,
        null=True,
        verbose_name="Adresse"
    )

    boite_postale = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Boîte postale"
    )

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
        verbose_name="Email"
    )

    site_web = models.URLField(
        blank=True,
        null=True,
        verbose_name="Site web"
    )

    logo = models.ImageField(
        upload_to='etablissements/logos/',
        blank=True,
        null=True,
        verbose_name="Logo"
    )

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

    devise = models.CharField(
        max_length=10,
        default='GNF',
        verbose_name="Devise"
    )

    fuseau_horaire = models.CharField(
        max_length=50,
        default='Africa/Conakry',
        verbose_name="Fuseau horaire"
    )

    module_prise_en_charge_actif = models.BooleanField(
        default=False,
        verbose_name="Module prise en charge actif",
        help_text="Active les modules liés à la prise en charge entreprise"
    )

    module_conventions_actif = models.BooleanField(
        default=False,
        verbose_name="Module conventions entreprises",
        help_text="Active la gestion des conventions et entreprises partenaires"
    )

    actif = models.BooleanField(
        default=True,
        verbose_name="Établissement actif"
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    date_modification = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Configuration établissement"
        verbose_name_plural = "Configurations établissements"
        ordering = ['nom_etablissement']

    def __str__(self):
        return f"{self.nom_etablissement} ({self.code_etablissement})"

    @property
    def specialites_slugs(self):
        return list(
            self.specialites
            .filter(actif=True)
            .values_list('slug', flat=True)
        )