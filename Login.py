import tkinter as tk
from tkinter import *
from tkinter import ttk
import mysql.connector
import hashlib
import Admin_menu, Seller_menu

def start():
    start = Tk()
    start.title("Login")
    start.resizable(False, False)

    # Centrar ventana
    height = 180
    width = 330
    x_v = start.winfo_screenwidth() // 2 - width //2
    y_v = start.winfo_screenheight() // 2 - width //2
    pos = str(width)+"x"+str(height)+"+"+str(x_v)+"+"+str(y_v)
    start.geometry(pos)

    # Conexión a la base de datos
    db = mysql.connector.connect(host = 'localhost', port = 3306, user = 'root', password = '', database = 'frutilla_rosada_db')
    cursor = db.cursor()

    txt_rut_user = tk.StringVar()
    txt_password = tk.StringVar()

    ########## FUNCIONES ##########
    def hash(psw): # Creación de clave encriptada
        enc = psw.encode()
        hash = hashlib.md5(enc).hexdigest()
        return hash

    def login(): # Autentificación de usuario
        try:
            cursor.execute('select * from usuarios where rut=%s', (txt_rut_user.get(),))
            result = cursor.fetchone()

            # Eliminar Label existentes en la posición (row=4, columnspan=0)
            for widget in start.grid_slaves():
                if int(widget.grid_info()["row"]) == 4 and int(widget.grid_info()["columnspan"]) == 2:
                    widget.destroy()

            if result is not None:
                if result[2] == hash(txt_password.get()):
                    Label(start, text="Inicio exitoso", justify="center", font=font).grid(row=4, columnspan=2, pady=10)
                    if result[3] == "Administrador": # Iniciar menú del rol administrador
                        start.destroy()
                        Admin_menu.administrator_menu()
                    elif result[3] == "Vendedor": # Iniciar menú del rol vendedor
                        start.destroy()
                        Seller_menu.seller_menu()
                else:
                    Label(start, text="Contraseña incorrecta", justify="center", font=font).grid(row=4, columnspan=2, pady=10)
                    
            else:
                Label(start, text="No existe el usuario", justify="center", font=font).grid(row=4, columnspan=2, pady=10)
        except Exception as e:
            print("Error:", e)

    ########## GUI ##########
    font = "verdana, 14"

    # Labels
    Label(start, text="RUT:", anchor="w", justify="left", width=6, font=font).grid(row=1, column=0, padx=10, pady=10)
    Label(start, text="Clave:", anchor="w", justify="left", width=6, font=font).grid(row=2, column=0, padx=10, pady=10)

    # Entrys
    ttk.Entry(start, font=font, textvariable=txt_rut_user).grid(row=1,column=1,pady=10)
    ttk.Entry(start, font=font, show="*", textvariable=txt_password).grid(row=2,column=1,pady=10)

    # Button
    ttk.Button(start, text="Iniciar sesión", width=20, command=login).grid(row=3, columnspan= 2)

    # Iniciar ventana
    start.mainloop()

if __name__ == '__main__':
    start()