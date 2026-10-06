from django.http import HttpResponse


def index(request):
    return HttpResponse(
        "Module Stock en cours de développement."
    )


from .medicaments import (
    medicament_list,
    medicament_create,
    medicament_detail,
    medicament_update,
    medicament_toggle,
    medicament_reference_preview,
    famille_list,
    famille_create,
    famille_update,
    famille_toggle,
)