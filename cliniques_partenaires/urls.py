from django.urls import path
from . import views

app_name = 'cliniques_partenaires'

urlpatterns = [
    path('', views.index, name='index'),
]
