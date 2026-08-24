from django.urls import path
from . import views

app_name = 'cartes_sanitaires'

urlpatterns = [
    path('', views.index, name='index'),

    path('liste/', views.liste, name='liste'),

    path('nouvelle/', views.nouvelle_carte, name='nouvelle'),

    path('qrcode/', views.qrcode, name='qrcode'),

    path('impression/', views.impression, name='impression'),
]