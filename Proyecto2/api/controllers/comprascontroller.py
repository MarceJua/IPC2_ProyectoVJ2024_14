import os
import xml.etree.ElementTree as ET
from flask import Blueprint, jsonify,   request
from controllers.estructuras import carrito, compras
from controllers.carritocontroller import carrito as carro
from controllers.productocontroller import getproducto
from controllers.usercontroller import getUsuario
from models.compras import Compra
from models.carro import Carro
from models.buy import Buy



BlueprintCompra = Blueprint('compra', __name__)

@BlueprintCompra.route('/compras/cargarCarrito', methods=['POST'])
def cargarCarrito():
    try: 
        nombreproducto = request.args.get('nombre')
        cantidad = int(request.args.get('cantidad'))
        
        productos = precargaProducto()
        
        # Buscar el producto por nombre
        producto_encontrado = next((prod for prod in productos if prod['nombre'] == nombreproducto), None)
        
        if not producto_encontrado:
            return jsonify({
                'message': 'Producto no encontrado',
                'status': 404
            }), 404
        
        if cantidad > producto_encontrado['cantidad']:
            return jsonify({
                'message': 'Cantidad solicitada excede la cantidad disponible',
                'status': 400
            }), 400
        
        # Crear o actualizar el carrito
        item_carrito = next((item for item in carrito if item['nombre'] == nombreproducto), None)
        
        if item_carrito:
            item_carrito['cantidad'] += cantidad
        else:
            carrito.append({
                'id': producto_encontrado['id'],
                'nombre': producto_encontrado['nombre'],
                'Total': producto_encontrado['precio']*cantidad,
                'cantidad': cantidad,
                'imagen': producto_encontrado['imagen']
            })

        return jsonify({
            'message': 'Producto agregado al carrito correctamente',
            'status': 200
        }), 200

    except Exception as e:
        return jsonify({
            'message': f'Error al cargar el carrito: {str(e)}',
            'status': 404
        }), 404
    
#ver carrito xml
@BlueprintCompra.route('/compras/verCarrito', methods=['GET'])
def verCarrito():
    try:
        root = ET.Element('carrito')
        for item in carrito:
            item_elem = ET.SubElement(root, 'item', id=item['id'])
            ET.SubElement(item_elem, 'nombre').text = item['nombre']
            ET.SubElement(item_elem, 'total').text = str(item['Total'])
            ET.SubElement(item_elem, 'cantidad').text = str(item['cantidad'])
            ET.SubElement(item_elem, 'imagen').text = item['imagen']
        
        xml_salida = ET.tostring(root, encoding='utf-8').decode('utf-8')
        
        return jsonify({
            'message': 'Carrito de compras',
            'xml_salida': xml_salida,
            'status': 200
        }), 200

    except Exception as e:
        return jsonify({
            'message': f'Error al mostrar el carrito: {str(e)}',
            'status': 404
        }), 404
    
#confrimar compra

@BlueprintCompra.route('/compras/confirmarCompra', methods=['POST'])
def confirmarCompra():
    try:
        if not carrito:
            return jsonify({
                'message': 'El carrito está vacío',
                'status': 400
            }), 400
        
        # Calcular el total de la compra
        total_compra = sum(item['Total'] for item in carrito)
        
        # Registrar la compra
        compra = Compra(items=carrito.copy())  # Crear una nueva instancia de Compra con los items actuales del carrito
        compras.append(compra)
        
        # Guardar la compra en el archivo XML
        if not os.path.exists('database'):
            os.makedirs('database')
        
        if os.path.exists('database/compras.xml'):
            tree = ET.parse('database/compras.xml')
            root = tree.getroot()
        else:
            root = ET.Element('compras')
            tree = ET.ElementTree(root)
       
        # Determinar el próximo número de compra
        compras_existentes = precargaCompras()
        next_compra_numero = len(compras_existentes) + 1
        
        # Crear el elemento <compra> con el atributo numero
        compra_elem = ET.SubElement(root, 'compra', numero=str(next_compra_numero))
        
        # Agregar el elemento <Total> con el total de la compra
        ET.SubElement(compra_elem, 'Total').text = str(total_compra)
        
        # Agregar cada item del carrito como <item> dentro de <compra>
        for item in carrito:
            item_elem = ET.SubElement(compra_elem, 'item', id=item['id'])
            ET.SubElement(item_elem, 'nombre').text = item['nombre']
            ET.SubElement(item_elem, 'total').text = str(item['Total'])
            ET.SubElement(item_elem, 'cantidad').text = str(item['cantidad'])
            ET.SubElement(item_elem, 'imagen').text = item['imagen']
        
        # Guardar el árbol XML en el archivo
        ET.indent(root, space='\t', level=1)
        tree.write('database/compras.xml', encoding='utf-8', xml_declaration=True)
        
        # Vaciar el carrito
        carrito.clear()
        
        return jsonify({
            'message': 'Compra confirmada y carrito vaciado',
            'status': 200
        }), 200

    except Exception as e:
        return jsonify({
            'message': f'Error al confirmar la compra: {str(e)}',
            'status': 404
        }), 404

#verc comprax json
@BlueprintCompra.route('/compras/verCompras', methods=['GET'])
def verCompras():
    try:
        compras = precargaCompras()
        diccionario_salida = {
            'message': 'Compras encontradas',
            'compras': [],
            'status': 200
        }
        
        for compra in compras:
            diccionario_salida['compras'].append({
                'numero': compra['numero'],
                'total_compra': compra['total_compra'],
                'productos': compra['productos']
            })
        
        return jsonify(diccionario_salida), 200

    except Exception as e:
        return jsonify({
            'message': f'Error al mostrar las compras: {str(e)}',
            'status': 404
        }), 404






    
def precargaProducto():
    try:
     produc= []
     if os.path.exists('database/productos.xml'):
        tree = ET.parse('database/productos.xml')
        root = tree.getroot()
        for producto in root.findall('producto'):
            id = producto.get('id')
            nombre = producto.find('nombre').text
            precio = producto.find('precio').text
            descripcion = producto.find('descripcion').text
            categoria = producto.find('categoria').text
            cantidad = producto.find('cantidad').text
            imagen = producto.find('imagen').text

            
            produc.append({'id': id, 'nombre': nombre, 'precio': float(precio), 'descripcion': descripcion, 'categoria': categoria, 'cantidad': int(cantidad), 'imagen': imagen})
     return produc
    except Exception as e:
        print(f"Error al precargar los productos: {str(e)}")
        return []
#vercomprasxml
@BlueprintCompra.route('/compras/verComprasXML', methods=['GET'])
def verComprasXML():
    try:
        if not os.path.exists('database/compras.xml'):
            return jsonify({
                'message': 'No hay compras registradas',
                'status': 404
            }), 404
        
        with open('database/compras.xml', 'r', encoding='utf-8') as f:
            xml_content = f.read()
        
        return jsonify({
            'message': 'Archivo XML de compras',
            'xml_content': xml_content,
            'status': 200
        }), 200

    except Exception as e:
        return jsonify({
            'message': f'Error al mostrar el archivo XML de compras: {str(e)}',
            'status': 404
        }), 404
    

def precargaCompras():
    try:
        compras_list = []
        if os.path.exists('database/compras.xml'):
            tree = ET.parse('database/compras.xml')
            root = tree.getroot()
            
            for compra_elem in root.findall('compra'):
                numero = compra_elem.get('numero')
                total_compra = float(compra_elem.find('Total').text)
                productos = []
                
                for item_elem in compra_elem.findall('item'):
                    id = item_elem.get('id')
                    nombre = item_elem.find('nombre').text
                    total = float(item_elem.find('total').text)
                    cantidad = int(item_elem.find('cantidad').text)
                    imagen = item_elem.find('imagen').text
                    
                    productos.append({
                        'id': id,
                        'nombre': nombre,
                        'total': total,
                        'cantidad': cantidad,
                        'imagen': imagen
                    })
                
                compras_list.append({
                    'numero': numero,
                    'total_compra': total_compra,
                    'productos': productos
                })
        
        return compras_list
    
    except Exception as e:
        print(f"Error al precargar las compras: {str(e)}")
        return []

def precargarAlquiler():
    alquileres = []
    if os.path.exists('database/compraaas.xml'):
        tree = ET.parse('database/compraaas.xml')
        root = tree.getroot()
        for alquiler in root:
            id_alquiler = alquiler.attrib['numero']
            id_user = ''
            productos = []
            for elemento in alquiler:
                if elemento.tag == 'usuario':
                    id_user = elemento.attrib['id']
                if elemento.tag == 'productos':
                    for producto in elemento:
                        productos.append(Carro(producto.attrib['id'], producto.find('cantidad').text))
            nuevo = Buy(id_alquiler, id_user, productos)
            alquileres.append(nuevo)
    return alquileres

@BlueprintCompra.route('/comprar/agregar', methods=['POST'])
def agregarAlquiler():
    try:
        alquileres = precargarAlquiler()
        id_user = request.json['id_user']
        id_alquiler = len(alquileres) + 1
        nuevo = Buy(id_alquiler, id_user, carro.copy())
        alquileres.append(nuevo)

        if os.path.exists('database/compraaas.xml'):
            tree = ET.parse('database/compraaas.xml')
            root = tree.getroot()
        else:
            root = ET.Element('compras')
            tree = ET.ElementTree(root)

        nuevo_alquiler = ET.SubElement(root, 'compra', numero=str(id_alquiler))
        usuario = getUsuario(id_user)
        user = ET.SubElement(nuevo_alquiler, 'usuario', id=str(id_user))
        user.text = usuario.nombre

        productos = ET.SubElement(nuevo_alquiler, 'productos')
        for car in carro:
            producto = getproducto(car.idproducto)
            productoxml = ET.SubElement(productos, 'producto', id=str(producto.id))
            titulo = ET.SubElement(productoxml, 'nombre')
            titulo.text = producto.nombre
            cantidad = ET.SubElement(productoxml, 'cantidad')
            cantidad.text = str(car.cantidad)

        ET.indent(tree, space='\t', level=0)
        tree.write('database/compraaas.xml', encoding='utf-8', xml_declaration=True)

        carro.clear()
        return jsonify({
            'message': 'Producto agregado al alquiler',
            'status': 200
        }), 200

    except Exception as e:
        return jsonify({
            'message': f'Error al agregar al alquiler: {str(e)}',
            'status': 500
        }), 500

@BlueprintCompra.route('/comprar/ver', methods=['GET'])
def verAlquiler():
    try:
        with open('database/compraaas.xml', 'r', encoding='utf-8') as file:
            xml_salida = file.read()
        return xml_salida, 200, {'Content-Type': 'application/xml'}
    except Exception as e:
        return jsonify({
            'message': f'Error al ver el alquiler: {str(e)}',
            'status': 500
        }), 500



           
           
           
   

