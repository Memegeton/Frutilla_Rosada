import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import datetime
import calendar
import hashlib
import Login

def administrator_menu():
    admin = Tk()
    admin.title("Menú Administrador")
    admin.resizable(False, False)

    # Centrar ventana
    height = 280
    width = 330
    x_v = admin.winfo_screenwidth() // 2 - width //2
    y_v = admin.winfo_screenheight() // 2 - width //2
    pos = str(width)+"x"+str(height)+"+"+str(x_v)+"+"+str(y_v)
    admin.geometry(pos)

    # Conexión a la base de datos
    db = mysql.connector.connect(host = 'localhost', port = 3306, user = 'root', password = '', database = 'frutilla_rosada_db')
    cursor = db.cursor()

    ########## FUNCIONES de administrator_menu ##########
    def manage_users(): # VENTANA DE GESTION DE USUARIOS
        admin.destroy()
        users = Tk()
        users.title("Gestión Usuarios")
        users.resizable(False, False)
        users.state("zoomed")

        # Variables de campo
        txt_rut = tk.StringVar()
        txt_name = tk.StringVar()
        txt_password = tk.StringVar()
        txt_validator = tk.StringVar()
        txt_rol = tk.StringVar()
        
        ########## FUNCIONES de manage_users() ##########
        def back(): # Volver al menú
            users.destroy()
            administrator_menu()

        def hash(psw): # Creación de clave encriptada
            enc = psw.encode()
            hash = hashlib.md5(enc).hexdigest()
            return hash

        def fill_table(): # Llenar la tabla con los datos de usuarios
            table.delete(*table.get_children())
            cursor.execute('select rut, nombre, rol from usuarios')
            result = cursor.fetchall()
            for row in result:
                r = list(row)
                r.pop(0)
                r = tuple(r)
                table.insert("", END, text=id, values=row)

        def clear(): # Limpiar campos de ingreso
            txt_rut.set("")
            txt_name.set("")
            txt_password.set("")
            txt_validator.set("")
            txt_rol.set("")

        def save_user(): # Guardar usuario
            rut = txt_rut.get().title()
            name = txt_name.get().title()
            password = hash(txt_password.get())
            validator = hash(txt_validator.get())
            rol = txt_rol.get().title()

            try:
                if rut !="" and name !="" and password !="" and validator !="" and rol !="":
                    if password == validator:
                        cursor.execute('insert into usuarios values (%s, %s, %s, %s)', (rut, name, password, rol))
                        db.commit()
                        fill_table()
                        clear()
                        messagebox.showinfo("OK","El {} {} ha sido ingresado correctamente".format(rol, name))
                    else:
                        messagebox.showerror("Error", "Las claves no coinciden")
                else:
                    messagebox.showerror("Error", "Llene todos los campos")
            except:
                messagebox.showerror("Error", "Ya existe un usuario con este rut")
                txt_rut.set("")
                e_rut.focus() 

        def search_user(): # Buscar usuario
            if txt_rut.get() !="":
                try:
                    cursor.execute('select * from usuarios where rut=%s', (txt_rut.get(),))
                    result = cursor.fetchone()
                    txt_rut.set(result[0])
                    txt_name.set(result[1])
                    txt_rol.set(result[3])
                except:
                    messagebox.showerror("Error", "No existe el usuario")
                    clear()
                    e_rut.focus()
            else:
                messagebox.showerror("Error", "Ingrese un rut")
                clear()
                e_rut.focus()

        def update_user(): # Modificar usuario
            rut = txt_rut.get().title()
            name = txt_name.get().title()
            password = hash(txt_password.get())
            validator = hash(txt_validator.get())
            rol = txt_rol.get().title()

            try:
                if rut !="" and name !="" and txt_password.get() !="" and txt_validator.get() !="" and rol !="":
                    if password == validator:
                        cursor.execute('update usuarios set nombre=%s, hash_clave=%s, rol=%s where rut=%s', (name, password, rol, rut))
                        db.commit()
                        rows_affected = cursor.rowcount
                        fill_table()
                        clear()
                        if rows_affected > 0:
                            messagebox.showinfo("OK", "El usuario {} ha sido actualizado correctamente".format(name))
                        else:
                            messagebox.showwarning("Advertencia", "El usuario no existe o se cambio el rut")
                    else:
                        messagebox.showerror("Error", "Las claves no coinciden")
                else:
                    messagebox.showerror("Error", "Llene todos los campos")
            except mysql.connector.Error as error:
                print(f"Error: {error}")

        def delete_user(): # Eliminar usuario
            search_user()
            if txt_rut.get() !="":
                query = messagebox.askquestion("Confirmar", "Realmente desea eliminar a {}" .format(txt_name.get()))
                if query == "yes":
                    cursor.execute('delete from usuarios where rut=%s', (txt_rut.get(),))
                    db.commit()
                    fill_table()
                    clear()
                    messagebox.showinfo("OK", "Usuario eliminado")
                else:
                    clear()

        ########## GUI de manage_users() ##########
        # Labels
        Label(users, text="RUT:", anchor="w", justify="left", width=7, font=font).grid(row=0, column=0, pady=20)
        Label(users, text="Nombre:", anchor="w", justify="left", width=7, font=font).grid(row=1, column=0, pady=5)
        Label(users, text="Clave:", anchor="w", justify="left", width=7, font=font).grid(row=2, column=0, pady=5)
        Label(users, text="Valide:", anchor="w", justify="left", width=7, font=font).grid(row=3, column=0, pady=5)
        Label(users, text="Rol:", anchor="w", justify="left", width=7, font=font).grid(row=4, column=0, pady=5)

        # Entrys
        roles = ["Administrador", "Vendedor"]

        e_rut = ttk.Entry(users, font=font, textvariable=txt_rut)
        e_rut.grid(row=0, column=1, pady=5)

        e_name = ttk.Entry(users, font=font, textvariable=txt_name)
        e_name.grid(row=1, column=1, pady=5)

        e_password = ttk.Entry(users, font=font, textvariable=txt_password, show="*")
        e_password.grid(row=2, column=1, pady=5)

        e_validator = ttk.Entry(users, font=font, textvariable=txt_validator, show="*")
        e_validator.grid(row=3, column=1, pady=5)

        e_rol = ttk.Combobox(users, textvariable=txt_rol, values=roles, font="verdana, 19")
        e_rol.grid(row=4, column=1, pady=5)

        # Buttons
        ttk.Button(users, text="Buscar", command=search_user, width=20).place(x=440, y=27)
        ttk.Button(users, text="Agregar", command=save_user, width=20).grid(row=5, column=0, pady=10)
        ttk.Button(users, text="Actualizar", command=update_user, width=20).grid(row=5, column=1, pady=10)
        ttk.Button(users, text="Eliminar", command=delete_user, width=20).grid(row=5, column=2, pady=10)

        ttk.Button(users, text="Volver", command=back, width=20).grid(row=6, column=1, pady=10)

        # Tabla de usuarios
        Label(users, text="Lista de Usuarios", font="verdana, 24").place(x=830, y=5)
        table = ttk.Treeview(users)
        table.place(x=700, y=50)
        # Configuración de columnas
        table["columns"] = ("RUT", "NOMBRE", "ROL")
        table.column("#0", width=0, stretch=NO)
        table.column("RUT", width=150, anchor=CENTER)
        table.column("NOMBRE", width=200, anchor=CENTER)
        table.column("ROL", width=150, anchor=CENTER)
        table.heading("#0", text="")
        table.heading("RUT", text="Rut")
        table.heading("NOMBRE", text="Nombre")
        table.heading("ROL", text="Rol")

        # Llenado de la tabla de usuarios
        fill_table()
        # Iniciar ventana de gestión de usuarios
        users.mainloop()
        ########## FIN MANAGE_USERS ##########

    def manage_clients(): # VENTANA DE GESTIÓN DE CLIENTES
        admin.destroy()
        clients = Tk()
        clients.title("Gestión Clientes")
        clients.resizable(False, False)
        clients.state("zoomed")

        # Variables de campos
        txt_rut = tk.StringVar()
        txt_name = tk.StringVar()
        txt_lastname = tk.StringVar()
        txt_region = tk.StringVar()
        txt_city = tk.StringVar()
        txt_street = tk.StringVar()
        txt_phone = tk.StringVar()
        txt_shipment = tk.StringVar()

        ########## FUNCIONES de manage_clients() ##########
        def back(): # Volver al menú
            clients.destroy()
            administrator_menu()
        
        def fill_table(): # Llenar la tabla con los datos de clientes
            table.delete(*table.get_children())
            cursor.execute('select * from clientes')
            result = cursor.fetchall()
            for row in result:
                r = list(row)
                r.pop(0)
                r = tuple(r)
                table.insert("", END, text=id, values=row)

        def clear(): # Limpiar los entrys
            txt_rut.set("")
            txt_name.set("")
            txt_lastname.set("")
            txt_region.set("")
            txt_city.set("")
            txt_street.set("")
            txt_phone.set("")
            txt_shipment.set("")

        def save_client(): # Guardar cliente
            rut = txt_rut.get().title()
            name = txt_name.get().title()
            lastname = txt_lastname.get().title()
            region = txt_region.get().title()
            city = txt_city.get().title()
            street = txt_street.get().title()
            phone = txt_phone.get()
            shipment = txt_shipment.get().title()

            try:
                if rut !="" and name !="" and lastname !="" and region !="" and city !="" and phone !="" and shipment !="":
                    if txt_phone.get().isnumeric():
                        cursor.execute('insert into clientes values (%s, %s, %s, %s, %s, %s, %s, %s)', (rut, name, lastname, region, city, street, phone, shipment))
                        db.commit()
                        fill_table()
                        clear()
                        messagebox.showinfo("OK","El cliente {} ha sido ingresado correctamente".format(name))
                    else:
                        messagebox.showerror("Error", "El teléfono solo debe tener números")
                        txt_phone.set("")
                        e_phone.focus()
                else:
                    messagebox.showerror("Error", "Llene todos los campos")
            except:
                messagebox.showerror("Error", "Ya existe un cliente con este rut")
                txt_rut.set("")
                e_rut.focus()   
                
        def search_client(): # Buscar cliente
            if txt_rut.get() !="":
                try:
                    cursor.execute('select * from clientes where rut_cliente=%s', (txt_rut.get(),))
                    result = cursor.fetchone()
                    txt_rut.set(result[0])
                    txt_name.set(result[1])
                    txt_lastname.set(result[2])
                    txt_region.set(result[3])
                    txt_city.set(result[4])
                    txt_street.set(result[5])
                    txt_phone.set(result[6])
                    txt_shipment.set(result[7])
                except:
                    messagebox.showerror("Error", "No existe el usuario")
                    clear()
                    e_rut.focus()
            else:
                messagebox.showerror("Error", "Ingrese un rut")
                clear()
                e_rut.focus()

        def update_client(): # Actualizar cliente
            rut = txt_rut.get().title()
            name = txt_name.get().title()
            lastname = txt_lastname.get().title()
            region = txt_region.get().title()
            city = txt_city.get().title()
            street = txt_street.get().title()
            phone = txt_phone.get()
            shipment = txt_shipment.get().title()

            try:
                if rut !="" and name !="" and lastname !="" and region !="" and city !="" and phone !="" and shipment !="":
                    if txt_phone.get().isnumeric():
                        cursor.execute('update clientes set nombre=%s, apellido=%s, region=%s, ciudad=%s, calle=%s, telefono=%s, tipo_envio=%s where rut_cliente=%s', (name, lastname, region, city, street, phone, shipment, rut))
                        db.commit()
                        rows_affected = cursor.rowcount
                        fill_table()
                        clear()
                        if rows_affected > 0:
                            messagebox.showinfo("OK","El cliente {} ha sido actualizado correctamente".format(name))
                        else:
                            messagebox.showwarning("Advertencia", "El cliente no existe o se cambio el rut")
                        
                    else:
                        messagebox.showerror("Error", "El teléfono solo debe tener números")
                        txt_phone.set("")
                        e_phone.focus()
                else:
                    messagebox.showerror("Error", "Llene todos los campos")
            except mysql.connector.Error as error:
                print(f"Error: {error}")  

        def delete_client(): # Eliminar cliente
            search_client()
            if txt_rut.get() !="":
                query = messagebox.askquestion("Confirmar", "Realmente desea eliminar a {} {}" .format(txt_name.get(), txt_lastname.get()))
                if query == "yes":
                    cursor.execute('delete from clientes where rut_cliente=%s', (txt_rut.get(),))
                    db.commit()
                    fill_table()
                    clear()
                    messagebox.showinfo("OK", "Cliente eliminado")
                else:
                    clear()
        
        ########## GUI de manage_clients() ##########
        # Labels
        Label(clients, text="RUT:", anchor="w", justify="left", width=7, font=font).grid(row=0, column=0, pady=20)
        Label(clients, text="Nombre:", anchor="w", justify="left", width=7, font=font).grid(row=1, column=0, pady=5)
        Label(clients, text="Apellido:", anchor="w", justify="left", width=7, font=font).grid(row=2, column=0, pady=5)
        Label(clients, text="Región:", anchor="w", justify="left", width=7, font=font).grid(row=3, column=0, pady=5)
        Label(clients, text="Ciudad:", anchor="w", justify="left", width=7, font=font).grid(row=4, column=0, pady=5)
        Label(clients, text="Calle:", anchor="w", justify="left", width=7, font=font).grid(row=5, column=0, pady=5)
        Label(clients, text="(Opcional)", anchor="w", justify="left", width=7, font="verdana, 10").grid(row=5, column=2, pady=5)
        Label(clients, text="Teléfono:", anchor="w", justify="left", width=7, font=font).grid(row=6, column=0, pady=5)
        Label(clients, text="Envío:", anchor="w", justify="left", width=7, font=font).grid(row=7, column=0, pady=5)

        # Entrys
        shipments = ["Starken", "Presencial"]

        e_rut = ttk.Entry(clients, font=font, textvariable=txt_rut)
        e_rut.grid(row=0, column=1, pady=5)

        e_name = ttk.Entry(clients, font=font, textvariable=txt_name)
        e_name.grid(row=1, column=1, pady=5)

        e_lastname = ttk.Entry(clients, font=font, textvariable=txt_lastname)
        e_lastname.grid(row=2, column=1, pady=5)

        e_region = ttk.Entry(clients, font=font, textvariable=txt_region)
        e_region.grid(row=3, column=1, pady=5)

        e_city = ttk.Entry(clients, font=font, textvariable=txt_city)
        e_city.grid(row=4, column=1, pady=5)

        e_street = ttk.Entry(clients, font=font, textvariable=txt_street)
        e_street.grid(row=5, column=1, pady=5)

        e_phone = ttk.Entry(clients, font=font, textvariable=txt_phone)
        e_phone.grid(row=6, column=1, pady=5)

        e_shipment = ttk.Combobox(clients, textvariable=txt_shipment, values=shipments, font="verdana, 19")
        e_shipment.grid(row=7, column=1, pady=5)

        # Botones
        ttk.Button(clients, text="Buscar", command=search_client, width=20).place(x=440, y=27)
        ttk.Button(clients, text="Agregar", command=save_client, width=20).grid(row=8, column=0, pady=10)
        ttk.Button(clients, text="Actualizar", command=update_client, width=20).grid(row=8, column=1, pady=10)
        ttk.Button(clients, text="Eliminar", command=delete_client, width=20).grid(row=8, column=2, pady=10)

        ttk.Button(clients, text="Volver", command=back, width=20).grid(row=9, column=1, pady=10)

        # Tabla de clientes
        Label(clients, text="Lista de Clientes", font="verdana, 24").place(x=730, y=5)
        table = ttk.Treeview(clients)
        table.place(x=600, y=50)
        # Configuración de columnas
        table["columns"] = ("RUT", "NOMBRE", "APELLIDO", "REGION", "CIUDAD", "CALLE", "TELEFONO", "ENVIO")
        table.column("#0", width=0, stretch=NO)
        table.column("RUT", width=100, anchor=CENTER)
        table.column("NOMBRE", width=150, anchor=CENTER)
        table.column("APELLIDO", width=150, anchor=CENTER)
        table.column("REGION", width=150, anchor=CENTER)
        table.column("CIUDAD", width=150, anchor=CENTER)
        table.column("CALLE", width=150, anchor=CENTER)
        table.column("TELEFONO", width=150, anchor=CENTER)
        table.column("ENVIO", width=100, anchor=CENTER)

        table.heading("#0", text="")
        table.heading("RUT", text="Rut")
        table.heading("NOMBRE", text="Nombre")
        table.heading("APELLIDO", text="Apellido")
        table.heading("REGION", text="Región")
        table.heading("CIUDAD", text="Ciudad")
        table.heading("CALLE", text="Calle")
        table.heading("TELEFONO", text="Teléfono")
        table.heading("ENVIO", text="Envío")

        fill_table()
        # Iniciar ventana de gestión de clientes
        clients.mainloop()

    def inventory(): # VENTANA DE INVENTARIO
        admin.destroy()
        inventory = Tk()
        inventory.title("Gestión de inventario")
        inventory.resizable(False, False)
        inventory.state("zoomed")

        # Rellenar combobox
        cursor.execute('select nombre from encuadernacion')
        binding = [row[0] for row in cursor.fetchall()]

        cursor.execute('select nombre from diseño')
        design = [row[0] for row in cursor.fetchall()]

        cursor.execute('select nombre from tamaño')
        sheet_size = [row[0] for row in cursor.fetchall()]

        cursor.execute('select nombre from elasticos')
        elastic = [row[0] for row in cursor.fetchall()]
        
        cursor.execute('select nombre from termolaminado')
        thermolaminated = [row[0] for row in cursor.fetchall()]

        # Variables de campos
        txt_category = tk.StringVar()
        txt_item = tk.StringVar()
        txt_change_amount = tk.StringVar()
        txt_change_price = tk.StringVar()
        txt_name = tk.StringVar()
        txt_amount = tk.StringVar()
        txt_price = tk.StringVar()

        ########## FUNCIONES de inventory ##########
        def back():
            inventory.destroy()
            administrator_menu()
        
        def clear():
            txt_change_amount.set("")
            txt_change_price.set("")
            txt_name.set("")
            txt_amount.set("")
            txt_price.set("")

        def fill_table_and_combobox(event):
            selected_item = e_category.get() # Obtener la opción seleccionada en el Combobox

            # Limpiar la tabla antes de llenarla con los nuevos datos
            for child in table.get_children():
                table.delete(child)

            # Obtener los resultados de la consulta SQL y llenar la tabla
            if selected_item == "encuadernacion":
                cursor.execute('SELECT * FROM encuadernacion')
                e_item['values'] = binding  # Establecer opciones para el segundo Combobox
                txt_change_amount.set("")
                txt_item.set("")
            elif selected_item == "diseño":
                cursor.execute('SELECT * FROM diseño')
                e_item['values'] = design  # Establecer opciones para el segundo Combobox
                txt_change_amount.set("No valido")
                txt_item.set("")
            elif selected_item == "tamaño":
                cursor.execute('SELECT * FROM tamaño')
                e_item['values'] = sheet_size  # Establecer opciones para el segundo Combobox
                txt_change_amount.set("")
                txt_item.set("")
            elif selected_item == "elasticos":
                cursor.execute('SELECT * FROM elasticos')
                e_item['values'] = elastic  # Establecer opciones para el segundo Combobox
                txt_change_amount.set("")
                txt_item.set("")
            elif selected_item == "termolaminado":
                cursor.execute('SELECT * FROM termolaminado')
                e_item['values'] = thermolaminated  # Establecer opciones para el segundo Combobox
                txt_change_amount.set("")
                txt_item.set("")
            
            result = cursor.fetchall()
            for row in result:
                table.insert("", tk.END, values=row)

        def fill_table():
            table.delete(*table.get_children())
            cursor.execute(f'select * from {txt_category.get()}')
            result = cursor.fetchall()
            for row in result:
                r = list(row)
                r.pop(0)
                r = tuple(r)
                table.insert("", END, text=id, values=row)
        
        def select_price(): # Seleccionar precio
            if txt_item.get() !="":
                try:
                    cursor.execute(f'select precio from {txt_category.get()} where nombre=%s', (txt_item.get(),))
                    result = cursor.fetchone()
                    txt_change_price.set(result[0])
                except:
                    messagebox.showerror("Error", "No existe el item")
                    clear()
            else:
                messagebox.showerror("Error", "Ingrese item")
                clear()

        def add(): # Agregar a las existencias
            if txt_item.get() !="":
                if txt_change_amount.get().isdigit():
                    cursor.execute(f'update {txt_category.get()} set cantidad = cantidad + %s where nombre=%s', (txt_change_amount.get(), txt_item.get()))
                    db.commit()
                    clear()
                    messagebox.showinfo("OK", "Suma realizada al inventario")
                    fill_table()
                else:
                    messagebox.showerror("ERROR", "El monto debe ser un número")
            else:
                messagebox.showerror("Error", "Ingrese item")
                clear()

        def subtract(): # Eliminar de la existencias
            if txt_item.get() !="":
                if txt_change_amount.get().isdigit():
                    cursor.execute(f'update {txt_category.get()} set cantidad = cantidad - %s where nombre=%s', (txt_change_amount.get(), txt_item.get()))
                    db.commit()
                    clear()
                    messagebox.showinfo("OK", "Resta realizada al inventario")
                    fill_table()
                else:
                    messagebox.showerror("ERROR", "El monto debe ser un número")
            else:
                messagebox.showerror("Error", "Ingrese item")
                clear()

        def change_price(): # Cambiar precio
            if txt_item.get() !="":
                if txt_change_price.get().isdigit():
                    cursor.execute(f'update {txt_category.get()} set precio=%s where nombre=%s', (txt_change_price.get(), txt_item.get()))
                    db.commit()
                    clear()
                    messagebox.showinfo("OK", "Precio actualizado")
                    fill_table()
                else:
                    messagebox.showerror("ERROR", "El monto debe ser un número")
            else:
                messagebox.showerror("Error", "Ingrese item")
                clear()

        def save_item(): # Guardar nuevo item
            name = txt_name.get()
            amount = txt_amount.get()
            price = txt_price.get()
            
            if txt_category.get() !="":
                try:
                    if name !="" and amount !="" and price !="":
                        if amount.isnumeric() and price.isnumeric():
                            cursor.execute(f'insert into {txt_category.get()} values (%s, %s, %s)', (name.capitalize(), amount, price))
                            db.commit()
                            fill_table()
                            clear()
                            messagebox.showinfo("OK","El cliente {} ha sido ingresado correctamente".format(name))
                        else:
                            messagebox.showerror("Error", "La cantidad y el precio solo deben ser números")
                    else:
                        messagebox.showerror("Error", "Llene todos los campos")
                except:
                    messagebox.showerror("Error", "Ya existe un item con ese nombre")
            else:
                messagebox.showerror("Error", "Ingrese una categoría")
                clear()

        def delete_item(): # Eliminar item
            if txt_item.get() !="":
                query = messagebox.askquestion("Confirmar", "Realmente desea eliminar el item {}" .format(txt_item.get()))
                if query == "yes":
                    cursor.execute(f'delete from {txt_category.get()} where nombre=%s', (txt_item.get(),))
                    db.commit()
                    fill_table()
                    clear()
                    messagebox.showinfo("OK", "Item eliminado")
                else:
                    clear()

        ########## GUI de inventory ##########
        # Lista de opciones para el Combobox e_category
        options = ["encuadernacion", "diseño", "tamaño", "elasticos", "termolaminado"]

        # Labels
        Label(inventory, text="Categoría:", anchor="w", justify="left", width=8, font=font).grid(row=0, column=0, pady=10)
        Label(inventory, text="Item:", anchor="w", justify="left", width=8, font=font).grid(row=1, column=0, pady=10)
        Label(inventory, text="", anchor="w", justify="left", width=8, font=font).grid(row=2, columnspan=2, pady=10)
        Label(inventory, text="Existencias:", anchor="w", justify="left", width=10, font=font).grid(row=3, column=0, pady=10)
        Label(inventory, text="Precio:", anchor="w", justify="left", width=8, font=font).grid(row=5, column=0, pady=10)
        Label(inventory, text="Nuevo", anchor="w", justify="left", width=8, font=font).grid(row=6, columnspan=2, pady=10)
        Label(inventory, text="Nombre:", anchor="w", justify="left", width=8, font=font).grid(row=7, column=0, pady=10)
        Label(inventory, text="Cantidad:", anchor="w", justify="left", width=8, font=font).grid(row=8, column=0, pady=10)
        Label(inventory, text="Precio:", anchor="w", justify="left", width=8, font=font).grid(row=9, column=0, pady=10)

        # Entrys
        e_category = ttk.Combobox(inventory, textvariable=txt_category, values=options, font="verdana, 19")
        e_category.grid(row=0, column=1, pady=5)
        e_category.bind("<<ComboboxSelected>>", fill_table_and_combobox)

        e_item = ttk.Combobox(inventory, textvariable=txt_item, values=[], font="verdana, 19")
        e_item.grid(row=1, column=1, pady=5)

        e_change_amount = ttk.Entry(inventory, font=font, textvariable=txt_change_amount)
        e_change_amount.grid(row=3, column=1, pady=5)

        e_change_price = ttk.Entry(inventory, font=font, textvariable=txt_change_price)
        e_change_price.grid(row=5, column=1, pady=5)

        e_name = ttk.Entry(inventory, font=font, textvariable=txt_name)
        e_name.grid(row=7, column=1, pady=5)

        e_amount = ttk.Entry(inventory, font=font, textvariable=txt_amount)
        e_amount.grid(row=8, column=1, pady=5)

        e_price = ttk.Entry(inventory, font=font, textvariable=txt_price)
        e_price.grid(row=9, column=1, pady=5)

        # Buttons
        ttk.Button(inventory, text="Precio", width=15, command=select_price).grid(row=1, column=2, padx=5)
        ttk.Button(inventory, text="Eliminar", width=15, command=delete_item).grid(row=1, column=3, padx=5)
        ttk.Button(inventory, text="Agregar", width=20, command=add).grid(row=3, column=2, padx=5)
        ttk.Button(inventory, text="Restar", width=20, command=subtract).grid(row=3, column=3, padx=5)
        ttk.Button(inventory, text="Cambiar precio", width=20, command=change_price).grid(row=5, column=2, padx=5)
        ttk.Button(inventory, text="Agregar", width=20, command=save_item).grid(row=10, columnspan=2, padx=5)
        ttk.Button(inventory, text="Volver", width=20, command=back).grid(row=12, columnspan=2, pady=20)

        # Tablaque varia según lo seleccionado en e_category
        table = ttk.Treeview(inventory)
        table.place(x=780, y=90)
        # Configuración de columnas
        table["columns"] = ("NOMBRE", "CANTIDAD", "PRECIO")
        table.column("#0", width=0, stretch=NO)
        table.column("NOMBRE", width=150, anchor=CENTER)
        table.column("CANTIDAD", width=100, anchor=CENTER)
        table.column("PRECIO", width=100, anchor=CENTER)

        table.heading("#0", text="")
        table.heading("NOMBRE", text="Nombre")
        table.heading("CANTIDAD", text="Cantidad")
        table.heading("PRECIO", text="Precio")
        
        # Iniciar ventana de inventario
        inventory.mainloop()

    def diary(): # VENTANA DE AGENDADO DE FECHAS
        admin.destroy()
        diary = Tk()
        diary.title("Agenda")
        diary.resizable(False, False)
        diary.state("zoomed")

        now = datetime.datetime.now()

        # Varables de campo
        txt_id = tk.StringVar()
        txt_day = tk.StringVar()
        txt_month = tk.StringVar()
        txt_year = tk.StringVar()
        txt_year.set(now.year)
        txt_description = tk.StringVar()

        ########## FUNCIONES de administrator_menu ##########
        def back(): # Volver al menú de adminstrador
            diary.destroy()
            administrator_menu()

        def fill_table(): # Rellenar tabla de fechas
            table.delete(*table.get_children())
            cursor.execute('select * from fechas_importantes')
            result = cursor.fetchall()
            for row in result:
                r = list(row)
                r.pop(0)
                r = tuple(r)
                table.insert("", END, text=id, values=row)

        def clear(): # Limpiar campos
            txt_day.set("")
            txt_month.set("")
            txt_description.set("")

        def save_date(): # Guardar fecha
            day = txt_day.get()
            month = txt_month.get()
            year = txt_year.get()
            description = txt_description.get()

            try:
                if day !="" and month !="" and year !="" and description !="":
                    if day.isdigit() and month.isdigit() and year.isdigit():
                        date = f"{year}-{month}-{day}" # Ajustar la fecha a la base de datos
                        cursor.execute('insert into fechas_importantes (fecha, descripción) values (%s, %s)', (date, description))
                        db.commit()
                        fill_table()
                        clear()
                        messagebox.showinfo("OK","Fecha ingresada correctamente")
                    else:
                        messagebox.showerror("Error", "La fecha deben ser números")
                else:
                    messagebox.showerror("Error", "Llene todos los campos")
            except mysql.connector.Error as error:
                print(f"Error: {error}")

        def update_date(): # Actualizar fecha
            id_date = txt_id.get()
            day = txt_day.get()
            month = txt_month.get()
            year = txt_year.get()
            description = txt_description.get()

            try:
                if id_date !="" and day !="" and month !="" and year !="" and description !="":
                    if day.isdigit() and month.isdigit() and year.isdigit():
                        date = f"{year}-{month}-{day}" # Ajustar la fecha a la base de datos
                        cursor.execute('update fechas_importantes set fecha=%s , descripción=%s where id_fecha=%s', (date, description, id_date))
                        db.commit()
                        fill_table()
                        clear()
                        messagebox.showinfo("OK","Fecha actualizada correctamente")
                    else:
                        messagebox.showerror("Error", "La fecha deben números")
                else:
                    messagebox.showerror("Error", "Llene todos los campos")
            except:
                messagebox.showerror("Error", "No existe la fecha agendada")

        def delete_date(): # Eliminar fecha
            search_date()
            if txt_id.get() !="":
                query = messagebox.askquestion("Confirmar", "¿Realmente desea eliminar la fecha?")
                if query == "yes":
                    cursor.execute('delete from fechas_importantes where id_fecha=%s', (txt_id.get(),))
                    db.commit()
                    fill_table()
                    clear()
                    messagebox.showinfo("OK", "Fecha eliminada")
                else:
                    clear()
        
        def search_date(): # Buscar fecha por ID
            if txt_id.get() !="":
                try:
                    cursor.execute('select * from fechas_importantes where id_fecha=%s', (txt_id.get(),))
                    result = cursor.fetchone()
                    txt_id.set(result[0])
                    txt_description.set(result[2])
                except:
                    messagebox.showerror("Error", "No existe la fecha")
                    clear()
            else:
                messagebox.showerror("Error", "Ingrese un ID")
                clear()

        ########## GUI de diary ##########
        Label(diary, text="Agenda", font="verdana, 24").pack(pady=20)

        # Tabla de ganancias
        table = ttk.Treeview(diary)
        table.pack(pady=20)
        # Configuración de columnas
        table["columns"] = ("ID", "FECHA", "DESCRIPCION")
        table.column("#0", width=0, stretch=NO)
        table.column("ID", width=30, anchor=CENTER)
        table.column("FECHA", width=100, anchor=CENTER)
        table.column("DESCRIPCION", width=400, anchor=CENTER)

        table.heading("#0", text="")
        table.heading("ID", text="ID")
        table.heading("FECHA", text="Fecha")
        table.heading("DESCRIPCION", text="Descripción")
        fill_table() # Llenado de la tabla ganancias

        Label(diary, text="ID (automática):", font="verdana, 24").place(x=680, y=356)
        ttk.Entry(diary, font=font, textvariable=txt_id, width=5).pack(pady=10)
        ttk.Button(diary, text="Buscar", width=20, command=search_date).place(x=1015, y=365)

        Label(diary, text="Fecha", font="verdana, 24").pack()
        Label(diary, text="", font="verdana, 24").pack(pady=20)
        Label(diary, text="Día:", font="verdana, 24").place(x=700, y=465)
        Label(diary, text="Mes:", font="verdana, 24").place(x=870, y=465)
        Label(diary, text="Año:", font="verdana, 24").place(x=1050, y=465)
        ttk.Entry(diary, font=font, textvariable=txt_day, width=5).place(x=770, y=465)
        ttk.Entry(diary, font=font, textvariable=txt_month, width=5).place(x=950, y=465)
        ttk.Entry(diary, font=font, textvariable=txt_year, width=5).place(x=1125, y=465)

        Label(diary, text="Descripción", font="verdana, 24").pack()
        ttk.Entry(diary, font=font, textvariable=txt_description, width=40).pack()

        # Buttons
        ttk.Button(diary, text="Agregar", width=20, command=save_date).pack(pady=10)
        ttk.Button(diary, text="Modificar", width=20, command=update_date).pack(pady=10)
        ttk.Button(diary, text="Eliminar", width=20, command=delete_date).pack(pady=10)
        ttk.Button(diary, text="Volver", width=20, command=back).pack(pady=20)

        diary.mainloop()

    def profits(): # VENTA DE RECUENTO MENSUAL DE GANANCIAS
        admin.destroy()
        profit = Tk()
        profit.title("Recuento de ganancias")
        profit.resizable(False, False)

        # Centrar ventana
        height = 600
        width = 330
        x_v = profit.winfo_screenwidth() // 2 - width //2
        y_v = profit.winfo_screenheight() // 2 - width //2
        pos = str(width)+"x"+str(height)+"+"+str(x_v)+"+"+str(y_v)
        profit.geometry(pos)
        
        ########## FUNCIONES de manage_clients() ##########
        def back(): # Volver al menú
            profit.destroy()
            administrator_menu()

        def fill_table(): # Llenar la tabla con los datos de ganancias
            # Obtener el año y mes actual
            now = datetime.datetime.now()
            year = now.year
            month = now.month
            table.delete(*table.get_children())
            cursor.execute('select * from ganancias where year(fecha)=%s and month(fecha)=%s', (year, month))
            result = cursor.fetchall()
            for row in result:
                r = list(row)
                r.pop(0)
                r = tuple(r)
                table.insert("", END, text=id, values=row)

        def total_profit(): # Sumar las ganancias del mes
            # Obtener el año y mes actual
            now = datetime.datetime.now()
            year = now.year
            month = now.month
            cursor.execute('select sum(precio) from ganancias where year(fecha)=%s and month(fecha)=%s', (year, month))
            total_profit = cursor.fetchone()[0]
            return total_profit
        
        ########## GUI de profits ##########
        Label(profit, text="Ganancias del mes", font="verdana, 24").pack(pady=20)

        # Tabla de ganancias
        table = ttk.Treeview(profit)
        table.pack(pady=20)
        # Configuración de columnas
        table["columns"] = ("FECHA", "GANANCIA")
        table.column("#0", width=0, stretch=NO)
        table.column("FECHA", width=100, anchor=CENTER)
        table.column("GANANCIA", width=100, anchor=CENTER)

        table.heading("#0", text="")
        table.heading("FECHA", text="Fecha")
        table.heading("GANANCIA", text="Ganancia")

        fill_table() # Llenado de la tabla ganancias

        Label(profit, text="Ganancia total:", font="verdana, 24").pack(pady=20)
        Label(profit, text=total_profit(), font="verdana, 24").pack()
        
        # Buttons
        ttk.Button(profit, text="Volver", width=20, command=back).pack(pady=20)

        # Iniciar ventana de recuento de ganancias
        profit.mainloop()

    def close_session(): # Cerrar la ventana de menú administrador y abrir la de logueo
        admin.destroy()
        Login.start()

    ########## GUI de administrator_menu ##########
    font = "verdana, 20"
    # Buttons
    ttk.Button(admin, text="Usuarios", width=30, command=manage_users).pack(pady=5)
    ttk.Button(admin, text="Clientes", width=30, command=manage_clients).pack(pady=5)
    ttk.Button(admin, text="Inventario", width=30, command=inventory).pack(pady=5)
    ttk.Button(admin, text="Agenda", width=30, command=diary).pack(pady=5)
    ttk.Button(admin, text="Recuento", width=30, command=profits).pack(pady=5)
    ttk.Button(admin, text="Cerrar Sesión", width=20, command=close_session).pack(pady=20)

    # Iniciar ventana de menú administrador
    admin.mainloop()
    
if __name__ == '__main__':
    administrator_menu()