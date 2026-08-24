from django.urls import path
from . import views

app_name = "entreprises"

urlpatterns = [
    path("", views.index, name="index"),
]