from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('modules/', views.index_global, name='index_global'),
]