import os
import xml.etree.ElementTree as ET
from flask import Blueprint, jsonify,   request
from controllers.estructuras import carrito, compras
from models.compras import Compra



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

        compra_elem = ET.SubElement(root, 'compra')
        for item in carrito:
            item_elem = ET.SubElement(compra_elem, 'item', id=item['id'])
            ET.SubElement(item_elem, 'nombre').text = item['nombre']
            ET.SubElement(item_elem, 'total').text = str(item['Total'])
            ET.SubElement(item_elem, 'cantidad').text = str(item['cantidad'])
            ET.SubElement(item_elem, 'imagen').text = item['imagen']

        ET.indent(root, space='\t', level=0)
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

def precargaCompras():
    try:
        compras = []
        if os.path.exists('database/compras.xml'):
            tree = ET.parse('database/compras.xml')
            root = tree.getroot()
            for compra_elem in root.findall('compra'):
                items = []
                for item_elem in compra_elem.findall('item'):
                    id = item_elem.get('id')
                    nombre = item_elem.find('nombre').text
                    precio = float(item_elem.find('total').text)
                    cantidad = int(item_elem.find('cantidad').text)
                    imagen = item_elem.find('imagen').text
                    items.append({
                        'id': id,
                        'nombre': nombre,
                        'total': precio,
                        'cantidad': cantidad,
                        'imagen': imagen
                    })
                compra = Compra(items=items)
                compras.append(compra)
        return compras
    except Exception as e:
        print(f"Error al precargar las compras: {str(e)}")
        return []

            
           
           
           
   

