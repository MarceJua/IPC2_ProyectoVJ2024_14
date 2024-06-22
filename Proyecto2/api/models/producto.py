class Producto:
   def __init__(self,id,precio,nombre,descripcion,categoria,cantidad, imagen) -> None:
        self.id=id
        self.nombre=nombre
        self.precio=precio
        self.descripcion=descripcion
        self.categoria=categoria
        self.cantidad=cantidad
        self.imagen=imagen
   def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'descripcion': self.descripcion,
            'categoria': self.categoria,
            'cantidad': self.cantidad,
            'imagen': self.imagen
        }