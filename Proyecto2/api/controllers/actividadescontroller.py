import os
import xml.etree.ElementTree as ET
from flask import Blueprint, jsonify, request
from models.actividad import Actividad
from controllers.estructuras import actividades
from datetime import datetime
from xml.dom import minidom

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


@BlueprintActividad.route('/actividades/veractividades', methods=['GET'])
def obtenerActividades():
    act = precargaActividades()
    diccionario_salida = {
        'mensaje': 'Actividades encontradas',
        'actividades': [],
        'status': 200
    }
    for actividad in act:
        diccionario_salida['actividades'].append({
            'id': actividad.id,
            'nombre': actividad.nombre,
            'descripcion': actividad.descripcion,
            'empleado': actividad.empleado,
            'dia': actividad.dia,
            'hora': actividad.hora
        })
    return jsonify(diccionario_salida), 200


@BlueprintActividad.route('/actividades/hoy', methods=['GET'])
def actividades_hoy():
    try:
        # Determinar el día actual de la semana (1=Lunes, 7=Domingo)
        dia_actual_num = datetime.now().isoweekday()
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        dia_actual_nombre = dias_semana[dia_actual_num - 1]

        # Precargar actividades y filtrar las actividades del día actual
        actividades_existentes = precargaActividades()
        actividades_hoy = [act for act in actividades_existentes if int(act.dia) == dia_actual_num]

        # Precargar empleados
        empleados = precargaEmpleados()

        # Crear el XML de respuesta
        root = ET.Element('Actividades_hoy')
        dia_elem = ET.SubElement(root, 'Dia')
        dia_elem.text = dia_actual_nombre
        actividades_elem = ET.SubElement(root, 'Actividades')

        for actividad in actividades_hoy:
            actividad_elem = ET.SubElement(actividades_elem, 'Actividad', id=actividad.id)
            ET.SubElement(actividad_elem, 'Nombre').text = actividad.nombre
            ET.SubElement(actividad_elem, 'Descripcion').text = actividad.descripcion
            
            empleado = next((emp for emp in empleados if emp['id'] == actividad.empleado), None)
            if empleado:
                empleado_elem = ET.SubElement(actividad_elem, 'Empleado', id=empleado['id'])
                empleado_elem.text = empleado['nombre']
            
            hora_elem = ET.SubElement(actividad_elem, 'Hora')
            hora_elem.text = f"{actividad.hora}:00"

        # Convertir el árbol XML a string y guardarlo en un archivo
        tree = ET.ElementTree(root)
        os.makedirs('database', exist_ok=True)
        file_path = os.path.join('database', 'actividades_hoy.xml')
        
        # Pretty print the XML
        xml_str = ET.tostring(root, encoding='utf-8')
        dom = minidom.parseString(xml_str)
        pretty_xml_as_string = dom.toprettyxml(indent="\t")
        
        # Write the pretty XML to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml_as_string)
        
        # Open the created XML file and return its content
        with open(file_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()

        return jsonify({
            'message': 'Archivo XML generado y guardado correctamente',
            'status': 200,
            'xml_content': xml_content
        }), 200

    except Exception as e:
        print(f"Error al obtener las actividades de hoy: {str(e)}")
        return jsonify({
            'message': f'Error al obtener las actividades de hoy: {str(e)}',
            'status': 404
        }), 404

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

def precargaEmpleados():
    try:
        empleados = []
        if os.path.exists('database/empleados.xml'):
            tree = ET.parse('database/empleados.xml')
            root = tree.getroot()
            for empleado in root.findall('empleado'):
                id = empleado.get('id')
                nombre = empleado.find('nombre').text
                empleados.append({'id': id, 'nombre': nombre})
        return empleados
    except Exception as e:
        print(f"Error al precargar los empleados: {str(e)}")
        return []