from usuario import Usuario

class Manager():
    def __init__(self):
        self.usuarios = []

    def add_usuario(self, id, password, nombre, edad, email, telefono):
        nuevo = Usuario(id, password, nombre, edad, email, telefono)
        self.usuarios.append(nuevo)
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