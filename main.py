import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext as st
from tkinter import ttk
import xml.etree.ElementTree as ET

import sys
from tkinter import filedialog 
from PIL import Image, ImageTk #pip install pillow en la consola 


class applicacion:
    def __init__(self, root) :
        self.root=root
        self.root.title("IPC2 MARKET")
        self.root.geometry("300x200")
    
        self.create_widgets()
    
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
  
        else:
            messagebox.showerror(title="error",message="DATOS INCORRECTOS")
            self.crear_ventanaUsuario()#solo para probar la interfaz

    
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
        self.file_report.add_command(label="Reporte de Usuarios")
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


    #''''''''''''
    def cargar_archivo(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo XML",
            filetypes=[("Archivos XML", "*.xml")]
        )

        if file_path:
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
                print(f"Archivo XML cargado correctamente desde: {file_path}")
                print(f"Elemento raíz: {root.tag}")
                # Puedes guardar file_path para usarlo más adelante si lo deseas
                self.archivo_path = file_path
            except ET.ParseError as e:
                print(f"Error al parsear el archivo XML: {e}")
        else:
            print("No se seleccionó ningún archivo.")
     
    
    #  ''''''''''   
    
    def crear_ventanaActividades(self):
        
        self.venA=tk.Toplevel(self.root)
        self.venA.title("Ventana Administrador")
        self.venA.geometry("550x450")
        self.label_tituloAct=tk.Label(self.venA,text="ACTIVIDADES DE HOY",font=("Roboto Cn",14))
        self.label_tituloAct.pack(pady=5)
        self.actividades_text=st.ScrolledText(self.venA,height=15,width=50)
        self.actividades_text.pack(pady=5)

    def crear_ventanaUsuario(self):
        self.root.withdraw()
        self.ventUser = tk.Toplevel(self.root)
        self.ventUser.title("IPC MARKET- USUARIO")
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
    
    
