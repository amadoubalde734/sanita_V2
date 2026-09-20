from django.shortcuts import render

# Create your views here.
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
)

from .models import Plan, License, MaintenanceContract
from .forms import LicenseForm, PlanForm, MaintenanceContractForm
from parametrage_general.models import ConfigurationEtablissement
from django.db.models import Q

# =========================================================
# ===================== LICENCES ==========================
# =========================================================


# =========================================================
# LISTE DES LICENCES
# =========================================================

class LicenseListView(LoginRequiredMixin, ListView):
    model = License
    template_name = "backend/administration/abonnement/list_licenses.html"
    context_object_name = "licenses"
    paginate_by = 20

    def get_queryset(self):
        queryset = License.objects.select_related(
            "etablissement",
            "plan",
            "created_by",
        ).order_by("-created_at")

        search = self.request.GET.get("search", "").strip()
        status = self.request.GET.get("status", "").strip()

        if search:
            queryset = queryset.filter(
                Q(license_key__icontains=search)
                | Q(etablissement__nom_etablissement__icontains=search)
            )

        if status:
            queryset = queryset.filter(status=status)

        # Mise à jour automatique des statuts
        for license in queryset:
            license.update_status()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_licenses = License.objects.all()

        context["total_licenses"] = all_licenses.count()
        context["active_licenses"] = all_licenses.filter(status=License.Status.ACTIVE).count()
        context["expiring_licenses"] = all_licenses.filter(status=License.Status.EXPIRING_SOON).count()
        context["expired_licenses"] = all_licenses.filter(status=License.Status.EXPIRED).count()
        context["status_choices"] = License.Status.choices
        context["current_search"] = self.request.GET.get("search", "")
        context["current_status"] = self.request.GET.get("status", "")

        return context


# =========================================================
# AJOUTER UNE LICENCE
# =========================================================

class LicenseCreateView(LoginRequiredMixin, CreateView):
    model = License
    form_class = LicenseForm
    template_name = "backend/administration/abonnement/add_license.html"

    def form_valid(self, form):
        form.instance.etablissement = ConfigurationEtablissement.objects.first()
        form.instance.created_by = self.request.user

        messages.success(
            self.request,
            "La licence a été créée avec succès."
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "abonnement:detail",
            kwargs={"pk": self.object.pk}
        )


# =========================================================
# DÉTAIL D'UNE LICENCE
# =========================================================

class LicenseDetailView(LoginRequiredMixin, DetailView):
    model = License
    template_name = "backend/administration/abonnement/detail_license.html"
    context_object_name = "license"

    def get_queryset(self):
        return License.objects.select_related(
            "etablissement",
            "plan",
            "created_by",
        )

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        # Mise à jour automatique du statut
        obj.update_status()

        return obj


# =========================================================
# MODIFIER UNE LICENCE
# =========================================================

class LicenseUpdateView(LoginRequiredMixin, UpdateView):
    model = License
    form_class = LicenseForm
    template_name = "backend/administration/abonnement/edit_license.html"
    context_object_name = "license"

    def form_valid(self, form):
        messages.success(
            self.request,
            "La licence a été modifiée avec succès."
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "abonnement:detail",
            kwargs={"pk": self.object.pk}
        )


# =========================================================
# SUSPENDRE UNE LICENCE
# =========================================================

def suspend_license(request, pk):
    license = get_object_or_404(License, pk=pk)

    license.status = License.Status.SUSPENDED
    license.save(update_fields=["status", "updated_at"])

    messages.warning(
        request,
        f"La licence {license.license_key} a été suspendue."
    )

    return redirect(
        "abonnement:detail",
        pk=license.pk
    )


# =========================================================
# ANNULER UNE LICENCE
# =========================================================

def cancel_license(request, pk):
    license = get_object_or_404(License, pk=pk)

    license.status = License.Status.CANCELLED
    license.save(update_fields=["status", "updated_at"])

    messages.warning(
        request,
        f"La licence {license.license_key} a été annulée."
    )

    return redirect(
        "abonnement:detail",
        pk=license.pk
    )


# =========================================================
# RÉACTIVER UNE LICENCE
# =========================================================

def activate_license(request, pk):
    license = get_object_or_404(License, pk=pk)

    license.status = License.Status.ACTIVE
    license.save(update_fields=["status", "updated_at"])

    # Vérification de la date d'expiration
    license.update_status()

    messages.success(
        request,
        f"La licence {license.license_key} a été réactivée."
    )

    return redirect(
        "abonnement:detail",
        pk=license.pk
    )


# =========================================================
# RENOUVELER UNE LICENCE
# =========================================================
# NOTE (non résolue, reportée telle quelle) : templates/backend/administration/
# abonnement/renew_license.html existe mais n'est rendu par aucune vue — celle-ci
# redirige directement sans jamais afficher de page de confirmation. Toujours en
# attente de la décision : GET (affiche renew_license.html) / POST (traite) ?

def renew_license(request, pk):
    license = get_object_or_404(License, pk=pk)

    if license.end_date:
        new_start_date = license.end_date + timedelta(days=1)
    else:
        new_start_date = timezone.localdate()

    license.start_date = new_start_date
    license.status = License.Status.ACTIVE

    license.save()

    messages.success(
        request,
        f"La licence {license.license_key} a été renouvelée avec succès."
    )

    return redirect(
        "abonnement:detail",
        pk=license.pk
    )


# =========================================================
# ======================= PLANS ===========================
# =========================================================


# =========================================================
# LISTE DES PLANS
# =========================================================

class PlanListView(LoginRequiredMixin, ListView):
    model = Plan
    template_name = "backend/administration/abonnement/list_plans.html"
    context_object_name = "plans"

    def get_queryset(self):
        return Plan.objects.all().prefetch_related(
            "licenses"
        ).order_by(
            "price",
            "name"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        plans = context["plans"]

        context["total_plans"] = plans.count()
        context["active_plans"] = plans.filter(active=True).count()
        context["inactive_plans"] = plans.filter(active=False).count()
        context["unlimited_user_plans"] = plans.filter(
            unlimited_users=True
        ).count()

        return context


# =========================================================
# AJOUTER UN PLAN
# =========================================================

class PlanCreateView(LoginRequiredMixin, CreateView):
    model = Plan
    form_class = PlanForm
    template_name = "backend/administration/abonnement/add_plan.html"

    def form_valid(self, form):
        messages.success(
            self.request,
            f"Le plan « {form.instance.name} » a été créé avec succès."
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("abonnement:plans")


# =========================================================
# DÉTAIL D'UN PLAN
# =========================================================

class PlanDetailView(LoginRequiredMixin, DetailView):
    model = Plan
    template_name = "backend/administration/abonnement/detail_plan.html"
    context_object_name = "plan"

    def get_queryset(self):
        return Plan.objects.prefetch_related(
            "licenses"
        )


# =========================================================
# MODIFIER UN PLAN
# =========================================================

class PlanUpdateView(LoginRequiredMixin, UpdateView):
    model = Plan
    form_class = PlanForm
    template_name = "backend/administration/abonnement/edit_plan.html"
    context_object_name = "plan"

    def form_valid(self, form):
        messages.success(
            self.request,
            f"Le plan « {form.instance.name} » a été modifié avec succès."
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "abonnement:plan_detail",
            kwargs={"pk": self.object.pk}
        )


# =========================================================
# ACTIVER / DÉSACTIVER UN PLAN
# =========================================================

def toggle_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk)

    plan.active = not plan.active
    plan.save(update_fields=["active", "updated_at"])

    if plan.active:
        messages.success(
            request,
            f"Le plan « {plan.name} » a été activé."
        )
    else:
        messages.warning(
            request,
            f"Le plan « {plan.name} » a été désactivé."
        )

    return redirect(
        "abonnement:plans"
    )


# =========================================================
# CONTRATS DE MAINTENANCE
# =========================================================

class MaintenanceContractListView(ListView):
    model = MaintenanceContract
    template_name = "backend/administration/abonnement/contrats/list_contracts.html"
    context_object_name = "contracts"
    paginate_by = 10

    def get_queryset(self):
        queryset = MaintenanceContract.objects.select_related(
            "etablissement",
            "license",
            "license__plan",
            "created_by",
        ).order_by("-created_at")

        search = self.request.GET.get("search", "").strip()

        if search:
            queryset = queryset.filter(
                Q(contract_number__icontains=search)
                | Q(etablissement__nom_etablissement__icontains=search)
                | Q(license__license_key__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = self.get_queryset()

        context["current_search"] = self.request.GET.get("search", "")

        context["total_contracts"] = queryset.count()

        context["active_contracts"] = queryset.filter(
            status=MaintenanceContract.Status.ACTIVE
        ).count()

        context["expiring_contracts"] = queryset.filter(
            status=MaintenanceContract.Status.EXPIRING_SOON
        ).count()

        context["expired_contracts"] = queryset.filter(
            status=MaintenanceContract.Status.EXPIRED
        ).count()

        return context


# =========================================================
# AJOUTER UN CONTRAT
# =========================================================

class MaintenanceContractCreateView(CreateView):
    model = MaintenanceContract
    form_class = MaintenanceContractForm
    template_name = "backend/administration/abonnement/contrats/add_contract.html"

    def form_valid(self, form):
        form.instance.etablissement = ConfigurationEtablissement.objects.first()
        form.instance.created_by = self.request.user

        messages.success(
            self.request,
            "Le contrat de maintenance a été créé avec succès."
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "abonnement:contract_detail",
            kwargs={"pk": self.object.pk},
        )


# =========================================================
# DÉTAIL D'UN CONTRAT
# =========================================================

class MaintenanceContractDetailView(DetailView):
    model = MaintenanceContract
    template_name = "backend/administration/abonnement/contrats/detail_contract.html"
    context_object_name = "contract"

    def get_object(self, queryset=None):
        contract = super().get_object(queryset)

        # Mise à jour automatique du statut
        contract.update_status()

        return contract


# =========================================================
# MODIFIER UN CONTRAT
# =========================================================

class MaintenanceContractUpdateView(UpdateView):
    model = MaintenanceContract
    form_class = MaintenanceContractForm
    template_name = "backend/administration/abonnement/contrats/edit_contract.html"

    def form_valid(self, form):

        messages.success(
            self.request,
            "Le contrat de maintenance a été modifié avec succès."
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "abonnement:contract_detail",
            kwargs={"pk": self.object.pk},
        )


# =========================================================
# SUSPENDRE UN CONTRAT
# =========================================================

def suspend_contract(request, pk):

    contract = get_object_or_404(
        MaintenanceContract,
        pk=pk,
    )

    contract.status = MaintenanceContract.Status.SUSPENDED
    contract.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    messages.warning(
        request,
        f"Le contrat {contract.contract_number} a été suspendu."
    )

    return redirect(
        "abonnement:contract_detail",
        pk=contract.pk,
    )


# =========================================================
# ANNULER UN CONTRAT
# =========================================================

def cancel_contract(request, pk):

    contract = get_object_or_404(
        MaintenanceContract,
        pk=pk,
    )

    contract.status = MaintenanceContract.Status.CANCELLED
    contract.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    messages.warning(
        request,
        f"Le contrat {contract.contract_number} a été annulé."
    )

    return redirect(
        "abonnement:contract_detail",
        pk=contract.pk,
    )


# =========================================================
# RÉACTIVER UN CONTRAT
# =========================================================

def activate_contract(request, pk):

    contract = get_object_or_404(
        MaintenanceContract,
        pk=pk,
    )

    contract.status = MaintenanceContract.Status.ACTIVE
    contract.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    contract.update_status()

    messages.success(
        request,
        f"Le contrat {contract.contract_number} a été réactivé."
    )

    return redirect(
        "abonnement:contract_detail",
        pk=contract.pk,
    )