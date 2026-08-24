from django.db import models


class Referement(models.Model):
    consultation = models.ForeignKey('consultations.Consultation', on_delete=models.CASCADE, related_name='referements')
    destination = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Référencement'
        verbose_name_plural = 'Référencements'

    def __str__(self):
        return self.destination
