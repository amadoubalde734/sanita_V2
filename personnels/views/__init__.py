from .employe_views import (
    employe_list,
    employe_create,
    employe_update,
    employe_delete,
    employe_dashboard,
    employe_profil,
    employe_historique,
    get_services_by_departement,
    get_fonctions_by_service,
)
from .ayant_droit_views import *
from .famille_views import *
from .recherche_views import *

__all__ = [
    'employe_list',
    'employe_create',
    'employe_update',
    'employe_delete',
    'employe_dashboard',
    'employe_profil',
    'employe_historique',
    'get_services_by_departement',
    'get_fonctions_by_service',
    'ayant_droit_list',
    'ayant_droit_create',
    'enfant_create',
    'conjoint_create',
    'autre_ayant_droit_create',
]
