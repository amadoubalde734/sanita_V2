from django.db import models


class HistoriqueConsultation(models.Model):
    consultation = models.ForeignKey('consultations.Consultation', on_delete=models.CASCADE, related_name='historiques')
    action = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Historique de consultation'
        verbose_name_plural = 'Historiques de consultation'

    def __str__(self):
        return f"{self.action} - {self.date:%d/%m/%Y}"
