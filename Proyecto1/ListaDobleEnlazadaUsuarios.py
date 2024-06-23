import re  # Importamos el módulo de expresiones regulares
import os

class nodoUsuarios:
    def __init__(self, id, password, nombre, edad, email, telefono):
        self.id = id
        self.password = password
        self.nombre = nombre
        self.edad = edad
        self.email = email
        self.telefono = telefono
        self.siguiente = None
        self.anterior = None

class listaDoble:
    def __init__(self):
        self.cabeza = None
        self.ultimo = None
        self.size = 0

    def __len__(self):
        return self.size

    def agregarUsuario(self, id, password, nombre, edad, email, telefono):
        # Validar el correo electrónico
        if not self.validarEmail(email):
            print(f"Error: El correo electrónico '{email}' no tiene un formato válido.")
            return
        
        # Validar el teléfono
        if not self.validarTelefono(telefono):
            print(f"Error: El número de teléfono '{telefono}' no es válido. Debe contener exactamente 8 dígitos.")
            return

        # Verificar si el nombre es único antes de agregar el nodo
        if self.nombreUnico(id):
            # Si el nombre es único, crea un nuevo nodo con la información del usuario
            nuevoNodo = nodoUsuarios(id, password, nombre, edad, email, telefono)
            # Verificar si está vacía
            if self.cabeza == None and self.ultimo == None:
                # Si la lista está vacía, el nuevo nodo es tanto la cabeza como el último nodo
                self.cabeza = nuevoNodo
                self.ultimo = nuevoNodo
            else:
                # Si la lista no está vacía, enlaza el nuevo nodo al final de la lista
                self.ultimo.siguiente = nuevoNodo  # El nodo actual último apunta al nuevo nodo como su siguiente
                nuevoNodo.anterior = self.ultimo  # El nuevo nodo apunta al nodo actual último como su anterior
                self.ultimo = nuevoNodo  # El nuevo nodo se convierte en el último nodo de la lista
            self.size += 1  # Incrementa el tamaño de la lista en 1
        else:
            # Si el nombre no es único, imprime un mensaje de error y no agrega el nodo
            print(f"Error: El nombre '{nombre}' ya existe en la lista. No se puede agregar.")

    def validarEmail(self, email):
        # Expresión regular para validar un correo electrónico
        patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(patron, email) is not None

    def validarTelefono(self, telefono):
        # Verifica que el teléfono tenga exactamente 8 dígitos
        return telefono.isdigit() and len(telefono) == 8

    def nombreUnico(self, id):
        # Verifica si el nombre es único en la lista
        actual = self.cabeza  # Empieza desde la cabeza de la lista
        while actual != None:
            # Recorre la lista comparando el nombre de cada nodo con el nombre proporcionado
            if actual.id == id:
                return False  # Si encuentra un nombre igual, retorna False
            actual = actual.siguiente  # Avanza al siguiente nodo
        return True  # Si no encuentra ningún nombre igual, retorna True
    
    def autenticacion(self, id, password):
        actual = self.cabeza
        while actual != None:
            if actual.id == id and actual.password == password:
                return True
            actual = actual.siguiente
        return False

    def imprimirlista_desdeinicio(self):
        # Imprime los detalles de cada nodo desde el inicio de la lista
        actual = self.cabeza  # Empieza desde la cabeza de la lista
        while actual != None:
            # Imprime la información del nodo actual
            print(f"{actual.id} password: {actual.password} nombre: {actual.nombre}")
            actual = actual.siguiente  # Avanza al siguiente nodo

    def graficar(self):
        try:
         codigo_dot = ''
         archivo = open('reportesdot/listaUsuarios.dot', 'w')
         codigo_dot +='''digraph G {
  rankdir=LR;
  node [shape = record, height = .1]\n'''
         actual = self.cabeza
         contador_nodos = 0
         #PRIMERO CREAMOS LOS NODOS
         while actual != None:
            codigo_dot += f'node{contador_nodos} [label = "{{ID: {actual.id}|password: {actual.password}|nombre: {actual.nombre}|edad: {actual.edad}|email: {actual.email}|Tel: {actual.telefono}}}"];\n'
            contador_nodos += 1
            actual = actual.siguiente

        #HACEMOS LAS RELACIONES
         actual = self.cabeza
         contador_nodos = 0
         while actual.siguiente != None:
            #RELACIONES DE IZQUIERDA A DERECHA
            codigo_dot += 'node'+str(contador_nodos)+':f2 -> node'+str(contador_nodos+1)+':f1;\n'
            #RELACIONES DE DERECHA A IZQUIERDA
            codigo_dot += 'node'+str(contador_nodos+1)+':f1 -> node'+str(contador_nodos)+':f2;\n'
            contador_nodos += 1
            actual = actual.siguiente

         codigo_dot += '}'

         archivo.write(codigo_dot)
         archivo.close()

        #GENERAMOS LA IMAGEN
         ruta_dot = 'reportesdot/listaUsuarios.dot'
         ruta_imagen = 'reportes/listaUsuarios.png'
         comando = 'dot -Tpng '+ruta_dot+' -o '+ruta_imagen
         os.system(comando)
      

        #ABRIR LA IMAGEN
        #convierte la ruta a una ruta válida para windows
         ruta_reporte = os.path.abspath(ruta_imagen)
         os.startfile(ruta_reporte)
        except:
            print("Vacio")

    def NombrePorId(self, id):
        nodo = self.buscarPorId(id)
        if nodo:
            return nodo.nombre
        return None
    
    def buscarPorId(self, id):
        if self.cabeza is None:
            return None
        actual = self.cabeza
        while True:
            if actual.id == id:
                return actual
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        return None

