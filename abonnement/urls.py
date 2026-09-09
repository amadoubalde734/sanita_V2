from django.urls import path

from . import views

app_name = "abonnement"

urlpatterns = [

    # =====================================================
    # LICENCES
    # =====================================================
    path("", views.LicenseListView.as_view(), name="list"),
    path("ajouter/", views.LicenseCreateView.as_view(), name="add"),
    path("<int:pk>/", views.LicenseDetailView.as_view(), name="detail"),
    path("<int:pk>/modifier/", views.LicenseUpdateView.as_view(), name="edit"),
    path("<int:pk>/suspendre/", views.suspend_license, name="suspend"),
    path("<int:pk>/annuler/", views.cancel_license, name="cancel"),
    path("<int:pk>/activer/", views.activate_license, name="activate"),
    path("<int:pk>/renouveler/", views.renew_license, name="renew"),

    # =====================================================
    # PLANS D'ABONNEMENT
    # =====================================================
    path("plans/", views.PlanListView.as_view(), name="plans"),
    path("plans/ajouter/", views.PlanCreateView.as_view(), name="plan_add"),
    path("plans/<int:pk>/", views.PlanDetailView.as_view(), name="plan_detail"),
    path("plans/<int:pk>/modifier/", views.PlanUpdateView.as_view(), name="plan_edit"),
    path("plans/<int:pk>/toggle/", views.toggle_plan, name="plan_toggle"),

    # =====================================================
    # CONTRATS DE MAINTENANCE
    # =====================================================
    path("contrats/", views.MaintenanceContractListView.as_view(), name="contract_list"),
    path("contrats/ajouter/", views.MaintenanceContractCreateView.as_view(), name="contract_add"),
    path("contrats/<int:pk>/", views.MaintenanceContractDetailView.as_view(), name="contract_detail"),
    path("contrats/<int:pk>/modifier/", views.MaintenanceContractUpdateView.as_view(), name="contract_edit"),
    path("contrats/<int:pk>/suspendre/", views.suspend_contract, name="contract_suspend"),
    path("contrats/<int:pk>/annuler/", views.cancel_contract, name="contract_cancel"),
    path("contrats/<int:pk>/activer/", views.activate_contract, name="contract_activate"),
]