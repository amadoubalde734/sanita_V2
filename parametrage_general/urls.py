from django.urls import path
from . import views

app_name = 'parametrage_general'

urlpatterns = [
    path('', views.index, name='index'),

    # ============================
    # CONFIGURATION ETABLISSEMENT
    # ============================
    path('configuration/', views.configuration_etablissement, name='configuration_etablissement'),
    path('configuration/modifier/', views.modifier_configuration_etablissement, name='modifier_configuration_etablissement'),

    # ============================
    # SOCIETES
    # ============================
    path('societes/liste/', views.liste_societes, name='liste_societes'),
    path('societes/ajouter/', views.ajouter_societe, name='ajouter_societe'),
    path('societes/modifier/<int:pk>/', views.modifier_societe, name='modifier_societe'),
    path('societes/supprimer/<int:pk>/', views.supprimer_societe, name='supprimer_societe'),

    # ============================
    # VILLES
    # ============================
    path('villes/liste/', views.liste_villes, name='liste_villes'),
    path('villes/ajouter/', views.ajouter_ville, name='ajouter_ville'),
    path('villes/modifier/<int:pk>/', views.modifier_ville, name='modifier_ville'),
    path('villes/supprimer/<int:pk>/', views.supprimer_ville, name='supprimer_ville'),

    # ============================
    # SITES
    # ============================
    path('sites/liste/', views.liste_sites, name='liste_sites'),
    path('sites/ajouter/', views.ajouter_site, name='ajouter_site'),
    path('sites/modifier/<int:pk>/', views.modifier_site, name='modifier_site'),
    path('sites/supprimer/<int:pk>/', views.supprimer_site, name='supprimer_site'),

    # ============================
    # UNITES MEDICALES
    # ============================
    path('unites-medicales/liste/', views.liste_unites_medicales, name='liste_unites_medicales'),
    path('unites-medicales/ajouter/', views.ajouter_unite_medicale, name='ajouter_unite_medicale'),
    path('unites-medicales/modifier/<int:pk>/', views.modifier_unite_medicale, name='modifier_unite_medicale'),
    path('unites-medicales/supprimer/<int:pk>/', views.supprimer_unite_medicale, name='supprimer_unite_medicale'),
    path('unites-medicales/toggle/<int:pk>/', views.toggle_unite_medicale, name='toggle_unite_medicale'),

    # ============================
    # DIRECTIONS
    # ============================
    path('directions/liste/', views.liste_directions, name='liste_directions'),
    path('directions/ajouter/', views.ajouter_direction, name='ajouter_direction'),
    path('directions/modifier/<int:pk>/', views.modifier_direction, name='modifier_direction'),
    path('directions/supprimer/<int:pk>/', views.supprimer_direction, name='supprimer_direction'),
    path('directions/toggle/<int:pk>/', views.toggle_direction, name='toggle_direction'),

    # ============================
    # DEPARTEMENTS
    # ============================
    path('departements/liste/', views.liste_departements, name='liste_departements'),
    path('departements/ajouter/', views.ajouter_departement, name='ajouter_departement'),
    path('departements/modifier/<int:pk>/', views.modifier_departement, name='modifier_departement'),
    path('departements/supprimer/<int:pk>/', views.supprimer_departement, name='supprimer_departement'),
    path('departements/toggle/<int:pk>/', views.toggle_departement, name='toggle_departement'),

    # ============================
    # SERVICES
    # ============================
    path('services/liste/', views.liste_services, name='liste_services'),
    path('services/ajouter/', views.ajouter_service, name='ajouter_service'),
    path('services/modifier/<int:pk>/', views.modifier_service, name='modifier_service'),
    path('services/supprimer/<int:pk>/', views.supprimer_service, name='supprimer_service'),

    # ============================
    # FONCTIONS
    # ============================
    path('fonctions/liste/', views.liste_fonctions, name='liste_fonctions'),
    path('fonctions/ajouter/', views.ajouter_fonction, name='ajouter_fonction'),
    path('fonctions/modifier/<int:pk>/', views.modifier_fonction, name='modifier_fonction'),
    path('fonctions/supprimer/<int:pk>/', views.supprimer_fonction, name='supprimer_fonction'),

    # ============================
    # SPECIALITES
    # ============================
    path('specialites/liste/', views.liste_specialites, name='liste_specialites'),
    path('specialites/ajouter/', views.ajouter_specialite, name='ajouter_specialite'),
    path('specialites/modifier/<int:pk>/', views.modifier_specialite, name='modifier_specialite'),
    path('specialites/supprimer/<int:pk>/', views.supprimer_specialite, name='supprimer_specialite'),
    path('specialites/toggle/<int:pk>/', views.toggle_specialite, name='toggle_specialite'),

    # ============================
    # EMAIL SETTINGS (optionnel)
    # ============================
    # path('email-settings/', views.email_settings, name='email_settings'),
]