from django.db import models
from .employe import Employe
from .ayant_droit import AyantDroit


class Conjoint(AyantDroit):
    certificat_mariage = models.FileField(upload_to='ayants_droit/certificats_mariage/', blank=True, null=True)

    class Meta:
        verbose_name = 'Conjoint'
        verbose_name_plural = 'Conjoints'
