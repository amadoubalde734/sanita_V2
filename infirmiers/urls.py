from django.urls import path
from . import views

app_name = 'infirmiers'

urlpatterns = [
    path('', views.index, name='index'),
]
