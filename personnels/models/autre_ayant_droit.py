from django.db import models
from .employe import Employe
from .ayant_droit import AyantDroit


class AutreAyantDroit(AyantDroit):

    class Meta:
        verbose_name = 'Autre ayant droit'
        verbose_name_plural = 'Autres ayants droit'
