from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
import string
import random


# =========================================================
# ROLE
# =========================================================
class Role(models.Model):
    code = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=191, unique=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"
        indexes = [models.Index(fields=["code"])]

    def clean(self):
        if not self.code:
            raise ValidationError("Le code du rôle est obligatoire.")

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            if Role.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{''.join(random.choices(string.ascii_letters + string.digits, k=6))}"
            self.slug = slug
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"


# =========================================================
# UTILISATEUR
# =========================================================
class CustomUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True, related_name="users", db_index=True)
    contact = models.CharField(max_length=191, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    matricule = models.CharField(max_length=50, unique=True, null=True, blank=True)
    fonction = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=191, unique=True, null=True, blank=True)
    statut_compte = models.BooleanField(default=True)
    statut_connecte = models.BooleanField(default=False)
    statut_change_pass = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    reset_code = models.CharField(max_length=6, blank=True, null=True)
    reset_code_expiry = models.DateTimeField(blank=True, null=True)
    groups = models.ManyToManyField('auth.Group', related_name='sanita_users', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='sanita_users_permissions', blank=True)

    def __str__(self):
        return self.get_full_name() or self.username

    def has_role(self, code):
        return self.role_id and self.role.code == code

    @property
    def role_code(self):
        return self.role.code if self.role_id else None

    def is_admin(self):
        return self.role_code == "administrateur"

    def is_medecin(self):
        return self.role_code == "medecin"

    def is_infirmier(self):
        return self.role_code == "infirmier"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ["username"]


# =========================================================
# MODULE
# =========================================================
class Module(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

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
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="permissions")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="permissions")
    can_create = models.BooleanField(default=False)
    can_read = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_validate = models.BooleanField(default=False)
    can_assign = models.BooleanField(default=False)

    class Meta:
        unique_together = ("role", "module")
        verbose_name = "Permission rôle"
        verbose_name_plural = "Permissions rôles"

    def __str__(self):
        return f"{self.role.name} → {self.module.name}"

    def has_permission(self, action):
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