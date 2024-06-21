from controllers.estructuras import pruductos, users
from controllers.productocontroller import BlueprinProducto,precargaProducto
from controllers.usercontroller import BlueprintUser, precargarUsuarios
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

#PARA PRECARGAR LA DATA
pruductos = precargaProducto()
users = precargarUsuarios()

#IMPRIMIMOS LA LONGITUD DE LAS LISTAS
print('Hay '+str(len(pruductos)) + ' productos')
print('Hay '+str(len(users)) + ' usuarios')

#REGISTRAMOS LOS BLUEPRINTS
app.register_blueprint(BlueprinProducto)
app.register_blueprint(BlueprintUser)

if __name__ == '__main__':
    app.run(host='localhost', port=4000, debug=True)