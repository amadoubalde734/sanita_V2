from django.db import models


class SigneVital(models.Model):
    consultation = models.ForeignKey('consultations.Consultation', on_delete=models.CASCADE, related_name='signes_vitaux')
    tension = models.CharField(max_length=50, blank=True)
    temperature = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'Signe vital'
        verbose_name_plural = 'Signes vitaux'

    def __str__(self):
        return f"Signes vitaux de {self.consultation}"
