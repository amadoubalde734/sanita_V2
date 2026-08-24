from django.urls import path
from . import views

app_name = 'pharmacie'

urlpatterns = [
    path('', views.index, name='index'),
]
