from django.urls import path
from . import views

app_name = "personnels"

urlpatterns = [
    # Dashboard
    path("", views.employe_dashboard, name="index"),
    path("dashboard/", views.employe_dashboard, name="dashboard"),

    # Employés
    path("employes/", views.employe_list, name="employe_list"),
    path("employes/ajouter/", views.employe_create, name="employe_create"),
    path("employes/<slug:slug>/modifier/", views.employe_update, name="employe_update"),
    path("employes/<slug:slug>/supprimer/", views.employe_delete, name="employe_delete"),

    # Profil & historique
    path("employes/<slug:slug>/profil/", views.employe_profil, name="employe_profil"),
    path("employes/<slug:slug>/historique/", views.employe_historique, name="employe_historique"),

    # Ayants droit
    path("ayants-droit/", views.ayant_droit_list, name="ayant_droit_list"),
    path("ayants-droit/ajouter/", views.ayant_droit_create, name="ayant_droit_create"),
    path("ayants-droit/ajouter/enfant/", views.enfant_create, name="enfant_create"),
    path("ayants-droit/ajouter/conjoint/", views.conjoint_create, name="conjoint_create"),
    path("ayants-droit/ajouter/autre/", views.autre_ayant_droit_create, name="autre_ayant_droit_create"),

    # AJAX
    path(
        "ajax/services/",
        views.get_services_by_departement,
        name="get_services_by_departement",
    ),
    path(
        "ajax/fonctions/",
        views.get_fonctions_by_service,
        name="get_fonctions_by_service",
    ),
]