import os
import xml.etree.ElementTree as ET
from flask import Blueprint, jsonify, request
from models.actividad import Actividad
from controllers.estructuras import actividades

BlueprintActividad = Blueprint('actividad', __name__)

@BlueprintActividad.route('/actividades/carga', methods=['POST'])
def cargarActividades():
    try:
        # OBTENEMOS EL XML
        xml_entrada = request.data.decode('utf-8')
        if xml_entrada == '':
            return jsonify({
                'message': 'Error al cargar las actividades: EL XML está vacío',
                'status': 404
            }), 404

        # QUITARLE LOS SALTOS DE LÍNEA INNECESARIOS
        xml_entrada = xml_entrada.replace('\n', '')

        # LEER EL XML
        root = ET.fromstring(xml_entrada)
        actividades_existentes = precargaActividades()
        for actividad in root.findall('actividad'):
            id = actividad.get('id')
            nombre = actividad.find('nombre').text
            descripcion = actividad.find('descripcion').text
            empleado = actividad.find('empleado').text
            dia_element = actividad.find('dia')
            dia = dia_element.text
            hora = dia_element.get('hora')

            # Validar dia y hora
            if not dia.isdigit() or not (1 <= int(dia) <= 7):
                print(f"Error: El dia '{dia}' no es válido. Debe ser un número del 1 al 7.")
                continue  # Saltar esta actividad si el dia no es válido

            if not hora.isdigit() or not (0 <= int(hora) <= 23):
                print(f"Error: La hora '{hora}' no es válida. Debe ser un número del 0 al 23.")
                continue  # Saltar esta actividad si la hora no es válida

            # Verificar si la actividad ya existe en la lista cargada desde el archivo XML
            if any(ac.id == id for ac in actividades_existentes):
                print(f"Actividad con ID {id} ya existe. No se agregará.")
                continue  # Saltar a la siguiente iteración si la actividad ya existe

            nuevo = add_actividad(id, nombre, descripcion, empleado, dia, hora)
            if nuevo is not None:
                actividades.append(nuevo)
                actividades_existentes.append(nuevo)  # Actualizar la lista de actividades existentes

                # AGREGAMOS LA ACTIVIDAD AL XML QUE YA EXISTE
                if os.path.exists('database/actividades.xml'):
                    tree2 = ET.parse('database/actividades.xml')
                    root2 = tree2.getroot()
                    nueva_actividad = ET.Element('actividad', id=nuevo.id)
                    ET.SubElement(nueva_actividad, 'nombre').text = nuevo.nombre
                    ET.SubElement(nueva_actividad, 'descripcion').text = nuevo.descripcion
                    ET.SubElement(nueva_actividad, 'empleado').text = nuevo.empleado
                    dia_elem = ET.SubElement(nueva_actividad, 'dia', hora=nuevo.hora)
                    dia_elem.text = nuevo.dia

                    root2.append(nueva_actividad)
                    ET.indent(root2, space='\t', level=0)
                    tree2.write('database/actividades.xml', encoding='utf-8', xml_declaration=True)

        # SI EN DADO CASO NO EXISTE EL XML, LO CREAMOS
        if not os.path.exists('database/actividades.xml'):
            root = ET.Element("actividades")
            for actividad in actividades:
                nueva_actividad = ET.Element('actividad', id=actividad.id)
                ET.SubElement(nueva_actividad, 'nombre').text = actividad.nombre
                ET.SubElement(nueva_actividad, 'descripcion').text = actividad.descripcion
                ET.SubElement(nueva_actividad, 'empleado').text = actividad.empleado
                dia_elem = ET.SubElement(nueva_actividad, 'dia', hora=actividad.hora)
                dia_elem.text = actividad.dia

                root.append(nueva_actividad)
            ET.indent(root, space='\t', level=0)
            tree = ET.ElementTree(root)
            tree.write('database/actividades.xml', encoding='utf-8', xml_declaration=True)

        return jsonify({
            'message': 'Actividades cargadas correctamente',
            'status': 200
        }), 200

    except Exception as e:
        print(f"Error al cargar las actividades: {str(e)}")
        return jsonify({
            'message': f'Error al cargar las actividades: {str(e)}',
            'status': 404
        }), 404

def add_actividad(id, nombre, descripcion, empleado, dia, hora):
    if verificacionActividad(id) is not None:
        print(f"Error: La actividad con código '{id}' ya existe.")
        return None
    nuevo = Actividad(id, nombre, descripcion, empleado, dia, hora)
    return nuevo

def verificacionActividad(id):
    actividades = precargaActividades()
    for actividad in actividades:
        if actividad.id == id:
            return actividad
    return None

def precargaActividades():
    try:
        activ = []
        if os.path.exists('database/actividades.xml'):
            tree = ET.parse('database/actividades.xml')
            root = tree.getroot()
            for actividad in root.findall('actividad'):
                id = actividad.get('id')
                nombre = actividad.find('nombre').text
                descripcion = actividad.find('descripcion').text
                empleado = actividad.find('empleado').text
                dia_element = actividad.find('dia')
                dia = dia_element.text
                hora = dia_element.get('hora')
                activ.append(Actividad(id, nombre, descripcion, empleado, dia, hora))
        return activ
    except Exception as e:
        print(f"Error al precargar las actividades: {str(e)}")
        return []
