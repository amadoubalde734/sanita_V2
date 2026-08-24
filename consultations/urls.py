from django.urls import path
from . import views

app_name = 'consultations'

urlpatterns = [
    path('', views.index, name='index'),
    path('consultation/', views.consultation_list, name='consultation_list'),
    path('consultation/ajouter/', views.consultation_add, name='consultation_add'),
    path('consultation/<int:pk>/', views.consultation_detail, name='consultation_detail'),
    path('hospitalisation/', views.hospitalisation_list, name='hospitalisation_list'),
    path('rendez_vous/', views.rendez_vous_list, name='rendez_vous_list'),
    path('arret_travail/', views.arret_travail_list, name='arret_travail_list'),
    path('orientation/', views.orientation_list, name='orientation_list'),
    path('referement/', views.referement_list, name='referement_list'),
]
