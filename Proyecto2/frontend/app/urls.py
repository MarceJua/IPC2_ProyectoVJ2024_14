from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('productos/', views.productos_view, name='productos'),
    path('compras/', views.compras_view, name='compras'),
]