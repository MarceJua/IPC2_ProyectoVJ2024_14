from controllers.productocontroller import getproducto
from flask import Blueprint, jsonify, request
from models.carro import Carro

BlueprintCarro = Blueprint('carro', __name__)
carrito = []
@BlueprintCarro.route('/carro/agregar', methods=['POST'])
def agregarcarro():
    try:
        #OBTENEMOS EL JSON
        json_entrada = request.json
        print(json_entrada)
        if json_entrada == '':
            return jsonify({
                'message': 'Error al agregar al carro: EL JSON está vacio',
                'status': 404
            }), 404
        #LEER EL JSON
        idproducto = json_entrada['idproducto']
        cantidad = json_entrada['cantidad']
        nuevo = Carro(idproducto, cantidad)
        carrito.append(nuevo)
        return jsonify({
            'message': 'Producto agregado al carro',
            'status': 200
        }), 200
    except:
        return jsonify({
            'message': 'Error al agregar al carro',
            'status': 404
        }), 404
    
@BlueprintCarro.route('/carro/ver', methods=['GET'])
def vercarro():
    try:
        contenido = '<carrito>\n'
        for car in carrito:
            producto = getproducto(car.idproducto)
            contenido += '\t<producto id="'+str(producto.id)+'">\n'
            contenido += '\t\t<nombre>'+producto.nombre+'</nombre>\n'
            contenido += '\t\t<cantidad>'+str(car.cantidad)+'</cantidad>\n'
            contenido += '\t</producto>\n'
        contenido += '</carrito>'
        return jsonify({
            'message': 'Carro',
            'status': 200,
            'contenido': contenido
        }), 200
    except:
        return jsonify({
            'message': 'Error al ver el carro',
            'status': 404
        }), 404