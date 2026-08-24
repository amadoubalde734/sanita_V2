from django.db import models


class Orientation(models.Model):
    consultation = models.ForeignKey('consultations.Consultation', on_delete=models.CASCADE, related_name='orientations')
    destination = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Orientation'
        verbose_name_plural = 'Orientations'

    def __str__(self):
        return self.destination
