from flask import Flask, request
from flask.json import jsonify
from manage import Manager
from xml.etree import ElementTree as ET

app = Flask(__name__)

manager = Manager()


@app.route('/') #Endpoint
def index():
    return "API python Hola Mundo!!! lkadlaskd"

@app.route('/add', methods=['POST'])
def add_usuarios():
    xml = request.data.decode('utf-8')
    raiz = ET.XML(xml)
    for elemento in raiz:
        id = elemento.attrib['id']
        password = elemento.attrib['password']
        nombre = elemento.find('nombre').text
        edad = int(elemento.find('edad').text)
        email = elemento.find('email').text
        telefono = elemento.find('telefono').text
        manager.add_usuario(id, password, nombre, edad, email, telefono)
    return jsonify({'msg': 'Archivo XML cargado satisfactoriamente'}), 200

@app.route('/showall', methods=['GET'])
def get_usuarios():
    c = manager.get_usuario()
    return jsonify(c), 200

@app.route('/cargaproductos',methods=['POST'])
def addProductos():
    xml=request.data.decode('utf-8')
    raiz=ET.XML(xml)
    for elemento in raiz:
        id=elemento.attrib["id"]
        nombre=elemento.find('nombre').text
        precio=elemento.find('precio').text
        descripcion=elemento.find('descripcion').text
        categoria=elemento.find('categoria').text
        cantidad=elemento.find('cantidad').text
        imagen=elemento.find('imagen').text
        manager.add_producto(id,precio, nombre,descripcion,categoria,cantidad,imagen)
    return jsonify({'msg': 'Archivo XML cargado satisfactoriamente'}), 200

@app.route('/showallproduct', methods=['GET'])
def get_productos():
    c = manager.get_productos()
    return jsonify(c), 200



if __name__=='__main__':
    app.run(debug=True, port=4000) #debug=True <- sirve para no estar reiniciando la api