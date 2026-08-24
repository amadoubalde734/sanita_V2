from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, Role, Module, RolePermission


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        'username', 'email', 'get_full_name', 'role',
        'matricule', 'statut_compte', 'statut_connecte', 'is_staff',
    )
    list_filter = ('role', 'statut_compte', 'statut_connecte', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'contact', 'matricule')
    ordering = ('username',)
    list_per_page = 25
    save_on_top = True
    autocomplete_fields = ('role',)
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('last_login', 'date_joined', 'avatar_preview')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'email', 'contact', 'avatar', 'avatar_preview')
        }),
        ('Informations professionnelles', {
            'fields': ('matricule', 'fonction', 'role')
        }),
        ('Statut du compte', {
            'fields': ('statut_compte', 'statut_connecte', 'statut_change_pass')
        }),
        ('Sécurité', {
            'fields': ('reset_code', 'reset_code_expiry'),
            'classes': ('collapse',),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

    @admin.display(description="Nom complet")
    def get_full_name(self, obj):
        return obj.get_full_name() or "-"

    @admin.display(description="Aperçu")
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="height:60px;border-radius:6px;" />', obj.avatar.url)
        return "-"


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'code')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'code')


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'module', 'can_create', 'can_read', 'can_update', 'can_delete', 'can_validate', 'can_assign')
    list_filter = ('role', 'module')
    autocomplete_fields = ('role', 'module')


admin.site.site_header = "Administration du Personnel"
admin.site.site_title = "Interface d'administration"
admin.site.index_title = "Bienvenue dans la gestion des utilisateurs"