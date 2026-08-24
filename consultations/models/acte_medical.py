from django.db import models


class ActeMedical(models.Model):
    consultation = models.ForeignKey('consultations.Consultation', on_delete=models.CASCADE, related_name='actes_medicales')
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Acte médical'
        verbose_name_plural = 'Actes médicaux'

    def __str__(self):
        return self.nom
