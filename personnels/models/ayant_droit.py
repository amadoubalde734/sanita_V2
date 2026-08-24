from django.db import models
from .employe import Employe


class AyantDroit(models.Model):
    TYPE_CHOICES = [
        ('ENFANT', 'Enfant'),
        ('CONJOINT', 'Conjoint(e)'),
        ('AUTRE', 'Autre ayant droit'),
    ]

    employe = models.ForeignKey(
        Employe,
        on_delete=models.CASCADE,
        related_name='ayants_droit',
        verbose_name='Employé'
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='ENFANT')
    nom = models.CharField(max_length=150)
    prenoms = models.CharField(max_length=150)
    date_naissance = models.DateField(blank=True, null=True)
    lien_parente = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='ayants_droit/photos/', blank=True, null=True)

    class Meta:
        verbose_name = 'Ayant droit'
        verbose_name_plural = 'Ayants droit'

    def __str__(self):
        return f"{self.get_type_display()} - {self.nom} {self.prenoms}"
