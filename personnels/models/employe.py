from django.db import models
from django.utils.text import slugify
from parametrage_general.models import Ville, Site, Departement, Service, Societe


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


class Employe(TimeStampedModel, StatusModel, SlugModel):
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=150)
    date_naissance = models.DateField(blank=True, null=True)
    lieu_naissance = models.CharField(max_length=150, blank=True, null=True)
    sexe_choices = [('M', 'Masculin'), ('F', 'Féminin')]
    sexe = models.CharField(max_length=1, choices=sexe_choices, blank=True, null=True)
    fonction = models.CharField(max_length=100, blank=True, null=True)

    societe = models.ForeignKey(Societe, on_delete=models.SET_NULL, null=True, blank=True, related_name='employes')
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True, blank=True, related_name='employes')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='employes')
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True, related_name='employes')
    ville = models.ForeignKey(Ville, on_delete=models.SET_NULL, null=True, blank=True, related_name='employes')

    responsable = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordonnes',
        verbose_name="Responsable hiérarchique"
    )

    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    date_embauche = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='employes/photos/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(f"{self.nom}-{self.prenoms}-{self.matricule}", Employe.objects)
        super().save(*args, **kwargs)

    def clean(self):
        if not self.responsable and Employe.objects.exists():
            from django.core.exceptions import ValidationError
            raise ValidationError("Un responsable hiérarchique doit être renseigné pour cet employé.")

    def __str__(self):
        return f"{self.nom} {self.prenoms} ({self.matricule})"
