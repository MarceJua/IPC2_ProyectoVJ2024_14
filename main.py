import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext as st

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
        self.file_menu.add_command(label="Cargar Usuarios")
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
    
    def crear_ventanaActividades(self):
        
        self.venA=tk.Toplevel(self.root)
        self.venA.title("Ventana Administrador")
        self.venA.geometry("550x450")
        self.label_tituloAct=tk.Label(self.venA,text="ACTIVIDADES DE HOY",font=("Roboto Cn",14))
        self.label_tituloAct.pack(pady=5)
        self.actividades_text=st.ScrolledText(self.venA,height=15,width=50)
        self.actividades_text.pack(pady=5)
    


        


        



      
        


    def regresarLogin(self):
        # Cerrar la ventana principal
        self.top.destroy()
        self.entry_user.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        
        # Mostrar la ventana de login
        self.root.deiconify()

if __name__=="__main__":
    root=tk.Tk()
    app=applicacion(root)
    root.mainloop()
    
    
