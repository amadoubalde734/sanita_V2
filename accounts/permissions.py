"""
Gestion des permissions par module et par rôle.

Ce module fournit trois outils :

    has_module_permission()        -> vérification ponctuelle
    @permission_required()         -> protection d'une vue fonction
    ModulePermissionRequiredMixin  -> protection d'une Class-Based View

Les permissions d'un utilisateur sont chargées en UNE seule requête SQL
puis mises en cache sur l'objet utilisateur pour la durée de la requête HTTP.
"""

from functools import wraps

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, resolve_url

from .models import RolePermission


# =========================================================
# CONSTANTES
# =========================================================

ALLOWED_ACTIONS = frozenset({
    "create",
    "read",
    "update",
    "delete",
    "validate",
    "assign",
})

LOGIN_URL = "accounts:admin_login"
DENIED_REDIRECT_URL = "dashboard:index"
DENIED_MESSAGE = (
    "Vous n'avez pas les permissions nécessaires "
    "pour effectuer cette action."
)

_CACHE_ATTR = "_module_permissions_cache"


# =========================================================
# OUTILS INTERNES
# =========================================================

def _is_admin(user):
    """
    Retourne True si l'utilisateur est administrateur.
    Supporte `is_admin` en méthode ou en propriété, ainsi que `is_superuser`.
    """
    if getattr(user, "is_superuser", False):
        return True

    is_admin = getattr(user, "is_admin", False)
    return bool(is_admin() if callable(is_admin) else is_admin)


def _get_user_permissions(user):
    """
    Charge toutes les permissions du rôle de l'utilisateur
    sous la forme : { "CODE_MODULE": {"read", "update", ...} }

    Le résultat est mis en cache sur l'objet utilisateur afin d'éviter
    une requête SQL à chaque vérification.
    """
    cached = getattr(user, _CACHE_ATTR, None)
    if cached is not None:
        return cached

    permissions = {}

    fields = [f"can_{action}" for action in ALLOWED_ACTIONS]

    rows = RolePermission.objects.filter(
        role_id=user.role_id,
        module__active=True,
    ).values("module__code", *fields)

    for row in rows:
        actions = permissions.setdefault(row["module__code"], set())
        actions.update(
            action for action in ALLOWED_ACTIONS if row[f"can_{action}"]
        )

    setattr(user, _CACHE_ATTR, permissions)
    return permissions


def _validate_action(action):
    """Lève une erreur explicite si l'action n'existe pas (erreur de développement)."""
    if action not in ALLOWED_ACTIONS:
        raise ImproperlyConfigured(
            f"Action de permission inconnue : '{action}'. "
            f"Actions autorisées : {', '.join(sorted(ALLOWED_ACTIONS))}."
        )


def _deny(request, message=DENIED_MESSAGE):
    """Réponse standard en cas d'accès refusé."""
    messages.error(request, message)
    return redirect(DENIED_REDIRECT_URL)


def _login_redirect(request):
    """Redirige vers la connexion en conservant la page demandée (?next=)."""
    return redirect_to_login(
        request.get_full_path(),
        resolve_url(LOGIN_URL),
    )


# =========================================================
# VÉRIFICATION D'UNE PERMISSION
# =========================================================

def has_module_permission(user, module_code, action):
    """
    Vérifie si un utilisateur possède une permission sur un module.

    Exemple :
        has_module_permission(request.user, "UTILISATEURS", "read")

    Actions disponibles :
        create, read, update, delete, validate, assign
    """
    if action not in ALLOWED_ACTIONS:
        return False

    if not user or not user.is_authenticated:
        return False

    if _is_admin(user):
        return True

    if not getattr(user, "role_id", None):
        return False

    return action in _get_user_permissions(user).get(module_code, set())


def clear_permissions_cache(user):
    """À appeler si le rôle ou les permissions changent en cours de requête."""
    if hasattr(user, _CACHE_ATTR):
        delattr(user, _CACHE_ATTR)


# =========================================================
# DÉCORATEUR POUR VUES FONCTIONS
# =========================================================

def permission_required(module_code, action):
    """
    Protège une vue basée sur une fonction.

    Exemple :
        @permission_required("UTILISATEURS", "read")
        def ma_vue(request):
            ...
    """
    _validate_action(action)

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return _login_redirect(request)

            if has_module_permission(request.user, module_code, action):
                return view_func(request, *args, **kwargs)

            return _deny(request)

        return wrapper

    return decorator


# =========================================================
# MIXIN POUR CLASS-BASED VIEWS
# =========================================================

class ModulePermissionRequiredMixin:
    """
    Protège une Class-Based View avec RolePermission.
    Gère aussi la vérification de connexion : LoginRequiredMixin est inutile.

    Exemple :
        class ListUsersView(ModulePermissionRequiredMixin, ListView):
            permission_module = "UTILISATEURS"
            permission_action = "read"
    """

    permission_module = None
    permission_action = None
    permission_denied_message = (
        "Vous n'avez pas les permissions nécessaires "
        "pour accéder à cette fonctionnalité."
    )

    def get_permission_module(self):
        if not self.permission_module:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} doit définir 'permission_module'."
            )
        return self.permission_module

    def get_permission_action(self):
        if not self.permission_action:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} doit définir 'permission_action'."
            )
        _validate_action(self.permission_action)
        return self.permission_action

    def has_permission(self):
        return has_module_permission(
            self.request.user,
            self.get_permission_module(),
            self.get_permission_action(),
        )

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return _login_redirect(request)

        if not self.has_permission():
            return _deny(request, self.permission_denied_message)

        return super().dispatch(request, *args, **kwargs)