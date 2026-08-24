from django.db import models


class Consultation(models.Model):
    patient = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    motif = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Consultation'
        verbose_name_plural = 'Consultations'

    def __str__(self):
        return f"Consultation de {self.patient} le {self.date:%d/%m/%Y}"
