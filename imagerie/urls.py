from django.urls import path
from . import views

app_name = 'imagerie'

urlpatterns = [
    path('', views.index, name='index'),
]
