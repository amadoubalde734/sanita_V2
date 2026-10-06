from django.db import models


class Client(models.Model):

    TYPE_CLIENT_CHOICES = [
        ("particulier", "Particulier"),
        ("entreprise", "Entreprise"),
        ("organisme", "Organisme"),
        ("autre", "Autre"),
    ]

    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Code client"
    )

    type_client = models.CharField(
        max_length=30,
        choices=TYPE_CLIENT_CHOICES,
        default="particulier",
        verbose_name="Type de client"
    )

    nom = models.CharField(
        max_length=255,
        verbose_name="Nom / raison sociale"
    )

    contact = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Contact"
    )

    telephone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Téléphone"
    )

    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="E-mail"
    )

    adresse = models.TextField(
        blank=True,
        null=True,
        verbose_name="Adresse"
    )

    numero_fiscal = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Numéro fiscal"
    )

    actif = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    date_modification = models.DateTimeField(
        auto_now=True
    )


    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True, verbose_name="Slug")
    statut = models.CharField(max_length=20, default="actif", verbose_name="Statut")
    class Meta:
        db_table = "stock_clients"
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ["nom"]

    def __str__(self):
        return self.nom