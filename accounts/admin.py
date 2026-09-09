from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import (
    CustomUser,
    Role,
    Module,
    RolePermission,
)


# =========================================================
# UTILISATEURS
# =========================================================

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    model = CustomUser

    list_display = (
        "username", "email", "get_full_name", "role",
        "fonction", "statut_compte", "statut_connecte", "is_staff",
    )

    list_filter = (
        "role", "statut_compte", "statut_connecte", "statut_change_pass",
        "is_active", "is_staff", "is_superuser",
    )

    search_fields = (
        "username", "email", "first_name", "last_name", "contact", "fonction",
    )

    ordering = ("username",)
    list_per_page = 25
    save_on_top = True

    autocomplete_fields = ("role",)
    filter_horizontal = ("groups", "user_permissions")

    readonly_fields = (
        "last_login", "date_joined", "date_creation",
        "date_modification", "avatar_preview",
    )

    fieldsets = (
        (None, {
            "fields": ("username", "password")
        }),
        ("Informations personnelles", {
            "fields": ("first_name", "last_name", "email", "contact", "avatar", "avatar_preview")
        }),
        ("Informations professionnelles", {
            "fields": ("fonction", "role")
        }),
        ("Organisation", {
            "fields": ("id_societe", "ville", "site")
        }),
        ("Statut du compte", {
            "fields": ("statut_compte", "statut_connecte", "statut_change_pass", "statut_log", "statut_d")
        }),
        ("Sécurité", {
            "fields": ("reset_code", "reset_code_expiry"),
            "classes": ("collapse",),
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Dates importantes", {
            "fields": ("last_login", "date_joined", "date_creation", "date_modification")
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role", "fonction"),
        }),
    )

    @admin.display(description="Nom complet")
    def get_full_name(self, obj):
        return obj.get_full_name() or "-"

    @admin.display(description="Aperçu")
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="height:60px;width:60px;'
                'object-fit:cover;border-radius:8px;" />',
                obj.avatar.url,
            )
        return "-"


# =========================================================
# RÔLES
# =========================================================

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):

    list_display = ("name", "code", "active")
    list_filter = ("active",)
    search_fields = ("name", "code", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)
    list_per_page = 25


# =========================================================
# MODULES
# =========================================================

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):

    list_display = ("name", "code", "active")
    list_filter = ("active",)
    search_fields = ("name", "code", "description")
    ordering = ("name",)
    list_per_page = 25


# =========================================================
# PERMISSIONS DES RÔLES
# =========================================================

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):

    list_display = (
        "role", "module", "can_create", "can_read",
        "can_update", "can_delete", "can_validate", "can_assign",
    )

    list_filter = (
        "role", "module", "can_create", "can_read",
        "can_update", "can_delete", "can_validate", "can_assign",
    )

    search_fields = (
        "role__name", "role__code", "module__name", "module__code",
    )

    autocomplete_fields = ("role", "module")
    list_per_page = 25


# =========================================================
# PERSONNALISATION DJANGO ADMIN / JAZZMIN
# =========================================================

admin.site.site_header = "Administration FleetMining"
admin.site.site_title = "FleetMining Administration"
admin.site.index_title = "Gestion des utilisateurs, rôles et permissions"