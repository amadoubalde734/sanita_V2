from .consultation_views import (
    index,
    consultation_list,
    consultation_add,
    consultation_detail,
    arret_travail_list,
    orientation_list,
    referement_list,
)
from .hospitalisation_views import hospitalisation_list
from .rendez_vous_views import rendez_vous_list

__all__ = [
    'index',
    'consultation_list',
    'consultation_add',
    'consultation_detail',
    'arret_travail_list',
    'orientation_list',
    'referement_list',
    'hospitalisation_list',
    'rendez_vous_list',
]
