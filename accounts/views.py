import json
import random
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout as auth_logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.sessions.models import Session
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import (
    EmailMessage,
    send_mail,
    get_connection,
)
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
)

from validate_email import validate_email

from .forms import (
    RequestResetCodeForm,
    ResetPasswordWithCodeForm,
    CustomPasswordChangeForm,
)
from .models import (
    CustomUser,
    Role,
)
from .utils import account_activation_token

from accounts.models import CustomUser
from parametrage_general.models import (
    Societe,
    EmailSettings,
)
from parametrage_general.models import (
    Ville,
    Site,
)

# -----------------------------------------
# Validation
# -----------------------------------------

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email invalide'}, status=400)
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email déjà utilisé'}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Utilisez uniquement des caractères alphanumériques'}, status=400)
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Nom d’utilisateur déjà utilisé'}, status=409)
        return JsonResponse({'username_valid': True})

# -----------------------------------------
# Inscription
# -----------------------------------------

class RegistrationView(View):
    def get_template_name(self, request):
        return 'front/authentification_front/register_front.html' if 'front' in request.path else 'admin/authentification/register.html'

    def get(self, request):
        return render(request, self.get_template_name(request))

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url = request.POST.get('next', 'index')

        context = {'fieldValues': request.POST}
        template_name = self.get_template_name(request)

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Nom d’utilisateur déjà utilisé.')
            return render(request, template_name, context)

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email déjà utilisé.')
            return render(request, template_name, context)

        if len(password) < 6:
            messages.error(request, 'Le mot de passe est trop court.')
            return render(request, template_name, context)

        user = CustomUser.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        domain = get_current_site(request).domain
        link = reverse('accounts:activate', kwargs={'uidb64': uidb64, 'token': token})
        activate_url = f'http://{domain}{link}?next={next_url}'

        email_subject = 'Activez votre compte'
        email_body = f'Bonjour {user.username},\n\nVeuillez activer votre compte :\n{activate_url}'
        EmailMessage(email_subject, email_body, 'noreply@monsite.com', [email]).send()

        messages.success(request, 'Compte créé. Vérifiez votre email.')
        return render(request, template_name)

# -----------------------------------------
# Activation
# -----------------------------------------

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=id)

            if user.is_active:
                return redirect('accounts:admin_login')

            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                messages.success(request, 'Compte activé.')
                return redirect('accounts:admin_login')
        except Exception:
            pass

        messages.error(request, 'Lien invalide ou expiré.')
        return redirect('accounts:admin_login')

# -----------------------------------------
# Connexion admin
# -----------------------------------------

class AdminLoginView(View):
    template_name = "backend/authentification/login.html"

    # Rôles orientés risques
    ROLES_RISQUES = {
        "qse",
        "digital_qse",
        "qse_team",
        "responsable_processus",
        "referent_processus",
        "responsable_action",
        "controle_interne",
        "top_management",
        "audit",
    }

    def get(self, request):
        """
        Si l'utilisateur est déjà connecté,
        on le redirige directement selon son rôle.
        """
        if request.user.is_authenticated:
            return self.redirect_by_role(request.user)

        return render(request, self.template_name)

    def post(self, request):
        """
        Authentification utilisateur.
        """
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.error(request, "⚠️ Identifiants invalides.")
            return render(request, self.template_name)

        if not user.is_active:
            messages.error(request, "⚠️ Votre compte est désactivé.")
            return render(request, self.template_name)

        login(request, user)
        messages.success(request, f"Bienvenue {user.username} 👋")

        return self.redirect_by_role(user)

    def redirect_by_role(self, user):
        """
        Redirection selon le rôle.
        """
        role_code = user.role_code

        if role_code == "administrateur":
            return redirect("/dashboard/")

        if role_code in self.ROLES_RISQUES:
            return redirect("/dashboard/risks/index/")

        return redirect("/dashboard/")

# -----------------------------------------
# Connexion front
# -----------------------------------------

class FrontLoginView(View):
    def get(self, request):
        return render(request, 'front/authentification_front/login_front.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} !')
            return redirect('/portail/')
        messages.error(request, 'Identifiants invalides ou compte inactif.')
        return render(request, 'front/authentification_front/login_front.html')


# -----------------------------------------
# Déconnexion
# -----------------------------------------

class LogoutView(View):

    def post(self, request):

        # Déterminer le type de connexion avant de fermer la session
        is_admin = 'admin' in request.path
        # Déconnexion Django
        auth_logout(request)
        messages.success(request, 'Déconnecté avec succès.')

        # Page de déconnexion admin
        if is_admin:
            return render(
                request,
                'backend/authentification/auth_logout.html'
            )
        # Page de déconnexion front
        return render(
            request,
            'front/authentification_front/auth_logout.html'
        )
# -----------------------------------------
# Adduser
# -----------------------------------------

class AddUserViews(View):

    def get(self, request):
        societes = Societe.objects.all()
        villes = Ville.objects.all()
        sites = Site.objects.all()

        # liste des rôles depuis la table Role
        role_choices = Role.objects.filter(active=True)

        return render(request, 'backend/authentification/add_user.html', {
            'societes': societes,
            'villes': villes,
            'sites': sites,
            'role_choices': role_choices,
        })

    def post(self, request):
        nom = request.POST.get('nom', '').strip()
        login = request.POST.get('login', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        ville_id = request.POST.get('ville')
        site_id = request.POST.get('site')
        societe_id = request.POST.get('societe')
        contact = request.POST.get('contact', '').strip()

        # ici on récupère ID role (FK)
        role_id = request.POST.get('role')

        image = request.FILES.get('image')

        # ---------------------------
        # VALIDATIONS
        # ---------------------------
        if CustomUser.objects.filter(username=login).exists():
            messages.error(request, "Login déjà utilisé.")
            return redirect('accounts:add_user')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email déjà utilisé.")
            return redirect('accounts:add_user')

        if len(password) < 6:
            messages.error(request, "Mot de passe trop court.")
            return redirect('accounts:add_user')

        # validation role via table Role
        if not Role.objects.filter(id=role_id, active=True).exists():
            messages.error(request, "Rôle invalide.")
            return redirect('accounts:add_user')

        role_obj = Role.objects.get(id=role_id)

        # ---------------------------
        # NOM / PRENOM
        # ---------------------------
        first_name, last_name = '', ''
        if nom:
            parts = nom.split(' ', 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ''

        # ---------------------------
        # CREATION USER
        # ---------------------------
        user = CustomUser(
            username=login,
            email=email,
            first_name=first_name,
            last_name=last_name,
            contact=contact,

            # IMPORTANT : FK ROLE
            role=role_obj,

            ville_id=ville_id or None,
            site_id=site_id or None,
            id_societe_id=societe_id or None,
        )

        user.set_password(password)

        if image:
            user.avatar = image

        user.save()

        messages.success(request, "Utilisateur créé avec succès.")
        return redirect('accounts:add_user')

# -----------------------------------------
# Edit d'utilisateur (Admin)
# -----------------------------------------

class EditUserView(View):

    def get(self, request, user_id):
        user_instance = get_object_or_404(CustomUser, pk=user_id)

        societes = Societe.objects.all()
        villes = Ville.objects.all()
        sites = Site.objects.all()

        # Rôles depuis la base
        roles = Role.objects.filter(active=True)

        return render(
            request,
            'backend/authentification/add_user.html',
            {
                'user_instance': user_instance,
                'societes': societes,
                'villes': villes,
                'sites': sites,
                'roles': roles,
            }
        )

    def post(self, request, user_id):
        user_instance = get_object_or_404(CustomUser, pk=user_id)

        nom = request.POST.get('nom', '').strip()
        login = request.POST.get('login', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        ville_id = request.POST.get('ville')
        site_id = request.POST.get('site')
        societe_id = request.POST.get('societe')

        contact = request.POST.get('contact', '').strip()

        role_id = request.POST.get('role')

        image = request.FILES.get('image')

        # Vérification login
        if CustomUser.objects.exclude(pk=user_instance.id).filter(username=login).exists():
            messages.error(request, "Login déjà utilisé.")
            return redirect('accounts:edit_user', user_id=user_id)

        # Vérification email
        if CustomUser.objects.exclude(pk=user_instance.id).filter(email=email).exists():
            messages.error(request, "Email déjà utilisé.")
            return redirect('accounts:edit_user', user_id=user_id)

        # Récupération rôle
        role = get_object_or_404(Role, id=role_id, active=True)

        # Découpage nom
        first_name = ''
        last_name = ''

        if nom:
            parts = nom.split(' ', 1)
            first_name = parts[0]
            if len(parts) > 1:
                last_name = parts[1]

        # Mise à jour utilisateur
        user_instance.username = login
        user_instance.email = email
        user_instance.first_name = first_name
        user_instance.last_name = last_name
        user_instance.contact = contact

        # IMPORTANT : on affecte l'objet Role et non le code texte
        user_instance.role = role

        user_instance.ville_id = ville_id or None
        user_instance.site_id = site_id or None
        user_instance.id_societe_id = societe_id or None

        if password:
            user_instance.set_password(password)

        if image:
            user_instance.avatar = image

        user_instance.save()

        messages.success(request, "Utilisateur modifié avec succès.")
        return redirect('accounts:list_users')

# -----------------------------------------
# Utilisateurs connectés
# -----------------------------------------

class ConnectedUsersView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'backend/authentification/connected_users.html'
    context_object_name = 'users'

    def get_queryset(self):
        # Récupérer les sessions valides
        sessions = Session.objects.filter(expire_date__gte=now())
        user_ids = [
            session.get_decoded().get('_auth_user_id')
            for session in sessions
            if session.get_decoded().get('_auth_user_id')
        ]
        # Récupérer les utilisateurs connectés avec select_related
        return CustomUser.objects.filter(id__in=user_ids).select_related('ville', 'site', 'id_societe')


# -----------------------------------------
# Changement de mot de passe
# -----------------------------------------

class ChangeUserPasswordView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'backend/authentification/change_password.html'
    form_class = CustomPasswordChangeForm

    def test_func(self):
        # Seuls les administrateurs peuvent changer le mot de passe
        return self.request.user.role == 'administrateur'

    def get_user_target(self):
        user_id = self.kwargs.get('user_id')
        return get_object_or_404(CustomUser, id=user_id)

    def get_form(self, form_class=None):
        # Passe l'utilisateur cible au formulaire
        return self.form_class(user=self.get_user_target(), **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_target'] = self.get_user_target()
        return context

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f"Mot de passe modifié pour {user.get_full_name()}.")
        return redirect('accounts:list_users')

    def form_invalid(self, form):
        messages.error(self.request, "Veuillez corriger les erreurs.")
        return self.render_to_response(self.get_context_data(form=form))


# -----------------------------------------
# liste users
# -----------------------------------------

class ListUsersView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'backend/authentification/list_users.html'
    context_object_name = 'users'
    login_url = 'accounts:admin_login'
    paginate_by = 20

    def get_queryset(self):
        """
        Récupère tous les utilisateurs avec leurs relations Ville, Site, Société.
        Optionnel : filtrage par recherche.
        """
        queryset = CustomUser.objects.select_related('ville', 'site', 'id_societe').all()
        search = self.request.GET.get('q', None)
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        return queryset.order_by('username')


# -----------------------------------------
# supprimer user
# -----------------------------------------

class DeleteUserView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        # Vérification du rôle
        if request.user.role != 'administrateur':
            messages.error(request, "Accès refusé.")
            return redirect('accounts:list_users')

        # Récupération et suppression de l'utilisateur
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        messages.success(request, "Utilisateur supprimé avec succès.")
        return redirect('accounts:list_users')

# ----------------------------------------
# Vue pour demander un code de réinitialisation avec durée de validité
# ----------------------------------------

class ResetCodeView(View):
    template_name_request = 'backend/authentification/reset_request.html'
    template_name_reset = 'backend/authentification/reset_password.html'
    code_validity_minutes = 15

    def get(self, request):
        form = RequestResetCodeForm()
        return render(request, self.template_name_request, {'form': form})

    def post(self, request):
        form = RequestResetCodeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                messages.error(request, "Utilisateur non trouvé.")
                return render(request, self.template_name_request, {'form': form})

            # Générer un code temporaire et définir l'expiration
            code = str(random.randint(100000, 999999))
            user.reset_code = code
            user.reset_code_expiry = timezone.now() + timedelta(minutes=self.code_validity_minutes)
            user.save()

            # Envoyer l'email avec le code
            try:
                email_config = EmailSettings.objects.first()
                if not email_config:
                    messages.error(request, "Configuration email introuvable.")
                    return render(request, self.template_name_request, {'form': form})

                connection = get_connection(
                    backend=email_config.email_backend,
                    host=email_config.email_host,
                    port=email_config.email_port,
                    username=email_config.email_host_user,
                    password=email_config.email_host_password,
                    use_tls=email_config.email_use_tls,
                )

                send_mail(
                    subject="Code de réinitialisation QSE360",
                    message=f"Bonjour {user.username},\n\nVoici votre code de réinitialisation valable {self.code_validity_minutes} minutes : {code}\n\nMerci.",
                    from_email=email_config.default_from_email,
                    recipient_list=[user.email],
                    connection=connection,
                    fail_silently=False,
                )
                messages.success(request, f"Code de réinitialisation envoyé à {user.email}.")
            except Exception as e:
                messages.error(request, f"Impossible d'envoyer l'email: {e}")

            return redirect('accounts:reset_code_verify', user_id=user.id)

        return render(request, self.template_name_request, {'form': form})

# ----------------------------------------
# Vue pour réinitialiser le mot de passe avec code
# ----------------------------------------

class ResetPasswordWithCodeView(View):
    template_name = 'backend/authentification/reset_password.html'

    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        form = ResetPasswordWithCodeForm(user=user)
        return render(request, self.template_name, {'form': form, 'user_target': user})

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        form = ResetPasswordWithCodeForm(user=user, data=request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code != user.reset_code:
                messages.error(request, "Code incorrect.")
                return render(request, self.template_name, {'form': form, 'user_target': user})

            # Réinitialiser le mot de passe
            form.save()
            user.reset_code = None
            user.save()
            messages.success(request, "Mot de passe réinitialisé avec succès.")
            return redirect('accounts:admin_login')

        return render(request, self.template_name, {'form': form, 'user_target': user})