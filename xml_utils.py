import xml.etree.ElementTree as ET
class XMLHandler:
    def __init__(self, file_path): 
        self.file_path = file_path
        self.root = None
    
    def read_xml(self): #Lee el archivo XML y 
                        #llama al método _parse_root() para analizar el elemento raíz.
        try:
            tree = ET.parse(self.file_path) # Parsea el archivo XML
            self.root = tree.getroot() # Obtiene el elemento raíz del árbol XML
            #self._parse_root(root)
        except FileNotFoundError:
            print("El archivo XML no se encontró.")
        except ET.ParseError:
            print("Error al analizar el archivo XML.")

    def _parse_root(self, root): # Comprueba la etiqueta del elemento raíz y llama al método correspondiente
        if root.tag == 'actividades':
            self._parse_actividades(root)
        elif root.tag == 'productos':
            self._parse_productos(root)
        elif root.tag == 'usuarios':
            self._parse_usuarios(root)
        elif root.tag == 'empleados':
            self._parse_vendedor(root)

    def _parse_actividades(self, root):
        for actividad in root.findall('actividad'): # Obtiene el atributo 'id' del elemento 'actividad'
            id = actividad.get('id')
            nombre = ''
            descripcion = ''
            empleado = ''
            dia = ''
            hora = ''
            for child in actividad:  # Itera sobre los elementos hijos de 'actividad'
                # Comprueba la etiqueta de cada elemento hijo y asigna el texto correspondiente
                if child.tag == 'nombre':
                    nombre = child.text
                elif child.tag == 'descripcion':
                    descripcion = child.text
                elif child.tag == 'empleado':
                    empleado = child.text
                elif child.tag == 'dia':
                    dia = child.text
                    hora = child.get('hora')
            # Imprime la información de la actividad
            print(f'ID: {id}\n' 
                  f'Nombre: {nombre}\n'
                  f'Descripción: {descripcion}\n'
                  f'Empleado: {empleado}\n'
                  f'Día: {dia}\n'
                  f'Hora: {hora}\n')

    def _parse_productos(self, root):
        for producto in root.findall('producto'):
            id = producto.get('id')
            nombre = ''
            precio = ''
            descripcion = ''
            categoria = ''
            cantidad = ''
            imagen = ''
            for child in producto:
                if child.tag == 'nombre':
                    nombre = child.text
                elif child.tag == 'precio':
                    precio = child.text
                elif child.tag == 'descripcion':
                    descripcion = child.text
                elif child.tag == 'categoria':
                    categoria = child.text
                elif child.tag == 'cantidad':
                    cantidad = child.text
                elif child.tag == 'imagen':
                    imagen = child.text
            print(f'ID: {id}\n'
                  f'Nombre: {nombre}\n'
                  f'Precio: {precio}\n'
                  f'Descripción: {descripcion}\n'
                  f'Categoría: {categoria}\n'
                  f'Cantidad: {cantidad}\n'
                  f'Imagen: {imagen}\n')

    def _parse_usuarios(self, root):
        for usuario in root.findall('usuario'):
            id = usuario.get('id')
            password = usuario.get('password')
            nombre = ''
            edad = ''
            email = ''
            telefono = ''
            for child in usuario:
                if child.tag == 'nombre':
                    nombre = child.text
                elif child.tag == 'edad':
                    edad = child.text
                elif child.tag == 'email':
                    email = child.text
                elif child.tag == 'telefono':
                    telefono = child.text
            print(f'ID: {id}\n'
                  f'Password: {password}\n'
                  f'Nombre: {nombre}\n'
                  f'Edad: {edad}\n'
                  f'Email: {email}\n'
                  f'Teléfono: {telefono}\n')

    def _parse_vendedor(self, root):
        for empleado in root.findall('empleado'):
            codigo = empleado.get('codigo')
            nombre = ''
            puesto = ''
            for child in empleado:
                if child.tag == 'nombre':
                    nombre = child.text
                elif child.tag == 'puesto':
                    puesto = child.text
            print(f'Código: {codigo}\n'
                  f'Nombre: {nombre}\n'
                  f'Puesto: {puesto}\n')

def leer_xml_elementtree(ruta):
    # Crea una instancia de la clase XMLHandler con la ruta proporcionada
    xml_handler = XMLHandler(ruta)
    # Llama al método read_xml() para leer y analizar el archivo XML
    xml_handler.read_xml()