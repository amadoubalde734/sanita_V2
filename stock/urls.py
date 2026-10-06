from django.urls import path

from . import views


app_name = "stock"


urlpatterns = [
    path(
        "",
        views.index,
        name="index",
    ),

    # ========================================================
    # MÉDICAMENTS
    # ========================================================

    path(
        "medicaments/",
        views.medicament_list,
        name="medicament_list",
    ),

    path(
        "medicaments/nouveau/",
        views.medicament_create,
        name="medicament_create",
    ),

    # --------------------------------------------------------
    # APERÇU RÉFÉRENCE MÉDICAMENT
    # --------------------------------------------------------

    path(
        "medicaments/reference-preview/",
        views.medicament_reference_preview,
        name="medicament_reference_preview",
    ),

    path(
        "medicaments/<int:pk>/",
        views.medicament_detail,
        name="medicament_detail",
    ),

    path(
        "medicaments/<int:pk>/modifier/",
        views.medicament_update,
        name="medicament_update",
    ),

    path(
        "medicaments/<int:pk>/toggle/",
        views.medicament_toggle,
        name="medicament_toggle",
    ),

    # ========================================================
    # FAMILLES DE MÉDICAMENTS
    # ========================================================

    path(
        "medicaments/familles/",
        views.famille_list,
        name="famille_list",
    ),

    path(
        "medicaments/familles/nouveau/",
        views.famille_create,
        name="famille_create",
    ),

    path(
        "medicaments/familles/<int:pk>/modifier/",
        views.famille_update,
        name="famille_update",
    ),

    path(
        "medicaments/familles/<int:pk>/toggle/",
        views.famille_toggle,
        name="famille_toggle",
    ),
]