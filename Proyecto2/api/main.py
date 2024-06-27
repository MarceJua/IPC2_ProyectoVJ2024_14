#from controllers.estructuras import pruductos, users, empleados,actividades,compras
from controllers.productocontroller import BlueprinProducto,precargaProducto
from controllers.usercontroller import BlueprintUser, precargarUsuarios
from controllers.empleadoscontroller import BlueprintEmpleado, precargarEmpleados
from controllers.actividadescontroller import BlueprintActividad, precargaActividades
from controllers.comprascontroller import BlueprintCompra, precargaCompras
from controllers.carritocontroller import BlueprintCarro

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

#PARA PRECARGAR LA DATA
pruductos = precargaProducto()
users = precargarUsuarios()
empleados=precargarEmpleados()
actividades=precargaActividades()
compras=precargaCompras()

#IMPRIMIMOS LA LONGITUD DE LAS LISTAS
print('Hay '+str(len(pruductos)) + ' productos')
print('Hay '+str(len(users)) + ' usuarios')
print('Hay '+str(len(empleados)) + ' empleados')
print('Hay '+str(len(actividades)) + ' actividades')
print('Hay '+str(len(compras)) + ' compras')

#REGISTRAMOS LOS BLUEPRINTS
app.register_blueprint(BlueprinProducto)
app.register_blueprint(BlueprintUser)
app.register_blueprint(BlueprintEmpleado)
app.register_blueprint(BlueprintActividad)
app.register_blueprint(BlueprintCompra)
app.register_blueprint(BlueprintCarro)


if __name__ == '__main__':
    app.run(host='localhost', port=4000, debug=True)