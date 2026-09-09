from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .models import RolePermission


# =========================================================
# VÉRIFICATION D'UNE PERMISSION
# =========================================================

def has_module_permission(user, module_code, action):
    """
    Vérifie si un utilisateur possède une permission
    sur un module donné.

    Exemple :

        has_module_permission(
            user,
            "UTILISATEURS",
            "read"
        )

    Actions disponibles :

        create
        read
        update
        delete
        validate
        assign
    """

    # -----------------------------------------------------
    # UTILISATEUR NON CONNECTÉ
    # -----------------------------------------------------

    if not user or not user.is_authenticated:
        return False

    # -----------------------------------------------------
    # ADMINISTRATEUR
    # -----------------------------------------------------

    # L'administrateur possède tous les droits.
    if user.is_admin():
        return True

    # -----------------------------------------------------
    # VÉRIFICATION DU RÔLE
    # -----------------------------------------------------

    if not user.role_id:
        return False

    # -----------------------------------------------------
    # VÉRIFICATION DE L'ACTION
    # -----------------------------------------------------

    allowed_actions = {
        "create",
        "read",
        "update",
        "delete",
        "validate",
        "assign",
    }

    if action not in allowed_actions:
        return False

    # -----------------------------------------------------
    # VÉRIFICATION ROLE + MODULE + PERMISSION
    # -----------------------------------------------------

    permission_field = f"can_{action}"

    return RolePermission.objects.filter(
        role_id=user.role_id,
        module__code=module_code,
        module__active=True,
        **{
            permission_field: True,
        },
    ).exists()


# =========================================================
# DÉCORATEUR DE PERMISSION
# =========================================================

def permission_required(module_code, action):
    """
    Décorateur permettant de protéger une vue basée
    sur une fonction.

    Exemple :

        @permission_required(
            "UTILISATEURS",
            "read"
        )
        def ma_vue(request):
            ...
    """

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            # -------------------------------------------------
            # VÉRIFICATION
            # -------------------------------------------------

            if has_module_permission(
                request.user,
                module_code,
                action,
            ):
                return view_func(
                    request,
                    *args,
                    **kwargs,
                )

            # -------------------------------------------------
            # ACCÈS REFUSÉ
            # -------------------------------------------------

            messages.error(
                request,
                "Vous n'avez pas les permissions nécessaires "
                "pour effectuer cette action.",
            )

            return redirect("dashboard:index")

        return wrapper

    return decorator


# =========================================================
# MIXIN POUR CLASS-BASED VIEWS
# =========================================================

class ModulePermissionRequiredMixin:
    """
    Mixin permettant de protéger une Class-Based View
    avec RolePermission.

    Exemple :

        class ListUsersView(
            ModulePermissionRequiredMixin,
            LoginRequiredMixin,
            ListView,
        ):

            permission_module = "UTILISATEURS"
            permission_action = "read"
    """

    permission_module = None
    permission_action = None

    def dispatch(self, request, *args, **kwargs):

        # -------------------------------------------------
        # UTILISATEUR NON CONNECTÉ
        # -------------------------------------------------

        if not request.user.is_authenticated:
            return redirect("accounts:admin_login")

        # -------------------------------------------------
        # CONFIGURATION OBLIGATOIRE
        # -------------------------------------------------

        if not self.permission_module:
            messages.error(
                request,
                "Module de permission non configuré.",
            )

            return redirect("dashboard:index")

        if not self.permission_action:
            messages.error(
                request,
                "Action de permission non configurée.",
            )

            return redirect("dashboard:index")

        # -------------------------------------------------
        # VÉRIFICATION DE LA PERMISSION
        # -------------------------------------------------

        if has_module_permission(
            request.user,
            self.permission_module,
            self.permission_action,
        ):
            return super().dispatch(
                request,
                *args,
                **kwargs,
            )

        # -------------------------------------------------
        # ACCÈS REFUSÉ
        # -------------------------------------------------

        messages.error(
            request,
            "Vous n'avez pas les permissions nécessaires "
            "pour accéder à cette fonctionnalité.",
        )

        return redirect("dashboard:index")