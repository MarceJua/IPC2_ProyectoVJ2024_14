import os
from xml.etree import ElementTree as ET
import re

from controllers.estructuras import users
from flask import Blueprint, jsonify, request
from models.user import User

BlueprintUser = Blueprint('user', __name__)
user_logueado = ''

@BlueprintUser.route('/usuarios/carga', methods=['POST'])
def cargarUsuarios():
    try:
        # OBTENEMOS EL XML
        xml_entrada = request.data.decode('utf-8')
        if xml_entrada == '':
            return jsonify({
                'message': 'Error al cargar los usuarios: EL XML está vacio',
                'status': 404
            }), 404
        
        # QUITARLE LOS SALTOS DE LINEA INNECESARIOS
        xml_entrada = xml_entrada.replace('\n', '')
        
        # LEER EL XML
        root = ET.fromstring(xml_entrada)
        usuarios_existentes = precargarUsuarios()
        
        for user in root:
            id = user.attrib['id']
            password = user.attrib['password']
            nombre = ''
            edad = ''
            email = ''
            telefono = ''
            for elemento in user:
                if elemento.tag == 'nombre':
                    nombre = elemento.text
                if elemento.tag == 'edad':
                    edad = elemento.text
                if elemento.tag == 'email':
                    email = elemento.text
                if elemento.tag == 'telefono':
                    telefono = elemento.text

            # Verificar si el usuario ya existe en la lista cargada desde el archivo XML
            if any(u.id == id for u in usuarios_existentes):
                print(f"Usuario con ID {id} ya existe. No se agregará.")
                continue  # Saltar a la siguiente iteración si el usuario ya existe

            nuevo = agregarUsuario(id, password, nombre, edad, email, telefono)
            if nuevo is not None:
                users.append(nuevo)
                usuarios_existentes.append(nuevo)  # Actualizar la lista de usuarios existentes

                # AGREGAMOS EL USUARIO AL XML QUE YA EXISTE
                if os.path.exists('database/usuarios.xml'):
                    tree2 = ET.parse('database/usuarios.xml')
                    root2 = tree2.getroot()
                    nuevo_usuario = ET.Element('usuario', id=nuevo.id, password=nuevo.password)
                    nombre_elem = ET.SubElement(nuevo_usuario, 'nombre')
                    nombre_elem.text = nuevo.nombre
                    edad_elem = ET.SubElement(nuevo_usuario, 'edad')
                    edad_elem.text = nuevo.edad
                    email_elem = ET.SubElement(nuevo_usuario, 'email')
                    email_elem.text = nuevo.email
                    telefono_elem = ET.SubElement(nuevo_usuario, 'telefono')
                    telefono_elem.text = nuevo.telefono
                    root2.append(nuevo_usuario)
                    ET.indent(root2, space='\t', level=0)
                    tree2.write('database/usuarios.xml', encoding='utf-8', xml_declaration=True)
        
        # SI EN DADO CASO NO EXISTE EL XML, LO CREAMOS
        if not os.path.exists('database/usuarios.xml'):
            root = ET.Element("usuarios")
            for user in users:
                nuevo_usuario = ET.Element('usuario', id=user.id, password=user.password)
                nombre_elem = ET.SubElement(nuevo_usuario, 'nombre')
                nombre_elem.text = user.nombre
                edad_elem = ET.SubElement(nuevo_usuario, 'edad')
                edad_elem.text = user.edad
                email_elem = ET.SubElement(nuevo_usuario, 'email')
                email_elem.text = user.email
                telefono_elem = ET.SubElement(nuevo_usuario, 'telefono')
                telefono_elem.text = user.telefono
                root.append(nuevo_usuario)
            tree = ET.ElementTree(root)
            ET.indent(root, space='\t', level=0)
            tree.write('database/usuarios.xml', encoding='utf-8', xml_declaration=True)
            
        return jsonify({
            'message': 'Usuarios cargados correctamente',
            'status': 200
        }), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'message': 'Error al cargar los usuarios',
            'status': 404
        }), 404

def agregarUsuario(id, password, nombre, edad, email, telefono):
    # Validar el correo electrónico
    if not validarEmail(email):
        print(f"Error: El correo electrónico '{email}' no tiene un formato válido.")
        return None
    # Validar el teléfono
    if not validarTelefono(telefono):
        print(f"Error: El número de teléfono '{telefono}' no es válido. Debe contener exactamente 8 dígitos.")
        return None
    if verificacionUsuario(id) is not None:
        print(f"Error: El usuario con ID '{id}' ya existe.")
        return None
    nuevo = User(id, password, nombre, edad, email, telefono)
    return nuevo

def validarEmail(email):
    # Expresión regular para validar un correo electrónico
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(patron, email) is not None

def validarTelefono(telefono):
    # Verifica que el teléfono tenga exactamente 8 dígitos
    return telefono.isdigit() and len(telefono) == 8

def verificacionUsuario(id):
    auxUser = precargarUsuarios()
    if auxUser is not None:
        for user in auxUser:
            if user.id == id:
                return user
    else:
        for user in users:
            if user.id == id:
                return user
    return None

@BlueprintUser.route('/usuarios/verUsuarios', methods=['GET'])
def obtenerUsuarios():
    users = precargarUsuarios()
    diccionario_salida = {
        'mensaje': 'Usuarios encontrados',
        'usuarios': [],
        'status': 200
    }
    for usuario in users:
        diccionario_salida['usuarios'].append({
            'id': usuario.id,
            'nombre': usuario.nombre,
            'edad': usuario.edad,
            'email': usuario.email,
            'telefono': usuario.telefono,
            'password': usuario.password
        })
    return jsonify(diccionario_salida), 200

@BlueprintUser.route('/usuarios/verXML', methods=['GET'])
def verXMLUsuarios():
    try:
        xml_salida = ''
        with open('database/usuarios.xml', 'r', encoding='utf-8') as file:
            xml_salida = file.read()
        return jsonify({
            'message': 'XML de usuarios encontrado',
            'xml_salida': xml_salida,
            'status': 200
        }), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'message': 'Error al cargar los usuarios',
            'status': 404
        }), 404

@BlueprintUser.route('/usuarios/login', methods=['POST'])
def Login():
    global user_logueado
    users = precargarUsuarios()
    id = request.json['id']
    password = request.json['password']
    if id == 'AdminIPC2' and password == 'IPC2VJ2024':
        user_logueado = id
        return jsonify({
            'message': 'Usuario logueado correctamente',
            'role': 0,
            'status': 200
        })
    for user in users:
        if user.id == id and user.password == password:
            return jsonify({
                'message': 'Usuario logueado correctamente',
                'role': 1,
                'status': 200
            }), 200
    return jsonify({
        'message': 'Usuario no encontrado',
        'role': 0,
        'status': 404
    }), 404

@BlueprintUser.route('/usuarios/obtenerLogueado', methods=['GET'])
def obtenerLogueado():
    global user_logueado
    return jsonify({
        'usuario': user_logueado,
        'status': 200
    }), 200

# METODO DE PRECARGAR USUARIOS
def precargarUsuarios():
    usuarios = []
    if os.path.exists('database/usuarios.xml'):
        tree = ET.parse('database/usuarios.xml')
        root = tree.getroot()
        for usuario in root:
            id = usuario.attrib['id']
            password = usuario.attrib['password']
            nombre = ''
            edad = ''
            email = ''
            telefono = ''
            for elemento in usuario:
                if elemento.tag == 'nombre':
                    nombre = elemento.text
                if elemento.tag == 'edad':
                    edad = elemento.text
                if elemento.tag == 'email':
                    email = elemento.text
                if elemento.tag == 'telefono':
                    telefono = elemento.text
            nuevo = User(id, password, nombre, edad, email, telefono)
            usuarios.append(nuevo)
    return usuarios
