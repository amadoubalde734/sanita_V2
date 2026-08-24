from django.db import models


class ArretTravail(models.Model):
    consultation = models.ForeignKey('consultations.Consultation', on_delete=models.CASCADE, related_name='arrets_travail')
    date_debut = models.DateField()
    date_fin = models.DateField()

    class Meta:
        verbose_name = 'Arrêt de travail'
        verbose_name_plural = 'Arrêts de travail'

    def __str__(self):
        return f"Arrêt de travail du {self.date_debut:%d/%m/%Y}"
