from django.urls import path
from . import views

app_name = 'consultations_dentaires'

urlpatterns = [
    path('', views.index, name='index'),
]
