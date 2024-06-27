import os
import xml.etree.ElementTree as ET
from flask import Blueprint, jsonify, request
from models.empleado import Empleado
from controllers.estructuras import Estructuras
empleados = Estructuras().empleados

BlueprintEmpleado = Blueprint('empleado', __name__)

@BlueprintEmpleado.route('/empleados/carga', methods=['POST'])
def cargarEmpleados():
    try:
        # OBTENEMOS EL XML
        xml_entrada = request.data.decode('utf-8')
        if not xml_entrada:
            return jsonify({
                'message': 'Error al cargar los empleados: EL XML está vacío',
                'status': 404
            }), 404
        
        xml_entrada = xml_entrada.replace('\n', '')
        root = ET.fromstring(xml_entrada)
        empleados_existentes = precargarEmpleados()
        for empleado in root.findall('empleado'):
            codigo = empleado.get('codigo')
            nombre = empleado.find('nombre').text
            puesto = empleado.find('puesto').text
            
            if any(e.codigo == codigo for e in empleados_existentes):
                print(f"Empleado con código {codigo} ya existe. No se agregará.")
                continue
            
            nuevo = add_empleado(codigo, nombre, puesto)
            if nuevo:
                empleados.append(nuevo)
                empleados_existentes.append(nuevo)
                
                if os.path.exists('database/empleados.xml'):
                    tree2 = ET.parse('database/empleados.xml')
                    root2 = tree2.getroot()
                    nuevo_empleado = ET.SubElement(root2, 'empleado', codigo=codigo)
                    ET.SubElement(nuevo_empleado, 'nombre').text = nombre
                    ET.SubElement(nuevo_empleado, 'puesto').text = puesto

                    ET.indent(root2, space='\t', level=0)
                    tree2.write('database/empleados.xml', encoding='utf-8', xml_declaration=True)

        # SI EN DADO CASO NO EXISTE EL XML, LO CREAMOS
        if not os.path.exists('database/empleados.xml'):
            root = ET.Element('empleados')
            for empleado in empleados:
                nuevo_empleado = ET.SubElement(root, 'empleado', codigo=empleado.codigo)
                ET.SubElement(nuevo_empleado, 'nombre').text = empleado.nombre
                ET.SubElement(nuevo_empleado, 'puesto').text = empleado.puesto
            ET.indent(root, space='\t', level=0)
            tree = ET.ElementTree(root)
            tree.write('database/empleados.xml', encoding='utf-8', xml_declaration=True)

        return jsonify({
            'message': 'Empleados cargados correctamente',
            'status': 200
        }), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'message': f'Error al cargar los empleados: {str(e)}',
            'status': 404
        }), 404

@BlueprintEmpleado.route('/empleados/verempleados', methods=['GET'])
def obtenerEmpleados():
    emp = precargarEmpleados()
    diccionario_salida = {
        'mensaje': 'Empleados encontrados',
        'empleados': [],
        'status': 200
    }
    for empleado in emp:
        diccionario_salida['empleados'].append({
            'codigo': empleado.codigo,
            'nombre': empleado.nombre,
            'puesto': empleado.puesto,
        })
    return jsonify(diccionario_salida), 200

def add_empleado(codigo, nombre, puesto):
    if verificacionEmpleado(codigo) is not None:
        print(f"Error: El empleado con código '{codigo}' ya existe.")
        return None
    
    nuevo = Empleado(codigo, nombre, puesto)
    return nuevo

def verificacionEmpleado(codigo):
    empleados = precargarEmpleados()
    for empleado in empleados:
        if empleado.codigo == codigo:
            return empleado
    return None

def precargarEmpleados():
    emp = []
    if os.path.exists('database/empleados.xml'):
        tree = ET.parse('database/empleados.xml')
        root = tree.getroot()
        for empleado in root.findall('empleado'):
            codigo = empleado.get('codigo')
            nombre = empleado.find('nombre').text
            puesto = empleado.find('puesto').text
            nuevo = Empleado(codigo, nombre, puesto)
            emp.append(nuevo)
    return emp
