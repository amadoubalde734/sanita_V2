from django.urls import path
from . import views

app_name = 'ordonnances'

urlpatterns = [
    path('', views.index, name='index'),
]
