import secrets
import string
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from parametrage_general.models import ConfigurationEtablissement

# =========================================================
# PLAN / FORMULE D'ABONNEMENT
# =========================================================

class Plan(models.Model):

    class Code(models.TextChoices):
        STANDARD = "STANDARD", "Standard"
        PROFESSIONAL = "PROFESSIONAL", "Professional"
        ENTERPRISE = "ENTERPRISE", "Enterprise"

    code = models.CharField("Code", max_length=20, choices=Code.choices, unique=True)
    name = models.CharField("Nom", max_length=100)
    description = models.TextField("Description", blank=True, default="")

    price = models.DecimalField("Prix", max_digits=15, decimal_places=2, default=0)
    currency = models.CharField("Devise", max_length=10, default="GNF")

    max_users = models.PositiveIntegerField("Nombre maximum d'utilisateurs", default=10)
    max_sites = models.PositiveIntegerField("Nombre maximum de sites", default=1)
    unlimited_users = models.BooleanField("Utilisateurs illimités", default=False)
    unlimited_sites = models.BooleanField("Sites illimités", default=False)

    active = models.BooleanField("Actif", default=True, db_index=True)

    created_at = models.DateTimeField("Date de création", auto_now_add=True)
    updated_at = models.DateTimeField("Dernière modification", auto_now=True)

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"
        ordering = ["price", "name"]

    def __str__(self):
        return self.name

    @property
    def users_limit_display(self):
        return "Illimité" if self.unlimited_users else self.max_users

    @property
    def sites_limit_display(self):
        return "Illimité" if self.unlimited_sites else self.max_sites


# =========================================================
# LICENCE — l'abonnement de CET établissement auprès de SANITA
# =========================================================

class License(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        EXPIRING_SOON = "EXPIRING_SOON", "Expire bientôt"
        EXPIRED = "EXPIRED", "Expirée"
        SUSPENDED = "SUSPENDED", "Suspendue"
        CANCELLED = "CANCELLED", "Annulée"

    class Duration(models.IntegerChoices):
        ONE_YEAR = 1, "1 an"
        TWO_YEARS = 2, "2 ans"
        THREE_YEARS = 3, "3 ans"

    license_key = models.CharField(
        "Clé de licence", max_length=64, unique=True, editable=False, db_index=True,
    )

    etablissement = models.ForeignKey(
        ConfigurationEtablissement, on_delete=models.PROTECT, related_name="licenses",
        verbose_name="Établissement",
    )
    plan = models.ForeignKey(
        Plan, on_delete=models.PROTECT, related_name="licenses", verbose_name="Plan",
    )

    start_date = models.DateField("Date de début")
    end_date = models.DateField("Date d'expiration", editable=False)
    duration_years = models.PositiveSmallIntegerField(
        "Durée", choices=Duration.choices, default=Duration.ONE_YEAR,
    )

    max_users = models.PositiveIntegerField("Nombre maximum d'utilisateurs", default=10)
    max_sites = models.PositiveIntegerField("Nombre maximum de sites", default=1)

    status = models.CharField(
        "Statut", max_length=20, choices=Status.choices, default=Status.ACTIVE, db_index=True,
    )

    auto_renew = models.BooleanField("Renouvellement automatique", default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="created_licenses", verbose_name="Créée par",
    )
    created_at = models.DateTimeField("Date de création", auto_now_add=True)
    updated_at = models.DateTimeField("Dernière modification", auto_now=True)
    notes = models.TextField("Notes", blank=True, default="")

    class Meta:
        verbose_name = "Licence"
        verbose_name_plural = "Licences"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.license_key} - {self.etablissement.nom_etablissement}"

    @staticmethod
    def generate_license_key():
        alphabet = string.ascii_uppercase + string.digits
        while True:
            parts = ["".join(secrets.choice(alphabet) for _ in range(4)) for _ in range(4)]
            key = "FM-" + "-".join(parts)
            if not License.objects.filter(license_key=key).exists():
                return key

    def calculate_end_date(self):
        if not self.start_date:
            return None
        return self.start_date.replace(
            year=self.start_date.year + self.duration_years
        ) - timedelta(days=1)

    def apply_plan_limits(self):
        if not self.plan:
            return
        self.max_users = 0 if self.plan.unlimited_users else self.plan.max_users
        self.max_sites = 0 if self.plan.unlimited_sites else self.plan.max_sites

    def update_status(self, save=True):
        if not self.end_date:
            return self.status
        today = timezone.localdate()
        if self.status in [self.Status.SUSPENDED, self.Status.CANCELLED]:
            return self.status
        if today > self.end_date:
            new_status = self.Status.EXPIRED
        elif today >= self.end_date - timedelta(days=30):
            new_status = self.Status.EXPIRING_SOON
        else:
            new_status = self.Status.ACTIVE
        if self.status != new_status:
            self.status = new_status
            if save:
                super().save(update_fields=["status", "updated_at"])
        return self.status

    @property
    def is_valid(self):
        self.update_status(save=True)
        return self.status == self.Status.ACTIVE

    @property
    def days_remaining(self):
        if not self.end_date:
            return 0
        today = timezone.localdate()
        if today > self.end_date:
            return 0
        return (self.end_date - today).days

    def save(self, *args, **kwargs):
        if not self.license_key:
            self.license_key = self.generate_license_key()
        self.apply_plan_limits()
        if self.start_date and self.duration_years:
            self.end_date = self.calculate_end_date()
        super().save(*args, **kwargs)


# =========================================================
# CONTRAT DE MAINTENANCE
# =========================================================

class MaintenanceContract(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Actif"
        EXPIRING_SOON = "EXPIRING_SOON", "Expire bientôt"
        EXPIRED = "EXPIRED", "Expiré"
        SUSPENDED = "SUSPENDED", "Suspendu"
        CANCELLED = "CANCELLED", "Annulé"

    contract_number = models.CharField(
        "Numéro du contrat", max_length=50, unique=True, editable=False, db_index=True,
    )

    etablissement = models.ForeignKey(
        ConfigurationEtablissement, on_delete=models.PROTECT,
        related_name="maintenance_contracts", verbose_name="Établissement",
    )
    license = models.ForeignKey(
        License, on_delete=models.PROTECT,
        related_name="maintenance_contracts", verbose_name="Licence",
    )

    start_date = models.DateField("Date de début")
    end_date = models.DateField("Date d'expiration")

    amount = models.DecimalField("Montant", max_digits=15, decimal_places=2, default=0)
    currency = models.CharField("Devise", max_length=10, default="GNF")

    status = models.CharField(
        "Statut", max_length=20, choices=Status.choices, default=Status.ACTIVE, db_index=True,
    )

    description = models.TextField("Description", blank=True, default="")
    notes = models.TextField("Notes", blank=True, default="")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="created_maintenance_contracts", verbose_name="Créé par",
    )
    created_at = models.DateTimeField("Date de création", auto_now_add=True)
    updated_at = models.DateTimeField("Dernière modification", auto_now=True)

    class Meta:
        verbose_name = "Contrat de maintenance"
        verbose_name_plural = "Contrats de maintenance"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.contract_number} - {self.etablissement.nom_etablissement}"

    @staticmethod
    def generate_contract_number():
        while True:
            number = f"CTR-{secrets.randbelow(900000) + 100000}"
            if not MaintenanceContract.objects.filter(contract_number=number).exists():
                return number

    def update_status(self, save=True):
        if not self.end_date:
            return self.status
        today = timezone.localdate()
        if self.status in [self.Status.SUSPENDED, self.Status.CANCELLED]:
            return self.status
        if today > self.end_date:
            new_status = self.Status.EXPIRED
        elif today >= self.end_date - timedelta(days=30):
            new_status = self.Status.EXPIRING_SOON
        else:
            new_status = self.Status.ACTIVE
        if self.status != new_status:
            self.status = new_status
            if save:
                super().save(update_fields=["status", "updated_at"])
        return self.status

    @property
    def is_valid(self):
        self.update_status(save=True)
        return self.status == self.Status.ACTIVE

    @property
    def days_remaining(self):
        if not self.end_date:
            return 0
        today = timezone.localdate()
        if today > self.end_date:
            return 0
        return (self.end_date - today).days

    def save(self, *args, **kwargs):
        if not self.contract_number:
            self.contract_number = self.generate_contract_number()
        super().save(*args, **kwargs)