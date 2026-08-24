from django.db import models


class Hospitalisation(models.Model):
    patient = models.CharField(max_length=255)
    date_entree = models.DateTimeField()
    date_sortie = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Hospitalisation'
        verbose_name_plural = 'Hospitalisations'

    def __str__(self):
        return f"Hospitalisation de {self.patient}"
