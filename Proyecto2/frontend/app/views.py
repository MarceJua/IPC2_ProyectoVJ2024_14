from django.shortcuts import render
import requests

# Create your views here.

enpoint = 'http://127.0.0.1:4000'
def home(request):
    response = requests.get(enpoint + 'showall')
    usuario = response.json()
    context = {
        'usuario': usuario
    }
    return render(request, 'index.html', context)