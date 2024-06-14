class NodoCelda:
    def __init__(self, id, nombre, descripcion, empleado, dia, hora):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.empleado = empleado
        self.dia = dia
        self.hora = hora
        self.arriba = None
        self.abajo = None
        self.izquierda = None
        self.derecha = None