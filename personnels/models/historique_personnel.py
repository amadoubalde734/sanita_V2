from django.db import models
from django.contrib.auth import get_user_model
from .employe import Employe

User = get_user_model()


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StatusModel(models.Model):
    actif = models.BooleanField(default=True)

    class Meta:
        abstract = True


class HistoriqueEmploye(TimeStampedModel, StatusModel):
    ACTION_CHOICES = [
        ('CREATION', 'Création'),
        ('MODIFICATION', 'Modification'),
        ('PROMOTION', 'Promotion'),
        ('DEPART', 'Départ'),
        ('CONGES', 'Congés'),
        ('FORMATION', 'Formation'),
        ('HABILITATION', 'Habilitation'),
        ('CHANGEMENT_RESPONSABLE', 'Changement de responsable')
    ]

    employe = models.ForeignKey(
        Employe,
        on_delete=models.CASCADE,
        related_name='historiques',
        verbose_name="Employé"
    )
    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
        verbose_name="Type d'action"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description / Détails")
    date_action = models.DateTimeField(auto_now_add=True, verbose_name="Date de l'action")
    utilisateur = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Utilisateur ayant effectué l'action"
    )

    class Meta:
        verbose_name = "Historique Employé"
        verbose_name_plural = "Historiques Employés"
        ordering = ['-date_action']
        indexes = [
            models.Index(fields=['employe', 'date_action']),
        ]

    def __str__(self):
        return f"{self.get_action_display()} - {self.employe.nom} {self.employe.prenoms} le {self.date_action.strftime('%d/%m/%Y %H:%M')}"
