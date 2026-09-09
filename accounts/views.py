import json
import random
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout as auth_logout,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.auth.models import Group
from django.contrib.sessions.models import Session

from django.core.mail import (
    EmailMessage,
    send_mail,
    get_connection,
)
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.db.models import Q
from django.http import JsonResponse

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.urls import reverse

from django.utils import timezone
from django.utils.encoding import (
    force_bytes,
    force_str,
)
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode,
)
from django.utils.timezone import now

from django.views import View
from django.views.generic import (
    ListView,
    FormView,
    TemplateView,
)

from django.contrib.sites.shortcuts import get_current_site


# =========================================================
# MODÈLES
# =========================================================

from accounts.models import (
    CustomUser,
    Role,
    Module,
    RolePermission,
)

from parametrage_general.models import (
    Societe,
    Ville,
    Site,
    EmailSettings,
)

# Le namespace 'administration' n'a pas de views.py propre : il est géré
# ici, par 'accounts' (cf. AdministrationIndexView tout en bas du fichier
# + config/urls.py qui monte accounts.urls une seconde fois sous
# namespace='administration' — il n'y a pas de administration/urls.py).
from abonnement.models import License, MaintenanceContract


# =========================================================
# FORMULAIRES
# =========================================================

from .forms import (
    RequestResetCodeForm,
    ResetPasswordWithCodeForm,
    CustomPasswordChangeForm,
    RoleForm,
)


# =========================================================
# UTILITAIRES
# =========================================================

from .utils import account_activation_token


# =========================================================
# PERMISSIONS
# =========================================================

from .permissions import ModulePermissionRequiredMixin
# =========================================================
# VALIDATION EMAIL
# =========================================================
# CORRIGÉ : accepte désormais un "user_id" optionnel (envoyé par le JS de
# add_user.html en mode édition) pour exclure l'utilisateur en cours de
# modification de la vérification d'unicité. Sans ça, éditer un utilisateur
# SANS changer son email déclenchait toujours "Email déjà utilisé" puisque
# la requête se retrouvait elle-même dans le filtre.

class EmailValidationView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get("email", "").strip()
            exclude_user_id = data.get("user_id")

            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({"email_error": "Email invalide"}, status=400)

            queryset = CustomUser.objects.filter(email=email)
            if exclude_user_id:
                queryset = queryset.exclude(pk=exclude_user_id)

            if queryset.exists():
                return JsonResponse({"email_error": "Email déjà utilisé"}, status=409)

            return JsonResponse({"email_valid": True})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Données invalides"}, status=400)


# =========================================================
# VALIDATION USERNAME
# =========================================================
# CORRIGÉ : même principe que EmailValidationView ci-dessus, avec
# exclude_user_id pour ne pas se bloquer soi-même en édition.

class UsernameValidationView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get("username", "").strip()
            exclude_user_id = data.get("user_id")

            if not username:
                return JsonResponse(
                    {"username_error": "Le nom d'utilisateur est obligatoire"}, status=400
                )

            if not str(username).isalnum():
                return JsonResponse(
                    {"username_error": "Utilisez uniquement des caractères alphanumériques"},
                    status=400
                )

            queryset = CustomUser.objects.filter(username=username)
            if exclude_user_id:
                queryset = queryset.exclude(pk=exclude_user_id)

            if queryset.exists():
                return JsonResponse({"username_error": "Nom d'utilisateur déjà utilisé"}, status=409)

            return JsonResponse({"username_valid": True})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Données invalides"}, status=400)


# =========================================================
# INSCRIPTION
# =========================================================

class RegistrationView(View):

    def get_template_name(self, request):
        if "front" in request.path:
            return "front/authentification_front/register_front.html"
        return "backend/authentification/register.html"

    def get(self, request):
        return render(request, self.get_template_name(request))

    def post(self, request):
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        next_url = request.POST.get("next", "index")

        context = {"fieldValues": request.POST}
        template_name = self.get_template_name(request)

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Nom d'utilisateur déjà utilisé.")
            return render(request, template_name, context)

        if email and CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email déjà utilisé.")
            return render(request, template_name, context)

        if len(password) < 6:
            messages.error(request, "Le mot de passe est trop court.")
            return render(request, template_name, context)

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_active = False
        user.save()

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        domain = get_current_site(request).domain

        link = reverse(
            "accounts:activate",
            kwargs={"uidb64": uidb64, "token": token},
        )
        activate_url = f"http://{domain}{link}?next={next_url}"

        email_subject = "Activez votre compte"
        email_body = (
            f"Bonjour {user.username},\n\n"
            f"Veuillez activer votre compte :\n"
            f"{activate_url}"
        )

        try:
            EmailMessage(
                email_subject,
                email_body,
                "noreply@monsite.com",
                [email],
            ).send()
        except Exception as e:
            messages.warning(request, f"Compte créé mais email non envoyé : {e}")

        messages.success(request, "Compte créé. Vérifiez votre email.")
        return render(request, template_name, context)


# =========================================================
# ACTIVATION COMPTE
# =========================================================

class VerificationView(View):

    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=user_id)

            if user.is_active:
                return redirect("accounts:admin_login")

            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save(update_fields=["is_active"])
                messages.success(request, "Compte activé avec succès.")
                return redirect("accounts:admin_login")

        except Exception:
            pass

        messages.error(request, "Lien invalide ou expiré.")
        return redirect("accounts:admin_login")


# =========================================================
# CONNEXION ADMIN
# =========================================================

class AdminLoginView(View):

    template_name = "backend/authentification/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/dashboard/")
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        # ✅ corrigé : conservé pour repré-remplir le champ "Identifiant"
        # en cas d'échec, cohérent avec RegistrationView qui fait déjà ça.
        # Sans ça, {{ fieldValues.username }} dans login.html restait
        # toujours vide après une tentative échouée.
        context = {"fieldValues": request.POST}

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.error(request, "⚠️ Identifiants invalides.")
            return render(request, self.template_name, context)

        if not user.is_active:
            messages.error(request, "⚠️ Votre compte est désactivé.")
            return render(request, self.template_name, context)

        login(request, user)

        user.statut_connecte = True
        user.save(update_fields=["statut_connecte"])

        # CORRIGÉ : la case "Se souvenir de moi" de login.html était purement
        # visuelle (aucun name= sur le champ, jamais lue côté serveur) — une
        # case à cocher qui ne fait rien n'est pas acceptable sur une page de
        # connexion. Décochée : la session expire à la fermeture du
        # navigateur. Cochée : elle suit SESSION_COOKIE_AGE (2 semaines par
        # défaut dans Django, sauf réglage différent dans settings.py).
        if request.POST.get("remember"):
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)

        messages.success(request, f"Bienvenue {user.username} 👋")

        # CORRIGÉ : un utilisateur marqué statut_change_pass=True (ex: compte
        # créé/réinitialisé par un administrateur) doit d'abord définir un
        # nouveau mot de passe avant d'accéder au tableau de bord.
        if user.statut_change_pass:
            return redirect("accounts:set_new_password")

        return redirect("/dashboard/")


# =========================================================
# CONNEXION FRONT
# =========================================================

class FrontLoginView(View):

    def get(self, request):
        return render(request, "front/authentification_front/login_front.html")

    def post(self, request):
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)

        if user and user.is_active:
            login(request, user)
            user.statut_connecte = True
            user.save(update_fields=["statut_connecte"])
            messages.success(request, f"Bienvenue {user.username} !")
            return redirect("/portail/")

        messages.error(request, "Identifiants invalides ou compte inactif.")
        return render(request, "front/authentification_front/login_front.html")


# =========================================================
# DECONNEXION
# =========================================================

class LogoutView(View):

    def post(self, request):
        user = request.user

        is_admin = "front" not in request.path

        if user.is_authenticated:
            user.statut_connecte = False
            user.save(update_fields=["statut_connecte"])

        auth_logout(request)
        messages.success(request, "Déconnecté avec succès.")

        if is_admin:
            return render(request, "backend/authentification/auth_logout.html")

        return render(request, "front/authentification_front/auth_logout.html")


# =========================================================
# AJOUT UTILISATEUR
# =========================================================

class AddUserView(LoginRequiredMixin, View):

    login_url = "accounts:admin_login"

    def get(self, request):
        societes = Societe.objects.all()
        villes = Ville.objects.all()
        sites = Site.objects.all()
        roles = Role.objects.filter(active=True).order_by("name")

        return render(
            request,
            "backend/authentification/add_user.html",
            {
                "societes": societes,
                "villes": villes,
                "sites": sites,
                "roles": roles,
            }
        )

    def post(self, request):
        nom = request.POST.get("nom", "").strip()
        login_name = request.POST.get("login", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        ville_id = request.POST.get("ville")
        site_id = request.POST.get("site")
        societe_id = request.POST.get("societe")
        contact = request.POST.get("contact", "").strip()
        role_id = request.POST.get("role")
        image = request.FILES.get("image")

        if CustomUser.objects.filter(username=login_name).exists():
            messages.error(request, "Login déjà utilisé.")
            return redirect("accounts:add_user")

        if email and CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email déjà utilisé.")
            return redirect("accounts:add_user")

        if len(password) < 6:
            messages.error(request, "Mot de passe trop court.")
            return redirect("accounts:add_user")

        if not role_id or not Role.objects.filter(pk=role_id, active=True).exists():
            messages.error(request, "Rôle sélectionné invalide.")
            return redirect("accounts:add_user")

        first_name = ""
        last_name = ""

        if nom:
            parts = nom.split(" ", 1)
            first_name = parts[0]
            if len(parts) > 1:
                last_name = parts[1]

        user = CustomUser(
            username=login_name,
            email=email or None,
            first_name=first_name,
            last_name=last_name,
            contact=contact,
            role_id=role_id,
            ville_id=ville_id or None,
            site_id=site_id or None,
            id_societe_id=societe_id or None,
        )
        user.set_password(password)

        if image:
            user.avatar = image

        user.save()

        messages.success(request, "Utilisateur créé avec succès.")
        return redirect("accounts:add_user")


# =========================================================
# MODIFICATION UTILISATEUR
# =========================================================

class EditUserView(LoginRequiredMixin, View):

    login_url = "accounts:admin_login"

    def get(self, request, user_id):
        user_instance = get_object_or_404(CustomUser, pk=user_id)

        societes = Societe.objects.all()
        villes = Ville.objects.all()
        sites = Site.objects.all()
        roles = Role.objects.filter(active=True).order_by("name")

        return render(
            request,
            "backend/authentification/add_user.html",
            {
                "user_instance": user_instance,
                "societes": societes,
                "villes": villes,
                "sites": sites,
                "roles": roles,
            }
        )

    def post(self, request, user_id):
        user_instance = get_object_or_404(CustomUser, pk=user_id)

        nom = request.POST.get("nom", "").strip()
        login_name = request.POST.get("login", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        ville_id = request.POST.get("ville")
        site_id = request.POST.get("site")
        societe_id = request.POST.get("societe")
        contact = request.POST.get("contact", "").strip()
        role_id = request.POST.get("role")
        image = request.FILES.get("image")

        if CustomUser.objects.exclude(pk=user_instance.pk).filter(username=login_name).exists():
            messages.error(request, "Login déjà utilisé.")
            return redirect("accounts:edit_user", user_id=user_id)

        if email and CustomUser.objects.exclude(pk=user_instance.pk).filter(email=email).exists():
            messages.error(request, "Email déjà utilisé.")
            return redirect("accounts:edit_user", user_id=user_id)

        if not role_id or not Role.objects.filter(pk=role_id, active=True).exists():
            messages.error(request, "Rôle sélectionné invalide.")
            return redirect("accounts:edit_user", user_id=user_id)

        first_name = ""
        last_name = ""

        if nom:
            parts = nom.split(" ", 1)
            first_name = parts[0]
            if len(parts) > 1:
                last_name = parts[1]

        user_instance.username = login_name
        user_instance.email = email or None
        user_instance.first_name = first_name
        user_instance.last_name = last_name
        user_instance.contact = contact
        user_instance.role_id = role_id
        user_instance.ville_id = ville_id or None
        user_instance.site_id = site_id or None
        user_instance.id_societe_id = societe_id or None

        if password:
            user_instance.set_password(password)

        if image:
            user_instance.avatar = image

        user_instance.save()

        messages.success(request, "Utilisateur modifié avec succès.")
        return redirect("accounts:list_users")


# =========================================================
# LISTE UTILISATEURS
# =========================================================
class ListUsersView(
    ModulePermissionRequiredMixin,
    LoginRequiredMixin,
    ListView,
):
    model = CustomUser
    template_name = "backend/authentification/list_users.html"
    context_object_name = "users"
    login_url = "accounts:admin_login"
    paginate_by = 20
    permission_module = "UTILISATEURS"
    permission_action = "read"

    def get_queryset(self):
        queryset = CustomUser.objects.select_related("ville", "site", "id_societe", "role").all()
        search = self.request.GET.get("q", "").strip()

        if search:
            queryset = queryset.filter(
                Q(username__icontains=search)
                | Q(email__icontains=search)
                | Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(contact__icontains=search)
            )

        return queryset.order_by("username")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_users = CustomUser.objects.all()

        context['search_query'] = self.request.GET.get("q", "")
        context['total_users'] = all_users.count()
        context['active_users'] = all_users.filter(statut_compte=True).count()
        context['inactive_users'] = all_users.filter(statut_compte=False).count()
        context['connected_users_count'] = all_users.filter(statut_connecte=True).count()
        return context


# =========================================================
# SUPPRESSION UTILISATEUR
# =========================================================

class DeleteUserView(LoginRequiredMixin, View):

    login_url = "accounts:admin_login"

    def post(self, request, user_id):
        if not request.user.is_admin():
            messages.error(request, "Accès refusé.")
            return redirect("accounts:list_users")

        user = get_object_or_404(CustomUser, id=user_id)

        if user.id == request.user.id:
            messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
            return redirect("accounts:list_users")

        user.delete()

        messages.success(request, "Utilisateur supprimé avec succès.")
        return redirect("accounts:list_users")


# =========================================================
# UTILISATEURS CONNECTÉS
# =========================================================

class ConnectedUsersView(LoginRequiredMixin, ListView):

    model = CustomUser
    template_name = "backend/authentification/connected_users.html"
    context_object_name = "users"
    login_url = "accounts:admin_login"

    def get_queryset(self):
        sessions = Session.objects.filter(expire_date__gte=now())
        user_ids = []

        for session in sessions:
            try:
                session_data = session.get_decoded()
                user_id = session_data.get("_auth_user_id")
                if user_id:
                    user_ids.append(user_id)
            except Exception:
                continue

        return CustomUser.objects.filter(id__in=user_ids).select_related("ville", "site", "id_societe")


# =========================================================
# CHANGEMENT MOT DE PASSE
# =========================================================

class ChangeUserPasswordView(LoginRequiredMixin, UserPassesTestMixin, FormView):

    template_name = "backend/authentification/change_password.html"
    form_class = CustomPasswordChangeForm
    login_url = "accounts:admin_login"

    def test_func(self):
        return self.request.user.is_admin()

    def get_user_target(self):
        user_id = self.kwargs.get("user_id")
        return get_object_or_404(CustomUser, id=user_id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.get_user_target()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_target"] = self.get_user_target()
        return context

    def form_valid(self, form):
        user = form.save()
        messages.success(
            self.request,
            f"Mot de passe modifié pour {user.get_full_name() or user.username}."
        )
        return redirect("accounts:list_users")

    def form_invalid(self, form):
        messages.error(self.request, "Veuillez corriger les erreurs.")
        return self.render_to_response(self.get_context_data(form=form))


# =========================================================
# NOUVEAU MOT DE PASSE OBLIGATOIRE (statut_change_pass)
# =========================================================
# Sert l'utilisateur lui-même (pas un admin qui modifie un autre compte,
# contrairement à ChangeUserPasswordView). Déclenchée par AdminLoginView
# quand user.statut_change_pass est True (ex: compte créé ou mot de passe
# réinitialisé par un administrateur) : l'utilisateur doit choisir un
# nouveau mot de passe avant d'accéder au tableau de bord.

class SetNewPasswordView(LoginRequiredMixin, FormView):

    template_name = "backend/authentification/set-newpassword.html"
    form_class = CustomPasswordChangeForm
    login_url = "accounts:admin_login"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()

        self.request.user.statut_change_pass = False
        self.request.user.save(update_fields=["statut_change_pass"])

        messages.success(self.request, "Mot de passe défini avec succès.")
        return redirect("/dashboard/")

    def form_invalid(self, form):
        messages.error(self.request, "Veuillez corriger les erreurs.")
        return self.render_to_response(self.get_context_data(form=form))


# =========================================================
# RÉINITIALISATION MOT DE PASSE - DEMANDE CODE
# =========================================================

class ResetCodeView(View):

    template_name_request = "backend/authentification/reset_request.html"
    template_name_reset = "backend/authentification/reset_password.html"
    code_validity_minutes = 15

    def get(self, request):
        form = RequestResetCodeForm()
        return render(request, self.template_name_request, {"form": form})

    def post(self, request):
        form = RequestResetCodeForm(request.POST)

        if not form.is_valid():
            return render(request, self.template_name_request, {"form": form})

        email = form.cleaned_data["email"]

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "Utilisateur non trouvé.")
            return render(request, self.template_name_request, {"form": form})

        code = str(random.randint(100000, 999999))
        user.reset_code = code
        user.reset_code_expiry = timezone.now() + timedelta(minutes=self.code_validity_minutes)
        user.save(update_fields=["reset_code", "reset_code_expiry"])

        try:
            email_config = EmailSettings.objects.first()

            if not email_config:
                messages.error(request, "Configuration email introuvable.")
                return render(request, self.template_name_request, {"form": form})

            connection = get_connection(
                backend=email_config.email_backend,
                host=email_config.email_host,
                port=email_config.email_port,
                username=email_config.email_host_user,
                password=email_config.email_host_password,
                use_tls=email_config.email_use_tls,
            )

            send_mail(
                subject="Code de réinitialisation FleetMining",
                message=(
                    f"Bonjour {user.username},\n\n"
                    f"Voici votre code de réinitialisation "
                    f"valable {self.code_validity_minutes} minutes : "
                    f"{code}\n\n"
                    f"Merci."
                ),
                from_email=email_config.default_from_email,
                recipient_list=[user.email],
                connection=connection,
                fail_silently=False,
            )

            messages.success(request, f"Code de réinitialisation envoyé à {user.email}.")

        except Exception as e:
            messages.error(request, f"Impossible d'envoyer l'email : {e}")
            return render(request, self.template_name_request, {"form": form})

        return redirect("accounts:reset_code_verify", user_id=user.id)


# =========================================================
# RÉINITIALISATION MOT DE PASSE - VALIDATION CODE
# =========================================================

class ResetPasswordWithCodeView(View):

    template_name = "backend/authentification/reset_password.html"

    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        form = ResetPasswordWithCodeForm(user=user)
        return render(request, self.template_name, {"form": form, "user_target": user})

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        form = ResetPasswordWithCodeForm(user=user, data=request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {"form": form, "user_target": user})

        code = form.cleaned_data["code"]

        if code != user.reset_code:
            messages.error(request, "Code incorrect.")
            return render(request, self.template_name, {"form": form, "user_target": user})

        if not user.reset_code_expiry or timezone.now() > user.reset_code_expiry:
            messages.error(request, "Le code a expiré. Veuillez demander un nouveau code.")
            return render(request, self.template_name, {"form": form, "user_target": user})

        form.save()
        user.reset_code = None
        user.reset_code_expiry = None
        user.save(update_fields=["reset_code", "reset_code_expiry"])

        messages.success(request, "Mot de passe réinitialisé avec succès.")
        return redirect("accounts:admin_login")


# =========================================================
# LISTE DES RÔLES
# =========================================================

class ListRolesView(LoginRequiredMixin, ListView):

    model = Role
    template_name = "backend/authentification/list_roles.html"
    context_object_name = "roles"
    login_url = "accounts:admin_login"
    paginate_by = 20

    def get_queryset(self):
        queryset = Role.objects.all()
        search = self.request.GET.get("q", "").strip()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(code__icontains=search)
            )

        return queryset.order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        # CORRIGÉ : menu.html attend 'roles_count' pour le badge du sous-menu
        # Rôles — n'était jamais fourni ici avant.
        context["roles_count"] = Role.objects.count()
        return context


# =========================================================
# AJOUT / MODIFICATION D'UN RÔLE (+ permissions)
# =========================================================

class RoleFormView(LoginRequiredMixin, UserPassesTestMixin, View):

    login_url = "accounts:admin_login"
    template_name = "backend/authentification/add_role.html"

    def test_func(self):
        return self.request.user.is_admin()

    def get_role(self, role_id):
        if role_id:
            return get_object_or_404(Role, pk=role_id)
        return None

    def get_permission_rows(self, role_instance, modules):
        """
        Construit une liste de tuples (module, permission_ou_None)
        prête à être bouclée dans le template, sans filtre custom.
        """
        existing = {}
        if role_instance:
            existing = {
                perm.module_id: perm
                for perm in role_instance.permissions.select_related("module")
            }
        return [(module, existing.get(module.id)) for module in modules]

    def get(self, request, role_id=None):
        role_instance = self.get_role(role_id)
        modules = Module.objects.filter(active=True).order_by("name")
        form = RoleForm(instance=role_instance)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "role_instance": role_instance,
                "permission_rows": self.get_permission_rows(role_instance, modules),
            },
        )

    def post(self, request, role_id=None):
        role_instance = self.get_role(role_id)
        modules = Module.objects.filter(active=True).order_by("name")
        form = RoleForm(request.POST, instance=role_instance)

        if not form.is_valid():
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "role_instance": role_instance,
                    "permission_rows": self.get_permission_rows(role_instance, modules),
                },
            )

        role_instance = form.save()

        for module in modules:
            RolePermission.objects.update_or_create(
                role=role_instance,
                module=module,
                defaults={
                    "can_create": f"perm_{module.id}_create" in request.POST,
                    "can_read": f"perm_{module.id}_read" in request.POST,
                    "can_update": f"perm_{module.id}_update" in request.POST,
                    "can_delete": f"perm_{module.id}_delete" in request.POST,
                    "can_validate": f"perm_{module.id}_validate" in request.POST,
                    "can_assign": f"perm_{module.id}_assign" in request.POST,
                },
            )

        messages.success(request, "Rôle enregistré avec succès.")
        return redirect("accounts:list_roles")

# =========================================================
# SUPPRESSION D'UN RÔLE
# =========================================================

class DeleteRoleView(LoginRequiredMixin, UserPassesTestMixin, View):

    login_url = "accounts:admin_login"

    def test_func(self):
        return self.request.user.is_admin()

    def post(self, request, role_id):
        role = get_object_or_404(Role, pk=role_id)

        if role.users.exists():
            messages.error(
                request,
                "Impossible de supprimer ce rôle : il est encore assigné à des utilisateurs.",
            )
            return redirect("accounts:list_roles")

        role.delete()
        messages.success(request, "Rôle supprimé avec succès.")
        return redirect("accounts:list_roles")


# =========================================================
# LISTE DES GROUPES
# =========================================================
# CORRIGÉ : il y avait DEUX définitions de ListGroupsView dans le fichier
# original (une sans UserPassesTestMixin utilisant 'groups_count', une avec
# UserPassesTestMixin utilisant 'total_groups'). Python ne gardait que la
# seconde silencieusement -> la première était du code mort. Cette version
# fusionne les deux : garde UserPassesTestMixin (contrôle d'accès) et fournit
# à la fois 'total_groups' ET 'groups_count'.

class ListGroupsView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = Group
    template_name = "backend/authentification/group/list_groups.html"
    context_object_name = "groups"
    login_url = "accounts:admin_login"
    paginate_by = 20

    def test_func(self):
        return self.request.user.is_admin()

    def get_queryset(self):
        queryset = (
            Group.objects
            .prefetch_related("fleet_users")
            .order_by("name")
        )

        search = self.request.GET.get("q", "").strip()

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search_query"] = self.request.GET.get("q", "")
        context["total_groups"] = Group.objects.count()
        context["groups_count"] = context["total_groups"]

        return context


# =========================================================
# AJOUT / MODIFICATION D'UN GROUPE
# =========================================================

class GroupFormView(LoginRequiredMixin, UserPassesTestMixin, View):

    login_url = "accounts:admin_login"
    template_name = "backend/authentification/group/add_group.html"

    def test_func(self):
        return self.request.user.is_admin()

    def get_group(self, group_id):
        if group_id:
            return get_object_or_404(Group, pk=group_id)

        return None

    def get(self, request, group_id=None):

        group_instance = self.get_group(group_id)

        users = (
            CustomUser.objects
            .filter(statut_compte=True)
            .select_related(
                "role",
                "ville",
                "site",
                "id_societe",
            )
            .order_by("username")
        )

        selected_user_ids = []

        if group_instance:
            selected_user_ids = list(
                group_instance.fleet_users.values_list(
                    "id",
                    flat=True
                )
            )

        return render(
            request,
            self.template_name,
            {
                "group_instance": group_instance,
                "users": users,
                "selected_user_ids": selected_user_ids,
            },
        )

    def post(self, request, group_id=None):

        group_instance = self.get_group(group_id)

        name = request.POST.get("name", "").strip()

        if not name:
            messages.error(
                request,
                "Le nom du groupe est obligatoire."
            )

            if group_instance:
                return redirect(
                    "accounts:edit_group",
                    group_id=group_instance.id
                )

            return redirect(
                "accounts:add_group"
            )

        existing = Group.objects.filter(
            name__iexact=name
        )

        if group_instance:
            existing = existing.exclude(
                pk=group_instance.pk
            )

        if existing.exists():

            messages.error(
                request,
                "Un groupe portant ce nom existe déjà."
            )

            if group_instance:
                return redirect(
                    "accounts:edit_group",
                    group_id=group_instance.id
                )

            return redirect(
                "accounts:add_group"
            )

        # -------------------------------------------------
        # CRÉATION / MODIFICATION
        # -------------------------------------------------

        if group_instance:

            group = group_instance
            group.name = name
            group.save()

            message = "Groupe modifié avec succès."

        else:

            group = Group.objects.create(
                name=name
            )

            message = "Groupe créé avec succès."

        # -------------------------------------------------
        # UTILISATEURS DU GROUPE
        # -------------------------------------------------

        user_ids = request.POST.getlist("users")

        users = CustomUser.objects.filter(
            id__in=user_ids,
            statut_compte=True,
        )

        # IMPORTANT :
        # related_name="fleet_users"
        group.fleet_users.set(users)

        messages.success(
            request,
            message
        )

        return redirect(
            "accounts:list_groups"
        )


# =========================================================
# SUPPRESSION D'UN GROUPE
# =========================================================

class DeleteGroupView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    View
):

    login_url = "accounts:admin_login"

    def test_func(self):
        return self.request.user.is_admin()

    def post(self, request, group_id):

        group = get_object_or_404(
            Group,
            pk=group_id
        )

        group.delete()

        messages.success(
            request,
            "Groupe supprimé avec succès."
        )

        return redirect(
            "accounts:list_groups"
        )


# =========================================================
# LISTE DES MODULES
# =========================================================

class ListModulesView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    ListView
):

    model = Module
    template_name = "backend/authentification/modules/list_modules.html"
    context_object_name = "modules"
    login_url = "accounts:admin_login"
    paginate_by = 20

    def test_func(self):
        return self.request.user.is_admin()

    def get_queryset(self):

        queryset = Module.objects.all().order_by("name")

        search = self.request.GET.get("q", "").strip()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(code__icontains=search)
                | Q(description__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        all_modules = Module.objects.all()

        context["search_query"] = self.request.GET.get("q", "")
        context["total_modules"] = all_modules.count()
        context["active_modules"] = all_modules.filter(
            active=True
        ).count()
        context["inactive_modules"] = all_modules.filter(
            active=False
        ).count()
        # CORRIGÉ : menu.html attend 'modules_count' pour le badge du
        # sous-menu Modules — n'était jamais fourni sous ce nom avant.
        context["modules_count"] = context["total_modules"]

        return context


# =========================================================
# AJOUT / MODIFICATION D'UN MODULE
# =========================================================

class ModuleFormView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    View
):

    login_url = "accounts:admin_login"
    template_name = "backend/authentification/modules/add_module.html"

    def test_func(self):
        return self.request.user.is_admin()

    def get_module(self, module_id):

        if module_id:
            return get_object_or_404(
                Module,
                pk=module_id
            )

        return None

    def get(self, request, module_id=None):

        module_instance = self.get_module(module_id)

        return render(
            request,
            self.template_name,
            {
                "module_instance": module_instance,
            }
        )

    def post(self, request, module_id=None):

        module_instance = self.get_module(module_id)

        code = request.POST.get(
            "code",
            ""
        ).strip()

        name = request.POST.get(
            "name",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        active = request.POST.get("active") == "on"

        # -------------------------------------------------
        # VALIDATION CODE
        # -------------------------------------------------

        if not code:

            messages.error(
                request,
                "Le code du module est obligatoire."
            )

            return render(
                request,
                self.template_name,
                {
                    "module_instance": module_instance,
                    "code": code,
                    "name": name,
                    "description": description,
                    "active": active,
                }
            )

        # -------------------------------------------------
        # VALIDATION NOM
        # -------------------------------------------------

        if not name:

            messages.error(
                request,
                "Le nom du module est obligatoire."
            )

            return render(
                request,
                self.template_name,
                {
                    "module_instance": module_instance,
                    "code": code,
                    "name": name,
                    "description": description,
                    "active": active,
                }
            )

        # -------------------------------------------------
        # VÉRIFICATION DOUBLON CODE
        # -------------------------------------------------

        existing_code = Module.objects.filter(
            code__iexact=code
        )

        if module_instance:

            existing_code = existing_code.exclude(
                pk=module_instance.pk
            )

        if existing_code.exists():

            messages.error(
                request,
                "Un module utilisant ce code existe déjà."
            )

            return render(
                request,
                self.template_name,
                {
                    "module_instance": module_instance,
                    "code": code,
                    "name": name,
                    "description": description,
                    "active": active,
                }
            )

        # -------------------------------------------------
        # VÉRIFICATION DOUBLON NOM
        # -------------------------------------------------

        existing_name = Module.objects.filter(
            name__iexact=name
        )

        if module_instance:

            existing_name = existing_name.exclude(
                pk=module_instance.pk
            )

        if existing_name.exists():

            messages.error(
                request,
                "Un module portant ce nom existe déjà."
            )

            return render(
                request,
                self.template_name,
                {
                    "module_instance": module_instance,
                    "code": code,
                    "name": name,
                    "description": description,
                    "active": active,
                }
            )

        # -------------------------------------------------
        # CRÉATION
        # -------------------------------------------------

        if module_instance:

            module = module_instance

            module.code = code
            module.name = name
            module.description = description
            module.active = active

            module.save()

            message = "Module modifié avec succès."

        # -------------------------------------------------
        # NOUVEAU MODULE
        # -------------------------------------------------

        else:

            module = Module.objects.create(
                code=code,
                name=name,
                description=description,
                active=active,
            )

            message = "Module créé avec succès."

        messages.success(
            request,
            message
        )

        return redirect(
            "accounts:list_modules"
        )


# =========================================================
# SUPPRESSION D'UN MODULE
# =========================================================

class DeleteModuleView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    View
):

    login_url = "accounts:admin_login"

    def test_func(self):
        return self.request.user.is_admin()

    def post(self, request, module_id):

        module = get_object_or_404(
            Module,
            pk=module_id
        )

        # -------------------------------------------------
        # VÉRIFIER SI LE MODULE EST UTILISÉ
        # -------------------------------------------------

        if RolePermission.objects.filter(
            module=module
        ).exists():

            messages.error(
                request,
                "Impossible de supprimer ce module : "
                "il est utilisé dans les permissions d'un ou plusieurs rôles."
            )

            return redirect(
                "accounts:list_modules"
            )

        # -------------------------------------------------
        # SUPPRESSION
        # -------------------------------------------------

        module.delete()

        messages.success(
            request,
            "Module supprimé avec succès."
        )

        return redirect(
            "accounts:list_modules"
        )


# =========================================================
# TABLEAU DE BORD ADMINISTRATION (namespace 'administration')
# =========================================================
# IMPORTANT : accounts/urls.py importe AdministrationIndexView et l'utilise
# pour path("", ...). Sans cette classe dans ce fichier, le simple import
# de accounts/urls.py lève une ImportError et TOUT le site plante (plus
# aucune route ne se charge, même /accounts/... et /administration/...).
# Le module Administration n'a pas de logique propre : config/urls.py monte
# accounts.urls une seconde fois sous namespace='administration' (pas de
# administration/urls.py séparé). Cette vue agrège les données 'accounts'
# (utilisateurs, rôles, modules, groupes) et 'abonnement' (licences,
# contrats de maintenance) pour templates/administration/index.html.

class AdministrationIndexView(LoginRequiredMixin, TemplateView):
    template_name = "administration/index.html"
    login_url = "accounts:admin_login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        users_qs = CustomUser.objects.all()
        context["total_users"] = users_qs.count()
        context["active_users"] = users_qs.filter(statut_compte=True).count()
        context["connected_users_count"] = users_qs.filter(statut_connecte=True).count()
        context["recent_users"] = users_qs.select_related("role").order_by("-date_creation")[:5]

        context["roles_count"] = Role.objects.count()

        modules_qs = Module.objects.all()
        context["total_modules"] = modules_qs.count()
        context["active_modules"] = modules_qs.filter(active=True).count()
        context["modules_count"] = context["total_modules"]

        context["groups_count"] = Group.objects.count()

        # NOTE : le champ `status` de License/MaintenanceContract n'est
        # rafraîchi que lorsqu'une instance est chargée via update_status()
        # (cf. abonnement/views.py) -> ces compteurs peuvent être légèrement
        # obsolètes tant qu'aucune tâche planifiée ne rafraîchit le statut
        # de toutes les licences/contrats chaque jour.
        licenses_qs = License.objects.all()
        context["licenses_active"] = licenses_qs.filter(status=License.Status.ACTIVE).count()
        context["licenses_expiring_soon"] = licenses_qs.filter(status=License.Status.EXPIRING_SOON).count()
        context["licenses_expired"] = licenses_qs.filter(
            status__in=[License.Status.EXPIRED, License.Status.SUSPENDED, License.Status.CANCELLED]
        ).count()
        context["licenses_watchlist"] = (
            licenses_qs.filter(status__in=[License.Status.EXPIRING_SOON, License.Status.EXPIRED])
            .select_related("societe", "plan")
            .order_by("end_date")[:5]
        )

        contracts_qs = MaintenanceContract.objects.all()
        context["contracts_active"] = contracts_qs.filter(status=MaintenanceContract.Status.ACTIVE).count()
        context["contracts_expiring_soon"] = contracts_qs.filter(
            status=MaintenanceContract.Status.EXPIRING_SOON
        ).count()

        return context