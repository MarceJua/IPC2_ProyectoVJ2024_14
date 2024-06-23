class Compra:
    def __init__(self, items):
        self.items = items
class Carrito:
    def __init__(self,idProducto,nombreProducto,cantidad, total):
        self.idProducto=idProducto
        self.nombreProducto=nombreProducto
        self.cantidad=cantidad
        self.total=total