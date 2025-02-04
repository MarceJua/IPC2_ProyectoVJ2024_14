import json

import requests
#para mostrar mensajes en pantalla
from django.contrib import messages
#para el cache
from django.core.cache import cache
#para las cookies
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from .forms import FileForm, LoginForm, SearchForm, CantidadForm

# Create your views here.
endpoint = 'http://localhost:4000/'

contexto = {
    'user':None,
    'contenido_archivo':None,
    'binario_xml':None
}


def login_view(request):
    return render(request, 'login.html')

def logout(request):
    response = redirect('login')
    response.delete_cookie('id_user')
    return response

def productos_view(request):
    return render(request, 'productos.html')

def compras_view(request):
    return render(request, 'compras.html')

def admincarga_view(request):
    return render(request, 'cargaadmin.html')

def user_view(request):
    ctx = {
        'Productos':None,
        'title':'Productos'
    }
    url = endpoint + 'productos/verProducto'
    response = requests.get(url)
    data = response.json()
    ctx['productos'] = data['productos']
    return render(request, 'user.html', ctx)

def signin(request):
    try:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                #obtenemos los datos del formulario
                iduser = form.cleaned_data['iduser']
                password = form.cleaned_data['password']

                #PETICION AL BACKEND
                #ENDPOINT- URL
                url = endpoint + 'usuarios/login'
                #DATA A ENVIAR
                data = {
                    'id': iduser,
                    'password': password
                }

                #convertimos los datos a json
                json_data = json.dumps(data)

                #HEADERS
                headers = {
                    'Content-Type': 'application/json'
                }

                #llamamos a la peticion backend
                response = requests.post(url, data=json_data, headers=headers)
                respuesta = response.json()
                if response.status_code == 200:
                    rol = int(respuesta['role'])
                    contexto['user'] = iduser
                    pagina_redireccion = None
                    #IR A ADMIN
                    if rol == 0:
                        #si yo quiero almacenar el usuario en cache
                        #cache.set('id_user', iduser, timeout=None)
                        #si yo quiero almacenar el usuario en cookies
                        pagina_redireccion = redirect('carga')
                        pagina_redireccion.set_cookie('id_user', iduser)
                        return pagina_redireccion
                    elif rol == 1:
                        #si yo quiero almacenar el usuario en cache
                        #cache.set('id_user', iduser, timeout=None)
                        #si yo quiero almacenar el usuario en cookies
                        pagina_redireccion = redirect('user')
                        pagina_redireccion.set_cookie('id_user', iduser)
                        return pagina_redireccion


    except:
        return render(request, 'login.html')

def admincarga(request):
    ctx = {
        'title':'Carga Masiva'
    }
    return render(request, 'cargaadmin.html', ctx)

def cargarXML(request):
    ctx = {
        'contenido_archivo':None
    }
    try:
        if request.method == 'POST':
            #obtenemos el formulario
            form = FileForm(request.POST, request.FILES)
            print(form.is_valid())
            if form.is_valid():
                #obtenemos el archivo
                archivo = request.FILES['file']
                #guardamos el binario
                xml = archivo.read()
                xml_decodificado = xml.decode('utf-8')
                #guardamos el contenido del archivo
                contexto['binario_xml'] = xml
                contexto['contenido_archivo'] = xml_decodificado
                ctx['contenido_archivo'] = xml_decodificado
                return render(request, 'cargaadmin.html', ctx)
    except:
        return render(request, 'cargaadmin.html')


def enviarProductos(request):
    try:
        if request.method == 'POST':
            xml = contexto['binario_xml']
            if xml is None:
                messages.error(request, 'No se ha cargado ningun archivo')
                return render(request, 'cargaadmin.html')
            
            #PETICION AL BACKEND
            url = endpoint + 'productos/carga'
            respuesta = requests.post(url, data=xml)
            mensaje = respuesta.json()
            messages.success(request, mensaje['message'])
            contexto['binario_xml'] = None
            contexto['contenido_archivo'] = None
            return render(request, 'cargaadmin.html', contexto)
    except:
        return render(request, 'cargaadmin.html')

def enviarUsuarios(request):
    try:
        if request.method == 'POST':
            xml = contexto['binario_xml']
            if xml is None:
                messages.error(request, 'No se ha cargado ningun archivo')
                return render(request, 'cargaadmin.html')
            
            #PETICION AL BACKEND
            url = endpoint + 'usuarios/carga'
            respuesta = requests.post(url, data=xml)
            mensaje = respuesta.json()
            messages.success(request, mensaje['message'])
            contexto['binario_xml'] = None
            contexto['contenido_archivo'] = None
            return render(request, 'cargaadmin.html', contexto)
    except:
        return render(request, 'cargaadmin.html')
    
def enviarEmpleados(request):
    try:
        if request.method == 'POST':
            xml = contexto['binario_xml']
            if xml is None:
                messages.error(request, 'No se ha cargado ningun archivo')
                return render(request, 'cargaadmin.html')
            
            #PETICION AL BACKEND
            url = endpoint + 'empleados/carga'
            respuesta = requests.post(url, data=xml)
            mensaje = respuesta.json()
            messages.success(request, mensaje['message'])
            contexto['binario_xml'] = None
            contexto['contenido_archivo'] = None
            return render(request, 'cargaadmin.html', contexto)
    except:
        return render(request, 'cargaadmin.html')

def enviarActividades(request):
    try:
        if request.method == 'POST':
            xml = contexto['binario_xml']
            if xml is None:
                messages.error(request, 'No se ha cargado ningun archivo')
                return render(request, 'cargaadmin.html')
            
            #PETICION AL BACKEND
            url = endpoint + 'actividades/carga'
            respuesta = requests.post(url, data=xml)
            mensaje = respuesta.json()
            messages.success(request, mensaje['message'])
            contexto['binario_xml'] = None
            contexto['contenido_archivo'] = None
            return render(request, 'cargaadmin.html', contexto)
    except:
        return render(request, 'cargaadmin.html')
    
def verEstadisticas(request):
    ctx = {
        'title':'Estadisticas'
    }
    return render(request, 'estadisticas.html', ctx)

def verProductos(request):
    ctx = {
        'Productos':None,
        'title':'Productos'
    }
    url = endpoint + 'productos/verProducto'
    response = requests.get(url)
    data = response.json()
    ctx['productos'] = data['productos']
    return render(request, 'verProductosAdmin.html', ctx)


def verPDF(request):
    cxt = {
        'show_pdf': True
    }
    
    if 'info' in request.GET:
        cxt['show_pdf'] = False
    
    return render(request, 'verpdf.html', cxt)

def userview(request):
    return render(request, 'user.html')

def comprapage(request):
    return render(request, 'compraUser.html')

ctx_producto = {
    'id_producto':None
}

def buscarProducto(request):
    ctx = {
        'producto_encontrado':None
    }
    try:
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                idproducto = form.cleaned_data['idproducto']
                ctx_producto['id_producto'] = idproducto
                url = endpoint + 'productos/ver/'+idproducto
                response = requests.get(url)
                data = response.json()
                producto = data.get('producto')
                ctx['producto_encontrado'] = producto

                return render(request, 'compraUser.html', ctx)
    except:
        return render(request, 'compraUser.html')
    
def agregarCarrito(request):
    try:
        if request.method == 'POST':
            form = CantidadForm(request.POST)
            if form.is_valid():
                cantidad = form.cleaned_data['cantidad']
                idproducto = ctx_producto['id_producto']
                data = {
                    'idproducto':idproducto,
                    'cantidad':cantidad
                }
                url = endpoint + 'carro/agregar'
                response = requests.post(url, json=data)
                return render(request, 'compraUser.html')
    except:
        return render(request, 'compraUser.html')
    
def comprar(request):
    try:
        if request.method == 'POST':
            id_user = request.COOKIES.get('id_user')
            url = endpoint + 'comprar/agregar'
            data = {
                'id_user':id_user
            }
            headers = {'Content-type':'application/json'}
            response = requests.post(url, json=data, headers=headers)
            print(response.json())
            return render(request, 'compraUser.html')
    except:
        return render(request, 'compraUser.html')
    
def verCarrito(request):
    ctx = {
        'contenido_carrito':None
    }
    url = endpoint + 'carro/ver'
    response = requests.get(url)
    data = response.json()
    ctx['contenido_carrito'] = data['contenido']
    return render(request, 'verCarrito.html', ctx)

def mostrarcompras(request):
    ctx = {
        'usuarios': ''
    }
    if request.method == 'POST':
        url = endpoint + 'comprar/ver'
        response = requests.get(url)
        if response.status_code == 200:
            ctx['usuarios'] = response.text
        else:
            ctx['usuarios'] = 'Error al obtener usuarios'
    return render(request, 'reportesadmin.html', ctx)

def verActividades(request):
    ctx = {
        'actividades': None,
    }

    if request.method == 'POST':
        url = endpoint + 'actividades/hoy'
        response = requests.get(url)
        if response.status_code == 200:
            xml_content = response.json().get('xml_content', 'No hay actividades para hoy.')
            ctx['actividades'] = xml_content
        else:
            ctx['actividades'] = 'Error al obtener las actividades de hoy.'

    return render(request, 'reportesadmin.html', ctx)