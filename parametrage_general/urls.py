from django.urls import path

from . import views

app_name = 'parametrage_general'

urlpatterns = [
    path('', views.index, name='index'),

    # ============================================================
    # CONFIGURATION DE L'ÉTABLISSEMENT
    # ============================================================
    path('configuration/', views.configuration_etablissement, name='configuration_etablissement'),
    path('configuration/modifier/', views.modifier_configuration_etablissement, name='modifier_configuration_etablissement'),

    # ============================================================
    # STRUCTURE / ORGANISATION
    # ============================================================
    # Sociétés
    path('societes/', views.liste_societes, name='liste_societes'),
    path('societes/ajouter/', views.ajouter_societe, name='ajouter_societe'),
    path('societes/<int:pk>/modifier/', views.modifier_societe, name='modifier_societe'),
    path('societes/<int:pk>/supprimer/', views.supprimer_societe, name='supprimer_societe'),

    # Villes
    path('villes/', views.liste_villes, name='liste_villes'),
    path('villes/ajouter/', views.ajouter_ville, name='ajouter_ville'),
    path('villes/<int:pk>/modifier/', views.modifier_ville, name='modifier_ville'),
    path('villes/<int:pk>/supprimer/', views.supprimer_ville, name='supprimer_ville'),

    # Sites
    path('sites/', views.liste_sites, name='liste_sites'),
    path('sites/ajouter/', views.ajouter_site, name='ajouter_site'),
    path('sites/<int:pk>/modifier/', views.modifier_site, name='modifier_site'),
    path('sites/<int:pk>/supprimer/', views.supprimer_site, name='supprimer_site'),

    # Unités médicales
    path('unites-medicales/', views.liste_unites_medicales, name='liste_unites_medicales'),
    path('unites-medicales/ajouter/', views.ajouter_unite_medicale, name='ajouter_unite_medicale'),
    path('unites-medicales/<int:pk>/modifier/', views.modifier_unite_medicale, name='modifier_unite_medicale'),
    path('unites-medicales/<int:pk>/supprimer/', views.supprimer_unite_medicale, name='supprimer_unite_medicale'),
    path('unites-medicales/<int:pk>/toggle/', views.toggle_unite_medicale, name='toggle_unite_medicale'),

    # Directions
    path('directions/', views.liste_directions, name='liste_directions'),
    path('directions/ajouter/', views.ajouter_direction, name='ajouter_direction'),
    path('directions/<int:pk>/modifier/', views.modifier_direction, name='modifier_direction'),
    path('directions/<int:pk>/supprimer/', views.supprimer_direction, name='supprimer_direction'),
    path('directions/<int:pk>/toggle/', views.toggle_direction, name='toggle_direction'),

    # Départements
    path('departements/', views.liste_departements, name='liste_departements'),
    path('departements/ajouter/', views.ajouter_departement, name='ajouter_departement'),
    path('departements/<int:pk>/modifier/', views.modifier_departement, name='modifier_departement'),
    path('departements/<int:pk>/supprimer/', views.supprimer_departement, name='supprimer_departement'),
    path('departements/<int:pk>/toggle/', views.toggle_departement, name='toggle_departement'),

    # Services
    path('services/', views.liste_services, name='liste_services'),
    path('services/ajouter/', views.ajouter_service, name='ajouter_service'),
    path('services/<int:pk>/modifier/', views.modifier_service, name='modifier_service'),
    path('services/<int:pk>/supprimer/', views.supprimer_service, name='supprimer_service'),

    # Fonctions
    path('fonctions/', views.liste_fonctions, name='liste_fonctions'),
    path('fonctions/ajouter/', views.ajouter_fonction, name='ajouter_fonction'),
    path('fonctions/<int:pk>/modifier/', views.modifier_fonction, name='modifier_fonction'),
    path('fonctions/<int:pk>/supprimer/', views.supprimer_fonction, name='supprimer_fonction'),

    # Spécialités
    path('specialites/', views.liste_specialites, name='liste_specialites'),
    path('specialites/ajouter/', views.ajouter_specialite, name='ajouter_specialite'),
    path('specialites/<int:pk>/modifier/', views.modifier_specialite, name='modifier_specialite'),
    path('specialites/<int:pk>/supprimer/', views.supprimer_specialite, name='supprimer_specialite'),
    path('specialites/<int:pk>/toggle/', views.toggle_specialite, name='toggle_specialite'),

    # ============================================================
    # ACTES MÉDICAUX
    # ============================================================
    # Catégories d'actes
    path('actes/categories/', views.liste_categories_actes, name='liste_categories_actes'),
    path('actes/categories/ajouter/', views.ajouter_categorie_acte, name='ajouter_categorie_acte'),
    path('actes/categories/<int:pk>/modifier/', views.modifier_categorie_acte, name='modifier_categorie_acte'),
    path('actes/categories/<int:pk>/supprimer/', views.supprimer_categorie_acte, name='supprimer_categorie_acte'),
    path('actes/categories/<int:pk>/toggle/', views.toggle_categorie_acte, name='toggle_categorie_acte'),

    # Tarifs des actes (déclaré avant 'actes/<int:pk>/...' par lisibilité)
    path('actes/tarifs/', views.liste_tarifs_actes, name='liste_tarifs_actes'),
    path('actes/tarifs/ajouter/', views.ajouter_tarif_acte, name='ajouter_tarif_acte'),
    path('actes/tarifs/<int:pk>/modifier/', views.modifier_tarif_acte, name='modifier_tarif_acte'),
    path('actes/tarifs/<int:pk>/supprimer/', views.supprimer_tarif_acte, name='supprimer_tarif_acte'),
    path('actes/tarifs/<int:pk>/toggle/', views.toggle_tarif_acte, name='toggle_tarif_acte'),

    # Actes médicaux
    path('actes/', views.liste_actes_medicaux, name='liste_actes_medicaux'),
    path('actes/ajouter/', views.ajouter_acte_medical, name='ajouter_acte_medical'),
    path('actes/<int:pk>/modifier/', views.modifier_acte_medical, name='modifier_acte_medical'),
    path('actes/<int:pk>/supprimer/', views.supprimer_acte_medical, name='supprimer_acte_medical'),
    path('actes/<int:pk>/toggle/', views.toggle_acte_medical, name='toggle_acte_medical'),

    # ============================================================
    # CONSULTATIONS
    # ============================================================
    # Types de consultation
    path('consultations/types/', views.liste_types_consultation, name='liste_types_consultation'),
    path('consultations/types/ajouter/', views.ajouter_type_consultation, name='ajouter_type_consultation'),
    path('consultations/types/<int:pk>/modifier/', views.modifier_type_consultation, name='modifier_type_consultation'),
    path('consultations/types/<int:pk>/supprimer/', views.supprimer_type_consultation, name='supprimer_type_consultation'),
    path('consultations/types/<int:pk>/toggle/', views.toggle_type_consultation, name='toggle_type_consultation'),

    # Tarifs de consultation
    path('consultations/tarifs/', views.liste_tarifs_consultation, name='liste_tarifs_consultation'),
    path('consultations/tarifs/ajouter/', views.ajouter_tarif_consultation, name='ajouter_tarif_consultation'),
    path('consultations/tarifs/<int:pk>/modifier/', views.modifier_tarif_consultation, name='modifier_tarif_consultation'),
    path('consultations/tarifs/<int:pk>/supprimer/', views.supprimer_tarif_consultation, name='supprimer_tarif_consultation'),
    path('consultations/tarifs/<int:pk>/toggle/', views.toggle_tarif_consultation, name='toggle_tarif_consultation'),

    # Motifs de consultation
    path('consultations/motifs/', views.liste_motifs_consultation, name='liste_motifs_consultation'),
    path('consultations/motifs/ajouter/', views.ajouter_motif_consultation, name='ajouter_motif_consultation'),
    path('consultations/motifs/<int:pk>/modifier/', views.modifier_motif_consultation, name='modifier_motif_consultation'),
    path('consultations/motifs/<int:pk>/supprimer/', views.supprimer_motif_consultation, name='supprimer_motif_consultation'),
    path('consultations/motifs/<int:pk>/toggle/', views.toggle_motif_consultation, name='toggle_motif_consultation'),

    # Posologies
    path('consultations/posologies/', views.liste_posologies, name='liste_posologies'),
    path('consultations/posologies/ajouter/', views.ajouter_posologie, name='ajouter_posologie'),
    path('consultations/posologies/<int:pk>/modifier/', views.modifier_posologie, name='modifier_posologie'),
    path('consultations/posologies/<int:pk>/supprimer/', views.supprimer_posologie, name='supprimer_posologie'),
    path('consultations/posologies/<int:pk>/toggle/', views.toggle_posologie, name='toggle_posologie'),

    # ============================================================
    # MÉDICAMENTS
    # ============================================================
    # Dosages
    path('medicaments/dosages/', views.liste_dosages, name='liste_dosages'),
    path('medicaments/dosages/ajouter/', views.ajouter_dosage, name='ajouter_dosage'),
    path('medicaments/dosages/<int:pk>/modifier/', views.modifier_dosage, name='modifier_dosage'),
    path('medicaments/dosages/<int:pk>/supprimer/', views.supprimer_dosage, name='supprimer_dosage'),
    path('medicaments/dosages/<int:pk>/toggle/', views.toggle_dosage, name='toggle_dosage'),

    # Formes galéniques
    path('medicaments/formes/', views.liste_formes, name='liste_formes'),
    path('medicaments/formes/ajouter/', views.ajouter_forme, name='ajouter_forme'),
    path('medicaments/formes/<int:pk>/modifier/', views.modifier_forme, name='modifier_forme'),
    path('medicaments/formes/<int:pk>/supprimer/', views.supprimer_forme, name='supprimer_forme'),
    path('medicaments/formes/<int:pk>/toggle/', views.toggle_forme, name='toggle_forme'),

    # Voies d'administration
    path('medicaments/voies-administration/', views.liste_voies_administration, name='liste_voies_administration'),
    path('medicaments/voies-administration/ajouter/', views.ajouter_voie_administration, name='ajouter_voie_administration'),
    path('medicaments/voies-administration/<int:pk>/modifier/', views.modifier_voie_administration, name='modifier_voie_administration'),
    path('medicaments/voies-administration/<int:pk>/supprimer/', views.supprimer_voie_administration, name='supprimer_voie_administration'),
    path('medicaments/voies-administration/<int:pk>/toggle/', views.toggle_voie_administration, name='toggle_voie_administration'),

    # ============================================================
    # EXAMENS
    # ============================================================
    # Catégories d'examens
    path('examens/categories/', views.liste_categories_examens, name='liste_categories_examens'),
    path('examens/categories/ajouter/', views.ajouter_categorie_examen, name='ajouter_categorie_examen'),
    path('examens/categories/<int:pk>/modifier/', views.modifier_categorie_examen, name='modifier_categorie_examen'),
    path('examens/categories/<int:pk>/supprimer/', views.supprimer_categorie_examen, name='supprimer_categorie_examen'),
    path('examens/categories/<int:pk>/toggle/', views.toggle_categorie_examen, name='toggle_categorie_examen'),

    # Types d'examens
    path('examens/types/', views.liste_types_examens, name='liste_types_examens'),
    path('examens/types/ajouter/', views.ajouter_type_examen, name='ajouter_type_examen'),
    path('examens/types/<int:pk>/modifier/', views.modifier_type_examen, name='modifier_type_examen'),
    path('examens/types/<int:pk>/supprimer/', views.supprimer_type_examen, name='supprimer_type_examen'),
    path('examens/types/<int:pk>/toggle/', views.toggle_type_examen, name='toggle_type_examen'),

    # Tarifs des examens
    path('examens/tarifs/', views.liste_tarifs_examens, name='liste_tarifs_examens'),
    path('examens/tarifs/ajouter/', views.ajouter_tarif_examen, name='ajouter_tarif_examen'),
    path('examens/tarifs/<int:pk>/modifier/', views.modifier_tarif_examen, name='modifier_tarif_examen'),
    path('examens/tarifs/<int:pk>/supprimer/', views.supprimer_tarif_examen, name='supprimer_tarif_examen'),
    path('examens/tarifs/<int:pk>/toggle/', views.toggle_tarif_examen, name='toggle_tarif_examen'),

    # Examens
    path('examens/', views.liste_examens, name='liste_examens'),
    path('examens/ajouter/', views.ajouter_examen, name='ajouter_examen'),
    path('examens/<int:pk>/modifier/', views.modifier_examen, name='modifier_examen'),
    path('examens/<int:pk>/supprimer/', views.supprimer_examen, name='supprimer_examen'),
    path('examens/<int:pk>/toggle/', views.toggle_examen, name='toggle_examen'),

    # ============================================================
    # HOSPITALISATION
    # ============================================================
    # Types de séjours
    path('hospitalisation/types-sejours/', views.liste_types_sejours, name='liste_types_sejours'),
    path('hospitalisation/types-sejours/ajouter/', views.ajouter_type_sejour, name='ajouter_type_sejour'),
    path('hospitalisation/types-sejours/<int:pk>/modifier/', views.modifier_type_sejour, name='modifier_type_sejour'),
    path('hospitalisation/types-sejours/<int:pk>/supprimer/', views.supprimer_type_sejour, name='supprimer_type_sejour'),
    path('hospitalisation/types-sejours/<int:pk>/toggle/', views.toggle_type_sejour, name='toggle_type_sejour'),

    # Types de chambres
    path('hospitalisation/types-chambres/', views.liste_types_chambres, name='liste_types_chambres'),
    path('hospitalisation/types-chambres/ajouter/', views.ajouter_type_chambre, name='ajouter_type_chambre'),
    path('hospitalisation/types-chambres/<int:pk>/modifier/', views.modifier_type_chambre, name='modifier_type_chambre'),
    path('hospitalisation/types-chambres/<int:pk>/supprimer/', views.supprimer_type_chambre, name='supprimer_type_chambre'),
    path('hospitalisation/types-chambres/<int:pk>/toggle/', views.toggle_type_chambre, name='toggle_type_chambre'),

    # Chambres
    path('hospitalisation/chambres/', views.liste_chambres, name='liste_chambres'),
    path('hospitalisation/chambres/ajouter/', views.ajouter_chambre, name='ajouter_chambre'),
    path('hospitalisation/chambres/<int:pk>/modifier/', views.modifier_chambre, name='modifier_chambre'),
    path('hospitalisation/chambres/<int:pk>/supprimer/', views.supprimer_chambre, name='supprimer_chambre'),
    path('hospitalisation/chambres/<int:pk>/toggle/', views.toggle_chambre, name='toggle_chambre'),

    # Lits
    path('hospitalisation/lits/', views.liste_lits, name='liste_lits'),
    path('hospitalisation/lits/ajouter/', views.ajouter_lit, name='ajouter_lit'),
    path('hospitalisation/lits/<int:pk>/modifier/', views.modifier_lit, name='modifier_lit'),
    path('hospitalisation/lits/<int:pk>/supprimer/', views.supprimer_lit, name='supprimer_lit'),
    path('hospitalisation/lits/<int:pk>/toggle/', views.toggle_lit, name='toggle_lit'),

    # Types de soins
    path('hospitalisation/types-soins/', views.liste_types_soins, name='liste_types_soins'),
    path('hospitalisation/types-soins/ajouter/', views.ajouter_type_soin, name='ajouter_type_soin'),
    path('hospitalisation/types-soins/<int:pk>/modifier/', views.modifier_type_soin, name='modifier_type_soin'),
    path('hospitalisation/types-soins/<int:pk>/supprimer/', views.supprimer_type_soin, name='supprimer_type_soin'),
    path('hospitalisation/types-soins/<int:pk>/toggle/', views.toggle_type_soin, name='toggle_type_soin'),

    # Régimes alimentaires
    path('hospitalisation/regimes-alimentaires/', views.liste_regimes_alimentaires, name='liste_regimes_alimentaires'),
    path('hospitalisation/regimes-alimentaires/ajouter/', views.ajouter_regime_alimentaire, name='ajouter_regime_alimentaire'),
    path('hospitalisation/regimes-alimentaires/<int:pk>/modifier/', views.modifier_regime_alimentaire, name='modifier_regime_alimentaire'),
    path('hospitalisation/regimes-alimentaires/<int:pk>/supprimer/', views.supprimer_regime_alimentaire, name='supprimer_regime_alimentaire'),
    path('hospitalisation/regimes-alimentaires/<int:pk>/toggle/', views.toggle_regime_alimentaire, name='toggle_regime_alimentaire'),

    # Motifs d'hospitalisation
    path('hospitalisation/motifs/', views.liste_motifs_hospitalisation, name='liste_motifs_hospitalisation'),
    path('hospitalisation/motifs/ajouter/', views.ajouter_motif_hospitalisation, name='ajouter_motif_hospitalisation'),
    path('hospitalisation/motifs/<int:pk>/modifier/', views.modifier_motif_hospitalisation, name='modifier_motif_hospitalisation'),
    path('hospitalisation/motifs/<int:pk>/supprimer/', views.supprimer_motif_hospitalisation, name='supprimer_motif_hospitalisation'),
    path('hospitalisation/motifs/<int:pk>/toggle/', views.toggle_motif_hospitalisation, name='toggle_motif_hospitalisation'),

    # Types de sortie
    path('hospitalisation/types-sortie/', views.liste_types_sortie, name='liste_types_sortie'),
    path('hospitalisation/types-sortie/ajouter/', views.ajouter_type_sortie, name='ajouter_type_sortie'),
    path('hospitalisation/types-sortie/<int:pk>/modifier/', views.modifier_type_sortie, name='modifier_type_sortie'),
    path('hospitalisation/types-sortie/<int:pk>/supprimer/', views.supprimer_type_sortie, name='supprimer_type_sortie'),
    path('hospitalisation/types-sortie/<int:pk>/toggle/', views.toggle_type_sortie, name='toggle_type_sortie'),

    # Tarifs des séjours
    path('hospitalisation/tarifs-sejours/', views.liste_tarifs_sejours, name='liste_tarifs_sejours'),
    path('hospitalisation/tarifs-sejours/ajouter/', views.ajouter_tarif_sejour, name='ajouter_tarif_sejour'),
    path('hospitalisation/tarifs-sejours/<int:pk>/modifier/', views.modifier_tarif_sejour, name='modifier_tarif_sejour'),
    path('hospitalisation/tarifs-sejours/<int:pk>/supprimer/', views.supprimer_tarif_sejour, name='supprimer_tarif_sejour'),
    path('hospitalisation/tarifs-sejours/<int:pk>/toggle/', views.toggle_tarif_sejour, name='toggle_tarif_sejour'),

    # ============================================================
    # ÉTABLISSEMENTS PARTENAIRES
    # ============================================================
    path('etablissements-partenaires/', views.liste_etablissements_partenaires, name='liste_etablissements_partenaires'),
    path('etablissements-partenaires/ajouter/', views.ajouter_etablissement_partenaire, name='ajouter_etablissement_partenaire'),
    path('etablissements-partenaires/<int:pk>/modifier/', views.modifier_etablissement_partenaire, name='modifier_etablissement_partenaire'),
    path('etablissements-partenaires/<int:pk>/supprimer/', views.supprimer_etablissement_partenaire, name='supprimer_etablissement_partenaire'),
    path('etablissements-partenaires/<int:pk>/toggle/', views.toggle_etablissement_partenaire, name='toggle_etablissement_partenaire'),

    # ============================================================
    # PHARMACIES
    # ============================================================
    path('pharmacies/', views.liste_pharmacies, name='liste_pharmacies'),
    path('pharmacies/ajouter/', views.ajouter_pharmacie, name='ajouter_pharmacie'),
    path('pharmacies/<int:pk>/modifier/', views.modifier_pharmacie, name='modifier_pharmacie'),
    path('pharmacies/<int:pk>/supprimer/', views.supprimer_pharmacie, name='supprimer_pharmacie'),
    path('pharmacies/<int:pk>/toggle/', views.toggle_pharmacie, name='toggle_pharmacie'),

    # ============================================================
    # PHARMACIES INTERNES
    # ============================================================
    path(
        'pharmacies-internes/',
        views.liste_pharmacies_internes,
        name='liste_pharmacies_internes'
    ),
    path(
        'pharmacies-internes/ajouter/',
        views.ajouter_pharmacie_interne,
        name='ajouter_pharmacie_interne'
    ),
    path(
        'pharmacies-internes/<int:pk>/',
        views.details_pharmacie_interne,
        name='details_pharmacie_interne'
    ),
    path(
        'pharmacies-internes/<int:pk>/modifier/',
        views.modifier_pharmacie_interne,
        name='modifier_pharmacie_interne'
    ),
    path(
        'pharmacies-internes/<int:pk>/supprimer/',
        views.supprimer_pharmacie_interne,
        name='supprimer_pharmacie_interne'
    ),
    path(
        'pharmacies-internes/<int:pk>/toggle/',
        views.toggle_pharmacie_interne,
        name='toggle_pharmacie_interne'
    ),
    
    # ============================================================
    # PHARMACIES PARTENAIRES
    # ============================================================
     
        # ============================================================
    # PHARMACIES PARTENAIRES
    # ============================================================

    path(
        'pharmacies-partenaires/',
        views.liste_pharmacies_partenaires,
        name='liste_pharmacies_partenaires'
    ),
    path(
        'pharmacies-partenaires/ajouter/',
        views.ajouter_pharmacie_partenaire,
        name='ajouter_pharmacie_partenaire'
    ),
    path(
        'pharmacies-partenaires/<int:pk>/',
        views.details_pharmacie_partenaire,
        name='details_pharmacie_partenaire'
    ),
    path(
        'pharmacies-partenaires/<int:pk>/modifier/',
        views.modifier_pharmacie_partenaire,
        name='modifier_pharmacie_partenaire'
    ),
    path(
        'pharmacies-partenaires/<int:pk>/supprimer/',
        views.supprimer_pharmacie_partenaire,
        name='supprimer_pharmacie_partenaire'
    ),
    path(
        'pharmacies-partenaires/<int:pk>/toggle/',
        views.toggle_pharmacie_partenaire,
        name='toggle_pharmacie_partenaire'
    ),

    # ============================================================
    # CATALOGUE DES MÉDICAMENTS — PHARMACIES PARTENAIRES
    # ============================================================

    # ============================================================
    # CATALOGUE DES MÉDICAMENTS — PHARMACIES PARTENAIRES
    # ============================================================

    path(
        'pharmacies-partenaires/catalogue/',
        views.liste_catalogue_medicaments_pharmacies_partenaires,
        name='liste_catalogue_medicaments_pharmacies_partenaires'
    ),

    path(
        'pharmacies-partenaires/catalogue/<int:pk>/',
        views.details_catalogue_medicament_pharmacie_partenaire,
        name='details_catalogue_medicament_pharmacie_partenaire'
    ),

    path(
        'pharmacies-partenaires/catalogue/<int:pk>/supprimer/',
        views.supprimer_catalogue_medicament_pharmacie_partenaire,
        name='supprimer_catalogue_medicament_pharmacie_partenaire'
    ),

    path(
        'pharmacies-partenaires/catalogue/<int:pk>/toggle/',
        views.toggle_catalogue_medicament_pharmacie_partenaire,
        name='toggle_catalogue_medicament_pharmacie_partenaire'
    ),


    # ============================================================
    # TARIFS DES MÉDICAMENTS — PHARMACIES PARTENAIRES
    # ============================================================

    path(
        'pharmacies-partenaires/tarifs/',
        views.liste_tarifs_medicaments_pharmacies_partenaires,
        name='liste_tarifs_medicaments_pharmacies_partenaires'
    ),

    path(
        'pharmacies-partenaires/tarifs/<int:pk>/',
        views.details_tarif_medicament_pharmacie_partenaire,
        name='details_tarif_medicament_pharmacie_partenaire'
    ),

    path(
        'pharmacies-partenaires/tarifs/<int:pk>/supprimer/',
        views.supprimer_tarif_medicament_pharmacie_partenaire,
        name='supprimer_tarif_medicament_pharmacie_partenaire'
    ),

    path(
        'pharmacies-partenaires/tarifs/<int:pk>/toggle/',
        views.toggle_tarif_medicament_pharmacie_partenaire,
        name='toggle_tarif_medicament_pharmacie_partenaire'
    ),

]
