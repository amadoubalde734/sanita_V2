from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify

import string
import random

from parametrage_general.models import Societe, Ville, Site


# =========================================================
# ROLE
# =========================================================

class Role(models.Model):
    code = models.CharField(
        max_length=50, unique=True, db_index=True, verbose_name="Code"
    )
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    slug = models.SlugField(max_length=191, unique=True, blank=True)
    active = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        ordering = ["name"]
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"

    def clean(self):
        if not self.code:
            raise ValidationError("Le code du rôle est obligatoire.")

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            if not base:
                base = "role"
            slug = base
            if Role.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                suffix = "".join(random.choices(string.ascii_letters + string.digits, k=6))
                slug = f"{base}-{suffix}"
            self.slug = slug
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"


# =========================================================
# UTILISATEUR
# =========================================================

class CustomUser(AbstractUser):
    # -----------------------------------------------------
    # Rôle
    # -----------------------------------------------------
    role = models.ForeignKey(
        Role, on_delete=models.PROTECT, null=True, blank=True,
        related_name="users", db_index=True, verbose_name="Rôle"
    )

    # -----------------------------------------------------
    # Informations organisationnelles
    # -----------------------------------------------------
    ville = models.ForeignKey(
        Ville, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Ville"
    )
    site = models.ForeignKey(
        Site, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Site"
    )
    id_societe = models.ForeignKey(
        Societe, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Société"
    )

    # -----------------------------------------------------
    # Informations personnelles
    # -----------------------------------------------------
    contact = models.CharField(max_length=191, blank=True, null=True, verbose_name="Contact")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Photo")
    fonction = models.CharField(max_length=100, blank=True, null=True, verbose_name="Fonction")
    email = models.EmailField(max_length=191, unique=True, null=True, blank=True, verbose_name="Adresse e-mail")

    # -----------------------------------------------------
    # Statuts
    # -----------------------------------------------------
    statut_compte = models.BooleanField(default=True, verbose_name="Compte actif")
    statut_connecte = models.BooleanField(default=False, verbose_name="Connecté")
    statut_log = models.BooleanField(default=True, verbose_name="Journalisation active")
    statut_change_pass = models.BooleanField(default=False, verbose_name="Doit changer le mot de passe")
    statut_d = models.BooleanField(default=True, verbose_name="Statut D")

    # -----------------------------------------------------
    # Dates
    # -----------------------------------------------------
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    # -----------------------------------------------------
    # Réinitialisation mot de passe
    # -----------------------------------------------------
    reset_code = models.CharField(max_length=6, blank=True, null=True)
    reset_code_expiry = models.DateTimeField(blank=True, null=True)

    # -----------------------------------------------------
    # Groupes Django
    # -----------------------------------------------------
    groups = models.ManyToManyField(
        "auth.Group", related_name="fleet_users", blank=True,
        help_text="Groupes de l'utilisateur."
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="fleet_user_permissions", blank=True,
        help_text="Permissions spécifiques à l'utilisateur."
    )

    # -----------------------------------------------------
    # Méthodes
    # -----------------------------------------------------
    def __str__(self):
        full_name = self.get_full_name()
        return f"{self.username} ({full_name})" if full_name else self.username

    @property
    def role_code(self):
        return self.role.code if self.role_id else None

    def has_role(self, code):
        return self.role_code == code

    def is_admin(self):
        return self.role_code == "administrateur"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ["username"]


# =========================================================
# MODULE
# =========================================================

class Module(models.Model):
    code = models.CharField(max_length=100, unique=True, verbose_name="Code")
    name = models.CharField(max_length=150, verbose_name="Nom")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    active = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        ordering = ["name"]
        verbose_name = "Module"
        verbose_name_plural = "Modules"

    def __str__(self):
        return self.name


# =========================================================
# PERMISSIONS ROLE / MODULE
# =========================================================

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="permissions", verbose_name="Rôle")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="permissions", verbose_name="Module")

    can_create = models.BooleanField(default=False, verbose_name="Créer")
    can_read = models.BooleanField(default=False, verbose_name="Consulter")
    can_update = models.BooleanField(default=False, verbose_name="Modifier")
    can_delete = models.BooleanField(default=False, verbose_name="Supprimer")
    can_validate = models.BooleanField(default=False, verbose_name="Valider")
    can_assign = models.BooleanField(default=False, verbose_name="Affecter")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["role", "module"], name="unique_role_module_permission")
        ]
        verbose_name = "Permission rôle"
        verbose_name_plural = "Permissions rôles"

    def __str__(self):
        return f"{self.role.name} → {self.module.name}"

    def has_permission(self, action):
        # Administrateur = accès complet
        if self.role.code == "administrateur":
            return True

        permissions = {
            "create": self.can_create,
            "read": self.can_read,
            "update": self.can_update,
            "delete": self.can_delete,
            "validate": self.can_validate,
            "assign": self.can_assign,
        }

        return permissions.get(action, False)