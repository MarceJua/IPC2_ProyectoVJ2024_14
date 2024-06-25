from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('productos/', views.productos_view, name='productos'),
    path('compras/', views.compras_view, name='compras'),
    path('carga/', views.admincarga_view, name='carga'),
    path('user/', views.user_view, name='user'),
    path('signin/', views.signin, name='signin'),
    path('cargaxml/', views.cargarXML, name='cargaxml'),
    path('xmlproductos/', views.enviarProductos, name='xmlproductos'),
    path('xmlusuarios/', views.enviarUsuarios, name='xmlusuarios'),
    path('xmlempleados/', views.enviarEmpleados, name='xmlempleados'),
    path('xmlactividades/', views.enviarActividades, name='xmlactividades'),
    path('productosAdmin/', views.verProductos, name='productosAdmin'),
    path('estadisticas/', views.verEstadisticas, name='estadisticas'),
    path('pdf/', views.verPDF, name='pdf'),
    path('logout/', views.logout, name='logout'),
    path('comprar/', views.comprapage, name='comprar'),
    path('search/', views.buscarProducto, name='search'),
    path('addCart/', views.agregarCarrito, name='addCart'),
    path('compro/', views.comprar, name='compro'),
    path('vercarrito/', views.verCarrito, name='vercarrito'),
    path('vercompras/', views.mostrarcompras, name='vercompras'),
]