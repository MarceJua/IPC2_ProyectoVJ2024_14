import os
from xml.etree import ElementTree as ET

from controllers.estructuras import pruductos
from flask import Blueprint, jsonify, request
from models.producto import Producto

BlueprinProducto = Blueprint('producto', __name__)

@BlueprinProducto.route('/productos/carga', methods=['POST'])
def cargaProductos():
    try:
        # OBTENEMOS EL XML
        xml_entrada = request.data.decode('utf-8')
        if xml_entrada == '':
            return jsonify({
                'message': 'Error al cargar los libros: EL XML está vacio',
                'status': 404
            }), 404

        # QUITARLE LOS SALTOS DE LINEA INNECESARIOS
        xml_entrada = xml_entrada.replace('\n', '')

        # LEER EL XML
        root = ET.fromstring(xml_entrada)
        for producto in root:
            id = producto.attrib['id']
            nombre = ''
            precio = ''
            descripcion = ''
            categoria = ''
            cantidad = ''
            imagen = ''
            for elemento in producto:
                if elemento.tag == 'nombre':
                    nombre = elemento.text
                elif elemento.tag == 'precio':
                    precio = elemento.text
                elif elemento.tag == 'descripcion':
                    descripcion = elemento.text
                elif elemento.tag == 'categoria':
                    categoria = elemento.text
                elif elemento.tag == 'cantidad':
                    cantidad = elemento.text
                elif elemento.tag == 'imagen':
                    imagen = elemento.text

            nuevo = add_producto(id, nombre, precio, descripcion, categoria, cantidad, imagen)
            if nuevo is not None:
                pruductos.append(nuevo)

                # AGREGAMOS EL PRODUCTO AL XML QUE YA EXISTE
                if os.path.exists('database/productos.xml'):
                    tree2 = ET.parse('database/productos.xml')
                    root2 = tree2.getroot()
                    nuevo_producto = ET.Element('producto', id=nuevo.id)
                    nombre_elem = ET.SubElement(nuevo_producto, 'nombre')
                    nombre_elem.text = nuevo.nombre 
                    precio_elem = ET.SubElement(nuevo_producto, 'precio')
                    precio_elem.text = str(nuevo.precio)
                    descripcion_elem = ET.SubElement(nuevo_producto, 'descripcion')
                    descripcion_elem.text = nuevo.descripcion
                    categoria_elem = ET.SubElement(nuevo_producto, 'categoria')
                    categoria_elem.text = nuevo.categoria
                    cantidad_elem = ET.SubElement(nuevo_producto, 'cantidad')
                    cantidad_elem.text = str(nuevo.cantidad)
                    imagen_elem = ET.SubElement(nuevo_producto, 'imagen')
                    imagen_elem.text = nuevo.imagen
        
                    root2.append(nuevo_producto)
                    ET.indent(root2, space='\t', level=0)
                    tree2.write('database/productos.xml', encoding='utf-8', xml_declaration=True)
            
        # SI EN DADO CASO NO EXISTE EL XML, LO CREAMOS
        if not os.path.exists('database/productos.xml'):
            root = ET.Element("productos")
            for producto in pruductos:
                nuevo_producto = ET.Element('producto', id=producto.id)
                nombre_elem = ET.SubElement(nuevo_producto, 'nombre')
                nombre_elem.text = producto.nombre
                precio_elem = ET.SubElement(nuevo_producto, 'precio')
                precio_elem.text = str(producto.precio)
                descripcion_elem = ET.SubElement(nuevo_producto, 'descripcion')
                descripcion_elem.text = producto.descripcion
                categoria_elem = ET.SubElement(nuevo_producto, 'categoria')
                categoria_elem.text = producto.categoria
                cantidad_elem = ET.SubElement(nuevo_producto, 'cantidad')
                cantidad_elem.text = str(producto.cantidad)
                imagen_elem = ET.SubElement(nuevo_producto, 'imagen')
                imagen_elem.text = producto.imagen
                root.append(nuevo_producto)
            ET.indent(root, space='\t', level=0)
            tree = ET.ElementTree(root)
            tree.write('database/productos.xml', encoding='utf-8', xml_declaration=True)
            

        return jsonify({
            'message': 'Productos cargados correctamente',
            'status': 200
        }), 200

    except Exception as e:
        print(f"Error al cargar los Productos: {str(e)}")
        return jsonify({
            'message': 'Error al cargar los Productos',
            'status': 404
        }), 404

def add_producto(id, nombre, precio_str, descripcion, categoria, cantidad_str, imagen):
    # Validación del precio
    if not precio_str.replace('.', '', 1).isdigit():
        print(f"Error: El precio '{precio_str}' no es válido. Debe ser un número decimal.")
        return None

    precio = float(precio_str)
    # Validación de la cantidad
    if not cantidad_str.isdigit():
        print(f"Error: La cantidad '{cantidad_str}' no es válida. Debe ser un número entero.")
        return None
    if verificacionProducto(id) is not None:
        print(f"Error: El producto con id '{id}' ya existe.")
        return None
    cantidad = int(cantidad_str)
    # Creación del objeto Producto
    nuevo = Producto(id, precio, nombre, descripcion, categoria, cantidad, imagen)
    return nuevo

def verificacionProducto(id):
    auxproducto =precargaProducto()
    if auxproducto is not None:
     for producto in auxproducto:
            if producto.id == id:
                return producto
     return None
    else:
        for producto in pruductos:
            if producto.id == id:
                return producto
        return None
    
    

@BlueprinProducto.route('/productos/verXML', methods=['GET'])
def verXMLProductos():
    try:
        xml_salida = ''
        with open('database/productos.xml', 'r', encoding='utf-8') as file:
            xml_salida = file.read()
        return jsonify({
            'message': 'XML de productos encontrado',
            'xml_salida': xml_salida,
            'status': 200
        }), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'message': 'Error al cargar los productos',
            'status': 404
        }), 404
   


#METODO DE PRECARGAR 

def precargaProducto():
    produc = []
    if os.path.exists('database/productos.xml'):
        tree = ET.parse('database/productos.xml')
        root = tree.getroot()
        for producto in root:
            id = producto.attrib['id']
            nombre = ''
            precio = ''
            descripcion=''
            categoria=''
            cantidad=''
            imagen = ''
            for elemento in producto:
                if elemento.tag == 'nombre':
                    nombre = elemento.text
                if elemento.tag == 'precio':
                    precio = elemento.text
                if elemento.tag == 'descripcion':
                    descripcion = elemento.text
                if elemento.tag == 'categoria':
                    categoria = elemento.text
                if elemento.tag == 'cantidad':
                    cantidad=elemento.tag
                if elemento.tag == 'imagen':
                    imagen=elemento.tag
            
            nuevo = Producto(id, nombre,precio, descripcion, categoria,cantidad,imagen)
            produc.append(nuevo)
    return produc