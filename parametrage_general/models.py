# Create your models here.
# parametrage/models.py
from django.db import models
from django.utils.text import slugify
import uuid

# ===============================
# MIXINS
# ===============================
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
        while queryset.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    class Meta:
        abstract = True


# ===============================
# SOCIETE
# ===============================
class Societe(TimeStampedModel, StatusModel, SlugModel):
    libelle = models.CharField(max_length=150, verbose_name='Nom de la société')
    date_integration = models.DateField(verbose_name="Date d'intégration")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.libelle)
            if Societe.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{str(uuid.uuid4())[:8]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.libelle

    class Meta:
        db_table = 'societes'
        verbose_name = 'Société'
        verbose_name_plural = 'Sociétés'


# ===============================
# VILLE
# ===============================
class Ville(TimeStampedModel, StatusModel, SlugModel):
    pays = models.CharField(max_length=100, default="Guinée")
    libelle = models.CharField(max_length=150, verbose_name='Ville')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.libelle, Ville.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.libelle

    class Meta:
        db_table = 'villes'
        verbose_name = 'Ville'
        verbose_name_plural = 'Villes'


# ===============================
# SITE
# ===============================
class Site(TimeStampedModel, StatusModel, SlugModel):
    nom_site = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.nom_site, Site.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom_site

    class Meta:
        db_table = 'sites'
        verbose_name = 'Site'
        verbose_name_plural = 'Sites'


# ===============================
# DEPARTEMENT
# ===============================
class Departement(TimeStampedModel, StatusModel, SlugModel):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.nom, Departement.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        db_table = 'departements'
        verbose_name = 'Département'
        verbose_name_plural = 'Départements'


# ===============================
# SERVICE
# ===============================
class Service(TimeStampedModel, StatusModel, SlugModel):
    nom = models.CharField(max_length=100, unique=True)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name='services')
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.nom, Service.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.departement.nom})"

    class Meta:
        db_table = 'services'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

# ===============================
# FONCTION
# ===============================
class Fonction(TimeStampedModel, StatusModel, SlugModel):
    nom = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='fonctions')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.nom, Fonction.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} - {self.service.nom}"

    class Meta:
        db_table = 'fonctions'
        verbose_name = 'Fonction'
        verbose_name_plural = 'Fonctions'

# EmailSettings model for storing email configuration
class EmailSettings(models.Model):
    email_backend = models.CharField(max_length=255, default='django.core.mail.backends.smtp.EmailBackend')
    email_host = models.CharField(max_length=255, default='smtp.gmail.com')
    email_port = models.PositiveIntegerField(default=587)
    email_use_tls = models.BooleanField(default=True)
    email_host_user = models.CharField(max_length=255)
    email_host_password = models.CharField(max_length=255)
    default_from_email = models.CharField(max_length=255)

    def __str__(self):
        return f"Email Settings ({self.email_host})"

class ConfigurationEtablissement(models.Model):
    TYPE_ETABLISSEMENT_CHOICES = [
        ('clinique', 'Clinique privée'),
        ('hopital_public', 'Hôpital public'),
        ('hopital_prive', 'Hôpital privé'),
        ('centre_entreprise', "Centre médical d'entreprise / Prise en charge"),
        ('cabinet', 'Cabinet médical'),
    ]

    nom_etablissement = models.CharField(max_length=255, verbose_name="Nom de l'établissement")
    code_etablissement = models.CharField(max_length=20, unique=True, verbose_name="Code établissement", help_text="Identifiant unique de l'établissement")
    type_etablissement = models.CharField(max_length=30, choices=TYPE_ETABLISSEMENT_CHOICES, default='clinique', verbose_name="Type d'établissement")
    adresse = models.TextField(blank=True, null=True, verbose_name="Adresse")
    telephone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    logo = models.ImageField(upload_to='etablissements/logos/', blank=True, null=True, verbose_name="Logo")
    module_prise_en_charge_actif = models.BooleanField(default=False, verbose_name="Module prise en charge actif", help_text="Active les modules Cartes sanitaires, Entreprises et Bénéficiaires")
    actif = models.BooleanField(default=True, verbose_name="Établissement actif")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuration établissement"
        verbose_name_plural = "Configurations établissements"

    def __str__(self):
        return f"{self.nom_etablissement} ({self.code_etablissement})"