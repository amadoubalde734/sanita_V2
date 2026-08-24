from django.db import models


class Famille(models.Model):
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Famille'
        verbose_name_plural = 'Familles'

    def __str__(self):
        return self.nom
