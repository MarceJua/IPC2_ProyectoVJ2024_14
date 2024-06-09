import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext as st
from tkinter import ttk
# import xml.etree.ElementTree as ET
from ListaDobleEnlazadaUsuarios import listaDoble
from xml_utils import XMLHandler

import sys
from tkinter import filedialog 
from PIL import Image, ImageTk #pip install pillow en la consola 


class applicacion:
    def __init__(self, root) :
        self.root=root
        self.root.title("IPC2 MARKET")
        self.root.geometry("300x200")
        self.create_widgets()
        self.listaDobleUsarios=listaDoble()
        
    
    def create_widgets(self):
        # Crear etiquetas y entradas

        self.label_tittle=tk.Label(self.root,text="IPC2 MARKET",font=("Roboto Cn",14))
        self.label_tittle.pack(pady=5)
        self.label_user = tk.Label(self.root, text="Usuario:")
        self.label_user.pack(pady=5)
        
        self.entry_user = tk.Entry(self.root)
        self.entry_user.pack(pady=5)
        
        self.label_password = tk.Label(self.root, text="Contraseña:")
        self.label_password.pack(pady=5)
        
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack(pady=5)
        
        # Botón de login
        self.button_login = tk.Button(self.root, text="Login",command=self.verifUsuarios)
        self.button_login.pack(pady=10)
    
    def verifUsuarios(self):
        #obtener valores de los textbox
        user=self.entry_user.get()
        password=self.entry_password.get()
        #aqui va la logica de inicio de sesion entre admin y usuarios por el momento solo 
        #verificare el admin
        if user=="AdminIPC2" and password=="IPC2VJ2024":
            messagebox.showinfo(title="Exito", message="Bienvenido Administrador")
            self.crear_ventanaAdmin()
        # verificar el usuario
        elif self.listaDobleUsarios.autenticacion(user, password):
            messagebox.showinfo(title="Exito", message=f"Bienvenido, {user}")
            self.crear_ventanaUsuario(user) # Pasar el ID del usuario como parámetro
        else:
            messagebox.showerror(title="error", message="DATOS INCORRECTOS")
            

    
    def crear_ventanaAdmin(self):
        self.root.withdraw()
        self.top = tk.Toplevel(self.root)
        self.top.title("Ventana Administrador")
        self.top.geometry("550x450")

           # Crear un contenedor para el menú y el botón
        self.menu_frame = tk.Frame(self.top)
        self.menu_frame.pack(fill=tk.X)
        
        # Crear un botón para cerrar sesión
        self.button_back = tk.Button(self.menu_frame, text="Cerrar Sesion", command=self.regresarLogin)
        self.button_back.pack(side=tk.RIGHT, padx=5, pady=5)
        self.button_Actividades=tk.Button(self.menu_frame,text="Ver Actividades de Hoy",command=self.crear_ventanaActividades)
        self.button_Actividades.pack(side=tk.RIGHT,padx=5,pady=15)
        


        #crar menu cascada
        self.menu_bar = tk.Menu(self.top)
        self.top.config(menu=self.menu_bar)
        #Crear menu archivo
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Cargar", menu=self.file_menu)
        self.file_menu.add_command(label="Cargar Usuarios",command=self.cargar_archivo)
        self.file_menu.add_command(label="Cargar Productos")
        self.file_menu.add_command(label="Cargar empleados")
        self.file_menu.add_command(label="Cargar actividades",)
        #crear menu reportes
        self.file_report=tk.Menu(self.menu_bar,tearoff=0)
        self.menu_bar.add_cascade(label="Reportes",menu=self.file_report)
        self.file_report.add_command(label="Reporte de Usuarios",command=self.listaDobleUsarios.graficar)
        self.file_report.add_command(label="Reporte Productos")
        self.file_report.add_separator()
        self.file_report.add_command(label="Reporte cola")
        self.file_report.add_command(label="reporte Compras")

        self.label_tittle=tk.Label(self.top,text="AUTORIZAR COMPRA",font=("Roboto Cn",14))
        self.label_tittle.pack(pady=5)


        #Cuadro de texto 
        self.autoriza_txt=st.ScrolledText(self.top,height=15,width=50)
        self.autoriza_txt.pack(padx=5,pady=10)
        #Botones
        self.button_accept=tk.Button(self.top,text="Aceptar")
        self.button_cancel=tk.Button(self.top,text="Cancelar")
        self.button_accept.pack(pady=5)
        self.button_cancel.pack(pady=5)

    """
    #''''''''''''
    #funcion para buscar el path
    def cargar_archivo(self):
        # Abrir un cuadro de diálogo para seleccionar un archivo XML
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo XML",  # Título del cuadro de diálogo
            filetypes=[("Archivos XML", "*.xml")]  # Filtrar para mostrar solo archivos XML
        )

        # Verificar si se ha seleccionado un archivo
        if file_path:
            try:
                # Intentar parsear el archivo XML
                tree = ET.parse(file_path)
                root = tree.getroot()
                
                # Imprimir la ruta del archivo y el elemento raíz del XML
                print(f"Archivo XML cargado correctamente desde: {file_path}")
                print(f"Elemento raíz: {root.tag}")
                self._parse_root(root)
            
                
                # Guardar la ruta del archivo para su uso posterior
                self.archivo_path = file_path
            except ET.ParseError as e:
                # Manejar errores de parseo del XML
                print(f"Error al parsear el archivo XML: {e}")
        else:
            # Mensaje si no se selecciona ningún archivo
            print("No se seleccionó ningún archivo.") """
    
    def cargar_archivo(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo XML",
            filetypes=[("Archivos XML", "*.xml")]
        )

        if file_path:
            xml_handler = XMLHandler(file_path) #Se hace uso de la clase XMLHandler
            xml_handler.read_xml()
            if xml_handler.root is not None:
                self._parse_root(xml_handler.root)
            else:
                print("No se pudo leer el archivo XML correctamente.")
        else:
            print("No se seleccionó ningún archivo.")

    def _parse_root(self, root): # Comprueba la etiqueta del elemento raíz y llama al método correspondiente
        if root.tag == 'actividades':
            self._parse_actividades(root)
        elif root.tag == 'productos':
            self._parse_productos(root)
        elif root.tag == 'usuarios':
            self._parse_usuarios(root)
        elif root.tag == 'empleados':
            self._parse_vendedor(root)

    def _parse_usuarios(self, root):
        print ("hola")
        pass
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
            self.listaDobleUsarios.agregarUsuario(id,password,nombre,edad,email,telefono)
        self.listaDobleUsarios.imprimirlista_desdeinicio()
            #print(f'ID: {id}\n'
                  #f'Password: {password}\n'
                  #f'Nombre: {nombre}\n'
                  #f'Edad: {edad}\n'
                  #f'Email: {email}\n'
                  #f'Teléfono: {telefono}\n')
        

    

        
    


    



    
    #==================
    
    def crear_ventanaActividades(self):
        
        self.venA=tk.Toplevel(self.root)
        self.venA.title("Ventana Administrador")
        self.venA.geometry("550x450")
        self.label_tituloAct=tk.Label(self.venA,text="ACTIVIDADES DE HOY",font=("Roboto Cn",14))
        self.label_tituloAct.pack(pady=5)
        self.actividades_text=st.ScrolledText(self.venA,height=15,width=50)
        self.actividades_text.pack(pady=5)

    def crear_ventanaUsuario(self, user):
        self.root.withdraw()
        self.ventUser = tk.Toplevel(self.root)
        self.ventUser.title(f"IPC MARKET- {user}") #Agrega el ID del usuario ingresado
        self.ventUser.geometry("550x450")

        self.dive = tk.Frame(self.ventUser)
        self.dive.pack(fill=tk.X)
        self.button_back = tk.Button(self.dive, text="Cerrar Sesion", command=self.regresarLoginUser)
        self.button_back.pack(side=tk.RIGHT, padx=5, pady=5)


           # Crear un contenedor para el menú y el botón
        self.div = tk.Frame(self.ventUser)
        self.div.pack(fill=tk.X)

        self.label_tittle=tk.Label(self.div,text="AUTORIZAR COMPRA",font=("Roboto Cn",14))
        self.label_tittle.pack(pady=10)
        #crear combobox
        self.combo = ttk.Combobox(self.div, state="readonly",values=["Producto1", "Producto2", "Producto3", "Producto4"])
        self.combo.pack(side=tk.LEFT, padx=50,pady=20)
        #crear boton ver: al darle click se desplegaran los datos en la ventana
        self.button_ver=tk.Button(self.div,text="Ver",width=30)
        self.button_ver.pack(side=tk.LEFT,padx=30,pady=20)
        self.div2 = tk.Frame(self.ventUser)
        self.div2.pack(fill=tk.X)
        # Dividir div2 en 3 columnas usando grid
        self.div2.columnconfigure(0, weight=1)
        self.div2.columnconfigure(1, weight=1)
        self.div2.columnconfigure(2, weight=1)
        
        # Crear los 3 segmentos dentro de div2
        self.label1 = tk.Label(self.div2, text="Segmento 1", bg="lightblue")
        self.label1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        #falta agregar el elemento para importar imagen 
        #labels segemeto 2
        self.label2 = tk.Label(self.div2, text="Segmento 2", bg="lightgreen")
        self.label2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        self.nombreProducto = tk.Label(self.div2, text="nombre", bg="lightgreen")
        self.nombreProducto.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.labe_precio = tk.Label(self.div2, text="0.00", bg="lightgreen")
        self.labe_precio.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        self.labe_descripcion = tk.Label(self.div2, text="Descirpcion", bg="lightgreen")
        self.labe_descripcion.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)

        self.labe_categoria = tk.Label(self.div2, text="Categoria", bg="lightgreen")
        self.labe_categoria.grid(row=4, column=1, sticky="nsew", padx=5, pady=5)
        self.labe_cantidad = tk.Label(self.div2, text="Cantidad", bg="lightgreen")
        self.labe_cantidad.grid(row=4, column=1, sticky="nsew", padx=5, pady=5)
        self.labe4 = tk.Label(self.div2, text="Cantidad a agregar:", bg="lightgreen")
        self.labe4.grid(row=5, column=1, sticky="nsew", pady=5)
        self.entry_cantidad = tk.Entry(self.div2,text="0",width=5) #falta hacer que solo agregue numeros
        self.entry_cantidad.grid(row=5, column=1, sticky="nsew", pady=5)

        
    
        self.button_agregarCarrito = tk.Button(self.div2, text="Agregar Carrito", bg="lightcoral")
        self.button_agregarCarrito.grid(row=5, column=2, sticky="nsew", padx=5, pady=5)


           # Cargar la imagen y agregarla a Segmento 1
        #image_path = "ruta/a/tu/imagen.jpg"  # Cambia esto a la ruta de tu imagen
        #image = Image.open(image_path)
        #image = image.resize((100, 100), Image.ANTIALIAS)  # Redimensionar la imagen si es necesario
        #photo = ImageTk.PhotoImage(image)

        #self.label1.config(image=photo)
        #self.label1.image = photo  # Necesario para mantener una referencia de la imagen
        self.button_verCarrito = tk.Button(self.ventUser, text="Ver Carrito")
        self.button_verCarrito.pack( padx=5, pady=5)
        self.button_confirmarCompra = tk.Button(self.ventUser, text="ConfirmarCompra",bg="lightblue")
        self.button_confirmarCompra.pack( padx=5, pady=5)
    

    def regresarLogin(self):
        # Cerrar la ventana principal
        self.top.destroy()
        self.entry_user.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        
        # Mostrar la ventana de login
        self.root.deiconify()

    def regresarLoginUser(self):
         # Cerrar la ventana principal
        self.ventUser.destroy()
        self.entry_user.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        
        # Mostrar la ventana de login
        self.root.deiconify()
    


if __name__=="__main__":
    root=tk.Tk()
    app=applicacion(root)
    root.mainloop()
    
    
