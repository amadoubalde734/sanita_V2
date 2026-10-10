from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from stock.models.medicaments import Medicament, FamilleMedicament
from stock.models.depots import DepotStock


@login_required
def index(request):
    context = {
        "nombre_medicaments": Medicament.objects.filter(
            actif=True,
            statut="actif",
        ).count(),

        "nombre_familles": FamilleMedicament.objects.filter(
            actif=True,
            statut="actif",
        ).count(),

        "nombre_depots": DepotStock.objects.filter(
            actif=True,
            statut="actif",
        ).count(),
    }

    return render(
        request,
        "backend/stock/index.html",
        context,
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

from .depots import (
    depot_list,
    depot_create,
    depot_detail,
    depot_update,
    depot_toggle,
)