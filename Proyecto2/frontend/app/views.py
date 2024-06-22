from django.shortcuts import render
import requests

# Create your views here.

def login_view(request):
    return render(request, 'login.html')

def productos_view(request):
    return render(request, 'productos.html')

def compras_view(request):
    return render(request, 'compras.html')

"""enpoint = 'http://127.0.0.1:4000/'
def home(request):
    response = requests.get(enpoint + 'showall')
    usuario = response.json()
    context = {
        'usuario': usuario
    }
    return render(request, 'index.html', context)"""