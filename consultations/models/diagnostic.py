from django.db import models


class Diagnostic(models.Model):
    consultation = models.ForeignKey('consultations.Consultation', on_delete=models.CASCADE, related_name='diagnostics')
    description = models.TextField()

    class Meta:
        verbose_name = 'Diagnostic'
        verbose_name_plural = 'Diagnostics'

    def __str__(self):
        return f"Diagnostic pour {self.consultation}"
