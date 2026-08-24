from django.db import models
from .employe import Employe
from .ayant_droit import AyantDroit


class Enfant(AyantDroit):
    extrait_naissance = models.FileField(upload_to='ayants_droit/extraits_naissance/', blank=True, null=True)

    class Meta:
        verbose_name = 'Enfant'
        verbose_name_plural = 'Enfants'
