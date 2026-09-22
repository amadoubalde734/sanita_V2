from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render

from ..forms.examens import (
    CategorieExamenForm,
    TypeExamenForm,
    ExamenForm,
    TarifExamenForm,
)

from ..models import (
    CategorieExamen,
    TypeExamen,
    Examen,
    TarifExamen,
)


@login_required
def liste_categories_examens(request):
    q = request.GET.get('q', '').strip()

    categories = CategorieExamen.objects.all()

    if q:
        categories = categories.filter(
            models.Q(code__icontains=q) |
            models.Q(nom__icontains=q) |
            models.Q(description__icontains=q)
        )

    context = {
        'categories': categories.order_by('ordre', 'nom'),
        'total_categories': CategorieExamen.objects.count(),
        'categories_actives': CategorieExamen.objects.filter(actif=True).count(),
        'categories_inactives': CategorieExamen.objects.filter(actif=False).count(),
        'categorie_to_edit': None,
        'form': CategorieExamenForm(),
        'modifier': False,
        'q': q,
    }

    return render(
        request,
        'backend/parametrage_general/pages/examens/categories.html',
        context
    )


@login_required
def ajouter_categorie_examen(request):
    if request.method == 'POST':
        form = CategorieExamenForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "La catégorie d'examen a été ajoutée avec succès."
            )
            return redirect('parametrage_general:liste_categories_examens')
    else:
        form = CategorieExamenForm()

    context = {
        'categories': CategorieExamen.objects.order_by('ordre', 'nom'),
        'total_categories': CategorieExamen.objects.count(),
        'categories_actives': CategorieExamen.objects.filter(actif=True).count(),
        'categories_inactives': CategorieExamen.objects.filter(actif=False).count(),
        'categorie_to_edit': None,
        'form': form,
        'modifier': False,
        'q': '',
    }

    return render(
        request,
        'backend/parametrage_general/pages/examens/categories.html',
        context
    )


@login_required
def modifier_categorie_examen(request, pk):
    categorie = get_object_or_404(CategorieExamen, pk=pk)

    if request.method == 'POST':
        form = CategorieExamenForm(request.POST, instance=categorie)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "La catégorie d'examen a été modifiée avec succès."
            )
            return redirect('parametrage_general:liste_categories_examens')
    else:
        form = CategorieExamenForm(instance=categorie)

    context = {
        'categories': CategorieExamen.objects.order_by('ordre', 'nom'),
        'total_categories': CategorieExamen.objects.count(),
        'categories_actives': CategorieExamen.objects.filter(actif=True).count(),
        'categories_inactives': CategorieExamen.objects.filter(actif=False).count(),
        'categorie_to_edit': categorie,
        'form': form,
        'modifier': True,
        'q': '',
    }

    return render(
        request,
        'backend/parametrage_general/pages/examens/categories.html',
        context
    )


@login_required
def supprimer_categorie_examen(request, pk):
    categorie = get_object_or_404(CategorieExamen, pk=pk)

    if request.method == 'POST':
        try:
            categorie.delete()
            messages.success(
                request,
                "La catégorie d'examen a été supprimée avec succès."
            )
        except models.ProtectedError:
            messages.error(
                request,
                "Cette catégorie ne peut pas être supprimée car elle est utilisée."
            )

    return redirect('parametrage_general:liste_categories_examens')


@login_required
def toggle_categorie_examen(request, pk):
    categorie = get_object_or_404(CategorieExamen, pk=pk)

    categorie.actif = not categorie.actif
    categorie.save(update_fields=['actif', 'updated_at'])

    messages.success(
        request,
        f"La catégorie d'examen est maintenant {'active' if categorie.actif else 'inactive'}."
    )

    return redirect('parametrage_general:liste_categories_examens')


@login_required
def liste_types_examens(request):
    q = request.GET.get('q', '').strip()

    types = TypeExamen.objects.select_related('categorie').all()

    if q:
        types = types.filter(
            models.Q(code__icontains=q) |
            models.Q(nom__icontains=q) |
            models.Q(description__icontains=q) |
            models.Q(categorie__nom__icontains=q)
        )

    context = {
        'types': types.order_by(
            'categorie__ordre',
            'categorie__nom',
            'ordre',
            'nom'
        ),
        'total_types': TypeExamen.objects.count(),
        'types_actifs': TypeExamen.objects.filter(actif=True).count(),
        'types_inactifs': TypeExamen.objects.filter(actif=False).count(),
        'type_to_edit': None,
        'form': TypeExamenForm(),
        'modifier': False,
        'q': q,
    }

    return render(
        request,
        'backend/parametrage_general/pages/examens/types.html',
        context
    )


@login_required
def ajouter_type_examen(request):
    if request.method == 'POST':
        form = TypeExamenForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Le type d'examen a été ajouté avec succès."
            )
            return redirect('parametrage_general:liste_types_examens')
    else:
        form = TypeExamenForm()

    context = {
        'types': TypeExamen.objects.select_related('categorie').order_by(
            'categorie__ordre',
            'categorie__nom',
            'ordre',
            'nom'
        ),
        'total_types': TypeExamen.objects.count(),
        'types_actifs': TypeExamen.objects.filter(actif=True).count(),
        'types_inactifs': TypeExamen.objects.filter(actif=False).count(),
        'type_to_edit': None,
        'form': form,
        'modifier': False,
        'q': '',
    }

    return render(
        request,
        'backend/parametrage_general/pages/examens/types.html',
        context
    )


@login_required
def modifier_type_examen(request, pk):
    type_examen = get_object_or_404(TypeExamen, pk=pk)

    if request.method == 'POST':
        form = TypeExamenForm(request.POST, instance=type_examen)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Le type d'examen a été modifié avec succès."
            )
            return redirect('parametrage_general:liste_types_examens')
    else:
        form = TypeExamenForm(instance=type_examen)

    context = {
        'types': TypeExamen.objects.select_related('categorie').order_by(
            'categorie__ordre',
            'categorie__nom',
            'ordre',
            'nom'
        ),
        'total_types': TypeExamen.objects.count(),
        'types_actifs': TypeExamen.objects.filter(actif=True).count(),
        'types_inactifs': TypeExamen.objects.filter(actif=False).count(),
        'type_to_edit': type_examen,
        'form': form,
        'modifier': True,
        'q': '',
    }

    return render(
        request,
        'backend/parametrage_general/pages/examens/types.html',
        context
    )


@login_required
def supprimer_type_examen(request, pk):
    type_examen = get_object_or_404(TypeExamen, pk=pk)

    if request.method == 'POST':
        try:
            type_examen.delete()
            messages.success(
                request,
                "Le type d'examen a été supprimé avec succès."
            )
        except models.ProtectedError:
            messages.error(
                request,
                "Ce type d'examen ne peut pas être supprimé car il est utilisé."
            )

    return redirect('parametrage_general:liste_types_examens')


@login_required
def toggle_type_examen(request, pk):
    type_examen = get_object_or_404(TypeExamen, pk=pk)

    type_examen.actif = not type_examen.actif
    type_examen.save(update_fields=['actif', 'updated_at'])

    messages.success(
        request,
        f"Le type d'examen est maintenant {'actif' if type_examen.actif else 'inactif'}."
    )

    return redirect('parametrage_general:liste_types_examens')


@login_required
def liste_examens(request):
    q = request.GET.get('q', '').strip()

    examens = Examen.objects.select_related(
        'type_examen',
        'type_examen__categorie'
    ).all()

    if q:
        examens = examens.filter(
            models.Q(code__icontains=q) |
            models.Q(libelle__icontains=q) |
            models.Q(description__icontains=q) |
            models.Q(type_examen__nom__icontains=q) |
            models.Q(type_examen__categorie__nom__icontains=q)
        )

    context = {
        'examens': examens.order_by(
            'type_examen__categorie__ordre',
            'type_examen__categorie__nom',
            'type_examen__ordre',
            'type_examen__nom',
            'ordre',
            'libelle'
        ),
        'total_examens': Examen.objects.count(),
        'examens_actifs': Examen.objects.filter(actif=True).count(),
        'examens_inactifs': Examen.objects.filter(actif=False).count(),
        'examen_to_edit': None,
        'form': ExamenForm(),
        'modifier': False,
        'q': q,
    }

    return render(
        request,
        'backend/parametrage_general/pages/examens/examens.html',
        context
    )


@login_required
def ajouter_examen(request):
    if request.method == 'POST':
        form = ExamenForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "L'examen a été ajouté avec succès."
            )
            return redirect('parametrage_general:liste_examens')
    else:
        form = ExamenForm()

    context = {
        'examens': Examen.objects.select_related(
            'type_examen',
            'type_examen__categorie'
        ).order_by(
            'type_examen__categorie__ordre',
            'type_examen__categorie__nom',
            'type_examen__ordre',
            'type_examen__nom',
            'ordre',
            'libelle'
        ),
        'total_examens': Examen.objects.count(),
        'examens_actifs': Examen.objects.filter(actif=True).count(),
        'examens_inactifs': Examen.objects.filter(actif=False).count(),
        'examen_to_edit': None,
        'form': form,
        'modifier': False,
        'q': '',
    }

    return render(
        request,
        'backend/parametrage_general/pages/examens/examens.html',
        context
    )


@login_required
def modifier_examen(request, pk):
    examen = get_object_or_404(Examen, pk=pk)

    if request.method == 'POST':
        form = ExamenForm(request.POST, instance=examen)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "L'examen a été modifié avec succès."
            )
            return redirect('parametrage_general:liste_examens')
    else:
        form = ExamenForm(instance=examen)

    context = {
        'examens': Examen.objects.select_related(
            'type_examen',
            'type_examen__categorie'
        ).order_by(
            'type_examen__categorie__ordre',
            'type_examen__categorie__nom',
            'type_examen__ordre',
            'type_examen__nom',
            'ordre',
            'libelle'
        ),
        'total_examens': Examen.objects.count(),
        'examens_actifs': Examen.objects.filter(actif=True).count(),
        'examens_inactifs': Examen.objects.filter(actif=False).count(),
        'examen_to_edit': examen,
        'form': form,
        'modifier': True,
        'q': '',
    }

    return render(
        request,
        'backend/parametrage_general/pages/examens/examens.html',
        context
    )


@login_required
def supprimer_examen(request, pk):
    examen = get_object_or_404(Examen, pk=pk)

    if request.method == 'POST':
        try:
            examen.delete()
            messages.success(
                request,
                "L'examen a été supprimé avec succès."
            )
        except models.ProtectedError:
            messages.error(
                request,
                "Cet examen ne peut pas être supprimé car il est utilisé."
            )

    return redirect('parametrage_general:liste_examens')


@login_required
def toggle_examen(request, pk):
    examen = get_object_or_404(Examen, pk=pk)

    examen.actif = not examen.actif
    examen.save(update_fields=['actif', 'updated_at'])

    messages.success(
        request,
        f"L'examen est maintenant {'actif' if examen.actif else 'inactif'}."
    )

    return redirect('parametrage_general:liste_examens')


@login_required
def liste_tarifs_examens(request):
    q = request.GET.get('q', '').strip()

    tarifs = TarifExamen.objects.select_related(
        'examen',
        'examen__type_examen',
        'examen__type_examen__categorie',
        'etablissement'
    ).all()

    if q:
        tarifs = tarifs.filter(
            models.Q(examen__code__icontains=q) |
            models.Q(examen__libelle__icontains=q)
        )

    context = {
        'tarifs': tarifs.order_by(
            '-date_debut',
            'examen__libelle'
        ),
        'total_tarifs': TarifExamen.objects.count(),
        'tarifs_actifs': TarifExamen.objects.filter(actif=True).count(),
        'tarifs_inactifs': TarifExamen.objects.filter(actif=False).count(),
        'tarif_to_edit': None,
        'form': TarifExamenForm(),
        'modifier': False,
        'q': q,
    }

    return render(
        request,
        'backend/parametrage_general/pages/examens/tarifs.html',
        context
    )


@login_required
def ajouter_tarif_examen(request):
    if request.method == 'POST':
        form = TarifExamenForm(request.POST)

        if form.is_valid():
            tarif = form.save(commit=False)

            try:
                tarif.full_clean()
                tarif.save()

                messages.success(
                    request,
                    "Le tarif de l'examen a été ajouté avec succès."
                )

                return redirect(
                    'parametrage_general:liste_tarifs_examens'
                )

            except ValidationError as e:
                form.add_error(None, e)

    else:
        form = TarifExamenForm()

    context = {
        'tarifs': TarifExamen.objects.select_related(
            'examen',
            'examen__type_examen',
            'examen__type_examen__categorie',
            'etablissement'
        ).order_by(
            '-date_debut',
            'examen__libelle'
        ),
        'total_tarifs': TarifExamen.objects.count(),
        'tarifs_actifs': TarifExamen.objects.filter(actif=True).count(),
        'tarifs_inactifs': TarifExamen.objects.filter(actif=False).count(),
        'tarif_to_edit': None,
        'form': form,
        'modifier': False,
        'q': '',
    }

    return render(
        request,
        'backend/parametrage_general/pages/examens/tarifs.html',
        context
    )


@login_required
def modifier_tarif_examen(request, pk):
    tarif = get_object_or_404(TarifExamen, pk=pk)

    if request.method == 'POST':
        form = TarifExamenForm(request.POST, instance=tarif)

        if form.is_valid():
            tarif = form.save(commit=False)

            try:
                tarif.full_clean()
                tarif.save()

                messages.success(
                    request,
                    "Le tarif de l'examen a été modifié avec succès."
                )

                return redirect(
                    'parametrage_general:liste_tarifs_examens'
                )

            except ValidationError as e:
                form.add_error(None, e)

    else:
        form = TarifExamenForm(instance=tarif)

    context = {
        'tarifs': TarifExamen.objects.select_related(
            'examen',
            'examen__type_examen',
            'examen__type_examen__categorie',
            'etablissement'
        ).order_by(
            '-date_debut',
            'examen__libelle'
        ),
        'total_tarifs': TarifExamen.objects.count(),
        'tarifs_actifs': TarifExamen.objects.filter(actif=True).count(),
        'tarifs_inactifs': TarifExamen.objects.filter(actif=False).count(),
        'tarif_to_edit': tarif,
        'form': form,
        'modifier': True,
        'q': '',
    }

    return render(
        request,
        'backend/parametrage_general/pages/examens/tarifs.html',
        context
    )


@login_required
def supprimer_tarif_examen(request, pk):
    tarif = get_object_or_404(TarifExamen, pk=pk)

    if request.method == 'POST':
        tarif.delete()

        messages.success(
            request,
            "Le tarif de l'examen a été supprimé avec succès."
        )

    return redirect('parametrage_general:liste_tarifs_examens')


@login_required
def toggle_tarif_examen(request, pk):
    tarif = get_object_or_404(TarifExamen, pk=pk)

    tarif.actif = not tarif.actif
    tarif.save(update_fields=['actif', 'updated_at'])

    messages.success(
        request,
        f"Le tarif de l'examen est maintenant {'actif' if tarif.actif else 'inactif'}."
    )

    return redirect('parametrage_general:liste_tarifs_examens')

