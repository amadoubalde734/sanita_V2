from django.db import models


class RendezVous(models.Model):
    patient = models.CharField(max_length=255)
    date = models.DateTimeField()
    statut = models.CharField(max_length=50, default='Prévu')

    class Meta:
        verbose_name = 'Rendez-vous'
        verbose_name_plural = 'Rendez-vous'

    def __str__(self):
        return f"Rendez-vous de {self.patient} le {self.date:%d/%m/%Y}"
