class Productos:
     def __init__(self,id,precio,nombre,descripcion,categoria,cantidad, imagen) -> None:
        self.id=id
        self.nombre=nombre
        self.precio=precio
        self.descripcion=descripcion
        self.categoria=categoria
        self.cantidad=cantidad
        self.imagen=imagen

     def getProductos(self):
        return self
    