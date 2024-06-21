from api.models.producto import Productos
import re
class Manager():
    def __init__(self):
        self.usuarios = []
        self.productos=[]

    def add_usuario(self, id, password, nombre, edad, email, telefono):
        if not self.validarEmail(email):
            print(f"Error: El correo electrónico '{email}' no tiene un formato válido.")
            return
        # Validar el teléfono
        if not self.validarTelefono(telefono):
            print(f"Error: El número de teléfono '{telefono}' no es válido. Debe contener exactamente 8 dígitos.")
            return
        nuevo = Usuario(id, password, nombre, edad, email, telefono)
        self.usuarios.append(nuevo)
        return True
    
    def validarEmail(self, email):
        # Expresión regular para validar un correo electrónico
        patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(patron, email) is not None

    def validarTelefono(self, telefono):
        # Verifica que el teléfono tenga exactamente 8 dígitos
        return telefono.isdigit() and len(telefono) == 8
    def validarFloat(self,precio):
        return precio.isdecimal()
    def validarInt(self,cantidad):
        return cantidad.isdigit()

    
    def add_producto(self, id, precio, nombre, descripcion, categoria, cantidad, imagen):
        try:
            precio = float(precio)
        except ValueError:
            print(f"Error: El precio '{precio}' no es válido. Debe ser un número decimal.")
            return 

        try:
            cantidad = int(cantidad)
        except ValueError:
            print(f"Error: La cantidad '{cantidad}' no es válida. Debe ser un número entero.")
            return 

        nuevo = Productos(id, precio, nombre, descripcion, categoria, cantidad, imagen)
        self.productos.append(nuevo)
        return True

    
    def get_usuario(self):
        json = []
        for k in self.usuarios:
            usuario = {
                'id': k.id,
                'password': k.password,
                'nombre': k.nombre,
                'edad': k.edad,
                'email': k.email,
                'telefono': k.telefono
            }
            json.append(usuario)
        return json
    def get_productos(self):
        json=[]
        for k in self.productos:
            producto={
                'id':k.id,
                'nombre':k.nombre,
                'precio':k.precio,
                'descripcion':k.descripcion,
                'categoria': k.categoria,
                'catidad':k.cantidad,
                'imagen':k.imagen

            }
            json.append(producto)
        return json

        