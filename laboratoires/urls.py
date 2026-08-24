from django.urls import path
from . import views

app_name = 'laboratoires'

urlpatterns = [
    path('', views.index, name='index'),
]
