class ListaCabecera:
    def __init__(self, tipo):
        self.tipo = tipo
        self.primero = None
        self.ultimo = None
        self.tamanio = 0

    def __len__(self):
        return self.tamanio
    
    def insertarNodoCabecera(self, nuevo):
        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            if nuevo.id < self.primero.id:
                nuevo.siguiente = self.primero
                self.primero.anterior = nuevo
                self.primero = nuevo
            elif nuevo.id > self.ultimo.id:
                self.ultimo.siguiente = nuevo
                nuevo.anterior = self.ultimo
                self.ultimo = nuevo
            else:
                actual = self.primero
                while actual is not None:
                    if nuevo.id < actual.id:
                        nuevo.siguiente = actual
                        nuevo.anterior = actual.anterior
                        actual.anterior.siguiente = nuevo
                        actual.anterior = nuevo
                        break
                    elif nuevo.id > actual.id:
                        actual = actual.siguiente
                    else:
                        break
        self.tamanio += 1

    def obtenerCabecera(self, id):
        actual = self.primero
        while actual is not None:
            if actual.id == id:
                return actual
            actual = actual.siguiente
        return None
    
    def mostrarCabeceras(self):
        actual = self.primero
        while actual is not None:
            print(actual.id)
            actual = actual.siguiente