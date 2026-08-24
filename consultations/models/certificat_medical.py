from django.db import models


class CertificatMedical(models.Model):
    consultation = models.ForeignKey('consultations.Consultation', on_delete=models.CASCADE, related_name='certificats')
    contenu = models.TextField()

    class Meta:
        verbose_name = 'Certificat médical'
        verbose_name_plural = 'Certificats médicaux'

    def __str__(self):
        return f"Certificat pour {self.consultation}"
