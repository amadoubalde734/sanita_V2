from django.urls import path
from . import views

app_name = 'medicaments'

urlpatterns = [
    path('', views.index, name='index'),
]
