class nodoUsuarios:
    def __init__(self,id,password,nombre,edad,email,telefono):
        self.id=id
        self.password=password
        self.nombre=nombre
        self.edad=edad
        self.email=email
        self.telefono=telefono
        self.siguiente=None
        self.anterior=None

class listaDoble:
    def __init__(self) :
        self.cabeza=None
        self.ultimo=None
        self.size=0
        
    def __len__(self):
        return self.size
    
    def agregarUsuario(self,id,password,nombre,edad,email,telefono):
        nuevoNodo=nodoUsuarios(id,password,nombre,edad,email,telefono)
        #verificar si esta vacia
        if self.cabeza==None and self.ultimo==None:
            self.cabeza=nuevoNodo
            self.ultimo=nuevoNodo
        else:
            self.ultimo.siguiente=nuevoNodo
            nuevoNodo.anterior=self.ultimo
            self.ultimo=nuevoNodo
        self.size+=1
        '''
self.ultimo.siguiente = nuevoNodo:
Se establece el siguiente del nodo actualmente último (self.ultimo) para que apunte a nuevoNodo.
Esto enlaza el nodo actualmente último con el nuevo nodo como su sucesor.

nuevoNodo.anterior = self.ultimo:
Se establece el anterior de nuevoNodo para que apunte al nodo que actualmente es el último (self.ultimo).
Esto enlaza el nuevo nodo con el nodo actualmente último como su predecesor.

self.ultimo = nuevoNodo:
Se actualiza self.ultimo para que apunte a nuevoNodo, que ahora es el último nodo de la lista.
Esto asegura que las futuras operaciones de agregar nodos se realizarán a partir de este nuevo último nodo.
        '''
    def imprimirlista_desdeinicio(self):
        actual = self.cabeza
        while actual != None:
            print(f"{actual.id} password: {actual.password} nombre {actual.nombre}")
            actual = actual.siguiente