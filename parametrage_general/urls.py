from django.urls import path
from . import views

app_name = 'parametrage_general'

urlpatterns = [
    path('', views.index, name='index'),

    path('configuration/', views.configuration_etablissement, name='configuration_etablissement'),
    path('configuration/modifier/', views.modifier_configuration_etablissement, name='modifier_configuration_etablissement'),

    path('societes/liste/', views.liste_societes, name='liste_societes'),
    path('societes/ajouter/', views.ajouter_societe, name='ajouter_societe'),
    path('societes/modifier/<int:pk>/', views.modifier_societe, name='modifier_societe'),
    path('societes/supprimer/<int:pk>/', views.supprimer_societe, name='supprimer_societe'),

    path('villes/liste/', views.liste_villes, name='liste_villes'),
    path('villes/ajouter/', views.ajouter_ville, name='ajouter_ville'),
    path('villes/modifier/<int:pk>/', views.modifier_ville, name='modifier_ville'),
    path('villes/supprimer/<int:pk>/', views.supprimer_ville, name='supprimer_ville'),

    path('sites/liste/', views.liste_sites, name='liste_sites'),
    path('sites/ajouter/', views.ajouter_site, name='ajouter_site'),
    path('sites/modifier/<int:pk>/', views.modifier_site, name='modifier_site'),
    path('sites/supprimer/<int:pk>/', views.supprimer_site, name='supprimer_site'),

    path('unites-medicales/liste/', views.liste_unites_medicales, name='liste_unites_medicales'),
    path('unites-medicales/ajouter/', views.ajouter_unite_medicale, name='ajouter_unite_medicale'),
    path('unites-medicales/modifier/<int:pk>/', views.modifier_unite_medicale, name='modifier_unite_medicale'),
    path('unites-medicales/supprimer/<int:pk>/', views.supprimer_unite_medicale, name='supprimer_unite_medicale'),
    path('unites-medicales/toggle/<int:pk>/', views.toggle_unite_medicale, name='toggle_unite_medicale'),

    path('directions/liste/', views.liste_directions, name='liste_directions'),
    path('directions/ajouter/', views.ajouter_direction, name='ajouter_direction'),
    path('directions/modifier/<int:pk>/', views.modifier_direction, name='modifier_direction'),
    path('directions/supprimer/<int:pk>/', views.supprimer_direction, name='supprimer_direction'),
    path('directions/toggle/<int:pk>/', views.toggle_direction, name='toggle_direction'),

    path('departements/liste/', views.liste_departements, name='liste_departements'),
    path('departements/ajouter/', views.ajouter_departement, name='ajouter_departement'),
    path('departements/modifier/<int:pk>/', views.modifier_departement, name='modifier_departement'),
    path('departements/supprimer/<int:pk>/', views.supprimer_departement, name='supprimer_departement'),
    path('departements/toggle/<int:pk>/', views.toggle_departement, name='toggle_departement'),

    path('services/liste/', views.liste_services, name='liste_services'),
    path('services/ajouter/', views.ajouter_service, name='ajouter_service'),
    path('services/modifier/<int:pk>/', views.modifier_service, name='modifier_service'),
    path('services/supprimer/<int:pk>/', views.supprimer_service, name='supprimer_service'),

    path('fonctions/liste/', views.liste_fonctions, name='liste_fonctions'),
    path('fonctions/ajouter/', views.ajouter_fonction, name='ajouter_fonction'),
    path('fonctions/modifier/<int:pk>/', views.modifier_fonction, name='modifier_fonction'),
    path('fonctions/supprimer/<int:pk>/', views.supprimer_fonction, name='supprimer_fonction'),

    path('specialites/liste/', views.liste_specialites, name='liste_specialites'),
    path('specialites/ajouter/', views.ajouter_specialite, name='ajouter_specialite'),
    path('specialites/modifier/<int:pk>/', views.modifier_specialite, name='modifier_specialite'),
    path('specialites/supprimer/<int:pk>/', views.supprimer_specialite, name='supprimer_specialite'),
    path('specialites/toggle/<int:pk>/', views.toggle_specialite, name='toggle_specialite'),

    path('actes/categories/', views.liste_categories_actes, name='liste_categories_actes'),
    path('actes/categories/ajouter/', views.ajouter_categorie_acte, name='ajouter_categorie_acte'),
    path('actes/categories/modifier/<int:pk>/', views.modifier_categorie_acte, name='modifier_categorie_acte'),
    path('actes/categories/supprimer/<int:pk>/', views.supprimer_categorie_acte, name='supprimer_categorie_acte'),
    path('actes/categories/toggle/<int:pk>/', views.toggle_categorie_acte, name='toggle_categorie_acte'),

    path('actes/liste/', views.liste_actes_medicaux, name='liste_actes_medicaux'),
    path('actes/ajouter/', views.ajouter_acte_medical, name='ajouter_acte_medical'),
    path('actes/modifier/<int:pk>/', views.modifier_acte_medical, name='modifier_acte_medical'),
    path('actes/supprimer/<int:pk>/', views.supprimer_acte_medical, name='supprimer_acte_medical'),
    path('actes/toggle/<int:pk>/', views.toggle_acte_medical, name='toggle_acte_medical'),

    path('actes/tarifs/', views.liste_tarifs_actes, name='liste_tarifs_actes'),
    path('actes/tarifs/ajouter/', views.ajouter_tarif_acte, name='ajouter_tarif_acte'),
    path('actes/tarifs/modifier/<int:pk>/', views.modifier_tarif_acte, name='modifier_tarif_acte'),
    path('actes/tarifs/supprimer/<int:pk>/', views.supprimer_tarif_acte, name='supprimer_tarif_acte'),
    path('actes/tarifs/toggle/<int:pk>/', views.toggle_tarif_acte, name='toggle_tarif_acte'),

    path('consultations/types/', views.liste_types_consultation, name='liste_types_consultation'),
    path('consultations/types/ajouter/', views.ajouter_type_consultation, name='ajouter_type_consultation'),
    path('consultations/types/modifier/<int:pk>/', views.modifier_type_consultation, name='modifier_type_consultation'),
    path('consultations/types/supprimer/<int:pk>/', views.supprimer_type_consultation, name='supprimer_type_consultation'),
    path('consultations/types/toggle/<int:pk>/', views.toggle_type_consultation, name='toggle_type_consultation'),

    path('consultations/tarifs/', views.liste_tarifs_consultation, name='liste_tarifs_consultation'),
    path('consultations/tarifs/ajouter/', views.ajouter_tarif_consultation, name='ajouter_tarif_consultation'),
    path('consultations/tarifs/modifier/<int:pk>/', views.modifier_tarif_consultation, name='modifier_tarif_consultation'),
    path('consultations/tarifs/supprimer/<int:pk>/', views.supprimer_tarif_consultation, name='supprimer_tarif_consultation'),
    path('consultations/tarifs/toggle/<int:pk>/', views.toggle_tarif_consultation, name='toggle_tarif_consultation'),

    path('consultations/motifs/', views.liste_motifs_consultation, name='liste_motifs_consultation'),
    path('consultations/motifs/ajouter/', views.ajouter_motif_consultation, name='ajouter_motif_consultation'),
    path('consultations/motifs/modifier/<int:pk>/', views.modifier_motif_consultation, name='modifier_motif_consultation'),
    path('consultations/motifs/supprimer/<int:pk>/', views.supprimer_motif_consultation, name='supprimer_motif_consultation'),
    path('consultations/motifs/toggle/<int:pk>/', views.toggle_motif_consultation, name='toggle_motif_consultation'),

    path('consultations/posologies/', views.liste_posologies, name='liste_posologies'),
    path('consultations/posologies/ajouter/', views.ajouter_posologie, name='ajouter_posologie'),
    path('consultations/posologies/modifier/<int:pk>/', views.modifier_posologie, name='modifier_posologie'),
    path('consultations/posologies/supprimer/<int:pk>/', views.supprimer_posologie, name='supprimer_posologie'),
    path('consultations/posologies/toggle/<int:pk>/', views.toggle_posologie, name='toggle_posologie'),

    path('medicaments/dosages/', views.liste_dosages, name='liste_dosages'),
    path('medicaments/dosages/ajouter/', views.ajouter_dosage, name='ajouter_dosage'),
    path('medicaments/dosages/modifier/<int:pk>/', views.modifier_dosage, name='modifier_dosage'),
    path('medicaments/dosages/supprimer/<int:pk>/', views.supprimer_dosage, name='supprimer_dosage'),
    path('medicaments/dosages/toggle/<int:pk>/', views.toggle_dosage, name='toggle_dosage'),

    path('medicaments/formes/', views.liste_formes, name='liste_formes'),
    path('medicaments/formes/ajouter/', views.ajouter_forme, name='ajouter_forme'),
    path('medicaments/formes/modifier/<int:pk>/', views.modifier_forme, name='modifier_forme'),
    path('medicaments/formes/supprimer/<int:pk>/', views.supprimer_forme, name='supprimer_forme'),
    path('medicaments/formes/toggle/<int:pk>/', views.toggle_forme, name='toggle_forme'),

    path('medicaments/voies-administration/', views.liste_voies_administration, name='liste_voies_administration'),
    path('medicaments/voies-administration/ajouter/', views.ajouter_voie_administration, name='ajouter_voie_administration'),
    path('medicaments/voies-administration/modifier/<int:pk>/', views.modifier_voie_administration, name='modifier_voie_administration'),
    path('medicaments/voies-administration/supprimer/<int:pk>/', views.supprimer_voie_administration, name='supprimer_voie_administration'),
    path('medicaments/voies-administration/toggle/<int:pk>/', views.toggle_voie_administration, name='toggle_voie_administration'),
    
    path('examens/categories/', views.liste_categories_examens, name='liste_categories_examens'),
    path('examens/categories/ajouter/', views.ajouter_categorie_examen, name='ajouter_categorie_examen'),
    path('examens/categories/modifier/<int:pk>/', views.modifier_categorie_examen, name='modifier_categorie_examen'),
    path('examens/categories/supprimer/<int:pk>/', views.supprimer_categorie_examen, name='supprimer_categorie_examen'),
    path('examens/categories/toggle/<int:pk>/', views.toggle_categorie_examen, name='toggle_categorie_examen'),

    path('examens/types/', views.liste_types_examens, name='liste_types_examens'),
    path('examens/types/ajouter/', views.ajouter_type_examen, name='ajouter_type_examen'),
    path('examens/types/modifier/<int:pk>/', views.modifier_type_examen, name='modifier_type_examen'),
    path('examens/types/supprimer/<int:pk>/', views.supprimer_type_examen, name='supprimer_type_examen'),
    path('examens/types/toggle/<int:pk>/', views.toggle_type_examen, name='toggle_type_examen'),

    path('examens/liste/', views.liste_examens, name='liste_examens'),
    path('examens/ajouter/', views.ajouter_examen, name='ajouter_examen'),
    path('examens/modifier/<int:pk>/', views.modifier_examen, name='modifier_examen'),
    path('examens/supprimer/<int:pk>/', views.supprimer_examen, name='supprimer_examen'),
    path('examens/toggle/<int:pk>/', views.toggle_examen, name='toggle_examen'),

    path('examens/tarifs/', views.liste_tarifs_examens, name='liste_tarifs_examens'),
    path('examens/tarifs/ajouter/', views.ajouter_tarif_examen, name='ajouter_tarif_examen'),
    path('examens/tarifs/modifier/<int:pk>/', views.modifier_tarif_examen, name='modifier_tarif_examen'),
    path('examens/tarifs/supprimer/<int:pk>/', views.supprimer_tarif_examen, name='supprimer_tarif_examen'),
    path('examens/tarifs/toggle/<int:pk>/', views.toggle_tarif_examen, name='toggle_tarif_examen'),
    
    path('hospitalisation/types-sejours/', views.liste_types_sejours, name='liste_types_sejours'),
    path('hospitalisation/types-sejours/ajouter/', views.ajouter_type_sejour, name='ajouter_type_sejour'),
    path('hospitalisation/types-sejours/modifier/<int:pk>/', views.modifier_type_sejour, name='modifier_type_sejour'),
    path('hospitalisation/types-sejours/supprimer/<int:pk>/', views.supprimer_type_sejour, name='supprimer_type_sejour'),
    path('hospitalisation/types-sejours/toggle/<int:pk>/', views.toggle_type_sejour, name='toggle_type_sejour'),

    path('hospitalisation/types-chambres/', views.liste_types_chambres, name='liste_types_chambres'),
    path('hospitalisation/types-chambres/ajouter/', views.ajouter_type_chambre, name='ajouter_type_chambre'),
    path('hospitalisation/types-chambres/modifier/<int:pk>/', views.modifier_type_chambre, name='modifier_type_chambre'),
    path('hospitalisation/types-chambres/supprimer/<int:pk>/', views.supprimer_type_chambre, name='supprimer_type_chambre'),
    path('hospitalisation/types-chambres/toggle/<int:pk>/', views.toggle_type_chambre, name='toggle_type_chambre'),

    path('hospitalisation/chambres/', views.liste_chambres, name='liste_chambres'),
    path('hospitalisation/chambres/ajouter/', views.ajouter_chambre, name='ajouter_chambre'),
    path('hospitalisation/chambres/modifier/<int:pk>/', views.modifier_chambre, name='modifier_chambre'),
    path('hospitalisation/chambres/supprimer/<int:pk>/', views.supprimer_chambre, name='supprimer_chambre'),
    path('hospitalisation/chambres/toggle/<int:pk>/', views.toggle_chambre, name='toggle_chambre'),

    path('hospitalisation/lits/', views.liste_lits, name='liste_lits'),
    path('hospitalisation/lits/ajouter/', views.ajouter_lit, name='ajouter_lit'),
    path('hospitalisation/lits/modifier/<int:pk>/', views.modifier_lit, name='modifier_lit'),
    path('hospitalisation/lits/supprimer/<int:pk>/', views.supprimer_lit, name='supprimer_lit'),
    path('hospitalisation/lits/toggle/<int:pk>/', views.toggle_lit, name='toggle_lit'),

    path('hospitalisation/soins/', views.liste_types_soins, name='liste_types_soins'),
    path('hospitalisation/soins/ajouter/', views.ajouter_type_soin, name='ajouter_type_soin'),
    path('hospitalisation/soins/modifier/<int:pk>/', views.modifier_type_soin, name='modifier_type_soin'),
    path('hospitalisation/soins/supprimer/<int:pk>/', views.supprimer_type_soin, name='supprimer_type_soin'),
    path('hospitalisation/soins/toggle/<int:pk>/', views.toggle_type_soin, name='toggle_type_soin'),

    path('hospitalisation/regimes-alimentaires/', views.liste_regimes_alimentaires, name='liste_regimes_alimentaires'),
    path('hospitalisation/regimes-alimentaires/ajouter/', views.ajouter_regime_alimentaire, name='ajouter_regime_alimentaire'),
    path('hospitalisation/regimes-alimentaires/modifier/<int:pk>/', views.modifier_regime_alimentaire, name='modifier_regime_alimentaire'),
    path('hospitalisation/regimes-alimentaires/supprimer/<int:pk>/', views.supprimer_regime_alimentaire, name='supprimer_regime_alimentaire'),
    path('hospitalisation/regimes-alimentaires/toggle/<int:pk>/', views.toggle_regime_alimentaire, name='toggle_regime_alimentaire'),

    path('hospitalisation/motifs/', views.liste_motifs_hospitalisation, name='liste_motifs_hospitalisation'),
    path('hospitalisation/motifs/ajouter/', views.ajouter_motif_hospitalisation, name='ajouter_motif_hospitalisation'),
    path('hospitalisation/motifs/modifier/<int:pk>/', views.modifier_motif_hospitalisation, name='modifier_motif_hospitalisation'),
    path('hospitalisation/motifs/supprimer/<int:pk>/', views.supprimer_motif_hospitalisation, name='supprimer_motif_hospitalisation'),
    path('hospitalisation/motifs/toggle/<int:pk>/', views.toggle_motif_hospitalisation, name='toggle_motif_hospitalisation'),

    path('hospitalisation/types-sortie/', views.liste_types_sortie, name='liste_types_sortie'),
    path('hospitalisation/types-sortie/ajouter/', views.ajouter_type_sortie, name='ajouter_type_sortie'),
    path('hospitalisation/types-sortie/modifier/<int:pk>/', views.modifier_type_sortie, name='modifier_type_sortie'),
    path('hospitalisation/types-sortie/supprimer/<int:pk>/', views.supprimer_type_sortie, name='supprimer_type_sortie'),
    path('hospitalisation/types-sortie/toggle/<int:pk>/', views.toggle_type_sortie, name='toggle_type_sortie'),

    path('hospitalisation/tarifs-sejours/', views.liste_tarifs_sejours, name='liste_tarifs_sejours'),
    path('hospitalisation/tarifs-sejours/ajouter/', views.ajouter_tarif_sejour, name='ajouter_tarif_sejour'),
    path('hospitalisation/tarifs-sejours/modifier/<int:pk>/', views.modifier_tarif_sejour, name='modifier_tarif_sejour'),
    path('hospitalisation/tarifs-sejours/supprimer/<int:pk>/', views.supprimer_tarif_sejour, name='supprimer_tarif_sejour'),
    path('hospitalisation/tarifs-sejours/toggle/<int:pk>/', views.toggle_tarif_sejour, name='toggle_tarif_sejour'),



]