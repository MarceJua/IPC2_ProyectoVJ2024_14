class  NodoCompras:
    def __init__(self,idUsuarios,nombreUsuario,NombreProductos,total) -> None:
        self.idUsuarios=idUsuarios
        self.nombreUsuario=nombreUsuario
        self.NombreProductos=NombreProductos
        self.total=total
        self.siguiente=None
        