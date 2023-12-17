import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import calendar
import datetime
import Login

def seller_menu():
    sell = Tk()
    sell.title("Menú Vendedor")
    sell.resizable(False, False)

    height = 280
    width = 330
    x_v = sell.winfo_screenwidth() // 2 - width //2
    y_v = sell.winfo_screenheight() // 2 - width //2
    pos = str(width)+"x"+str(height)+"+"+str(x_v)+"+"+str(y_v)
    sell.geometry(pos)

    # Conexión a la base de datos
    db = mysql.connector.connect(host = 'localhost', port = 3306, user = 'root', password = '', database = 'frutilla_rosada_db')
    cursor = db.cursor()

    ########## FUNCIONES de seller_menu ##########
    def orders_panel(): # VENTANA DE PEDIDOS
        sell.destroy()
        orders = Tk()
        orders.title("Pedidos")
        orders.resizable(False, False)
        orders.state("zoomed")
        
        now = datetime.datetime.now()

        # Varables de campo
        txt_id = tk.StringVar()
        txt_id.set("ID automático")
        txt_rut_client = tk.StringVar()
        txt_admission_day = tk.StringVar()
        txt_admission_day.set(now.day)
        txt_admission_month = tk.StringVar()
        txt_admission_month.set(now.month)
        txt_admission_year = tk.StringVar()
        txt_admission_year.set(now.year)
        txt_binding = tk.StringVar()
        txt_design = tk.StringVar()
        txt_sheet_size = tk.StringVar()
        txt_quantity = tk.StringVar()
        txt_elastic = tk.StringVar()
        txt_thermolaminated = tk.StringVar()
        txt_comentary = tk.StringVar()
        txt_finish_day = tk.StringVar()
        txt_finish_day.set(now.day)
        txt_finish_month = tk.StringVar()
        txt_finish_month.set(now.month)
        txt_finish_year = tk.StringVar()
        txt_finish_year.set(now.year)

        ########## FUNCIONES de orders_panel ##########
        def back(): # Volver al menú
            orders.destroy()
            seller_menu()

        def fill_table(): # Rellenar tabla de pedidos
            table.delete(*table.get_children())
            cursor.execute('select id_pedido, rut_cliente, fecha_ingreso, tipo_encuadernacion, tipo_diseño, tamaño_hoja, cantidad_hojas, elastico, termolaminado, comentarios, precio from pedidos where fecha_salida is null')
            result = cursor.fetchall()
            for row in result:
                r = list(row)
                r.pop(0)
                r = tuple(r)
                table.insert("", END, text=id, values=row)

        def clear(): # Limpiar los campos
            txt_rut_client.set("")
            txt_binding.set("")
            txt_design.set("")
            txt_sheet_size.set("")
            txt_quantity.set("")
            txt_elastic.set("")
            txt_thermolaminated.set("")
            txt_comentary.set("")

        def save_order(): # Guardar pedido
            rut_client = txt_rut_client.get()
            day = txt_admission_day.get()
            month = txt_admission_month.get()
            year = txt_admission_year.get()
            income = f"{year}-{month}-{day}" # Ajustar la fecha a la base de datos
            binding = txt_binding.get()
            design = txt_design.get()
            sheet_size = txt_sheet_size.get()
            quantity = txt_quantity.get()
            elastic = txt_elastic.get()
            thermolaminated = txt_thermolaminated.get()
            comentary = txt_comentary.get()
            try:
                if rut_client !="" and day !="" and month !="" and year !="" and binding !="" and design !="" and sheet_size !="" and quantity !="" and elastic !="" and thermolaminated !="":
                    if quantity.isdigit():
                        # Extracción de precios
                        cursor.execute('select precio from encuadernacion where nombre=%s', (binding,))
                        result = cursor.fetchone()
                        price_binding = result[0]
                        cursor.execute('select precio from diseño where nombre=%s', (design,))
                        result = cursor.fetchone()
                        price_design = result[0]
                        cursor.execute('select precio from tamaño where nombre=%s', (sheet_size,))
                        result = cursor.fetchone()
                        price_sheet_size = result[0]
                        int_quantity = int(quantity)
                        cursor.execute('select precio from elasticos where nombre=%s', (elastic,))
                        result = cursor.fetchone()
                        price_elastic = result[0]
                        cursor.execute('select precio from termolaminado where nombre=%s', (thermolaminated,))
                        result = cursor.fetchone()
                        price_thermolaminated = result[0]
                        total_price = price_binding + price_design + (price_sheet_size * int_quantity) + price_elastic + price_thermolaminated
                        
                        cursor.execute('insert into pedidos (rut_cliente, fecha_ingreso, tipo_encuadernacion, tipo_diseño, tamaño_hoja, cantidad_hojas, elastico, termolaminado, comentarios, precio) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                                       (rut_client, income, binding, design, sheet_size, quantity, elastic, thermolaminated, comentary, total_price))
                        db.commit()
                        fill_table()
                        clear()
                        
                        # Actualizar las cantidades del inventario
                        if elastic == "Sin Elastico":
                            cursor.execute('update encuadernacion set cantidad = cantidad - 1 where nombre=%s', (binding,))
                            db.commit()
                            cursor.execute('update tamaño set cantidad = cantidad - %s where nombre=%s', (quantity, sheet_size))
                            db.commit()
                            cursor.execute('update termolaminado set cantidad = cantidad - 1 where nombre=%s', (thermolaminated,))
                            db.commit()
                        else:
                            cursor.execute('update encuadernacion set cantidad = cantidad - 1 where nombre=%s', (binding,))
                            db.commit()
                            cursor.execute('update tamaño set cantidad = cantidad - %s where nombre=%s', (quantity, sheet_size))
                            db.commit()
                            cursor.execute('update elasticos set cantidad = cantidad - 1 where nombre=%s', (elastic,))
                            db.commit()
                            cursor.execute('update termolaminado set cantidad = cantidad - 1 where nombre=%s', (thermolaminated,))
                            db.commit()
                    else:
                        messagebox.showerror("Error", "La cantidad de hojas debe ser un número")
                else:
                    messagebox.showerror("Error", "Llene todos los campos obligatorios")
            except:
                messagebox.showerror("Error", "El cliente no existe, por favor agregar")

        def quote(): # Cotizar pedido sin guardar
            binding = txt_binding.get()
            design = txt_design.get()
            sheet_size = txt_sheet_size.get()
            quantity = txt_quantity.get()
            elastic = txt_elastic.get()
            thermolaminated = txt_thermolaminated.get()
            try:
                if binding !="" and design !="" and sheet_size !="" and quantity !="" and elastic !="" and thermolaminated !="":
                    if quantity.isdigit():
                        # Extracción de precios
                        cursor.execute('select precio from encuadernacion where id_encuadernacion=%s', (binding,))
                        result = cursor.fetchone()
                        price_binding = result[0]
                        cursor.execute('select precio from diseño where id_diseño=%s', (design,))
                        result = cursor.fetchone()
                        price_design = result[0]
                        cursor.execute('select precio from tamaño where id_tamaño=%s', (sheet_size,))
                        result = cursor.fetchone()
                        price_sheet_size = result[0]
                        int_quantity = int(quantity)
                        cursor.execute('select precio from elasticos where id_elastico=%s', (elastic,))
                        result = cursor.fetchone()
                        price_elastic = result[0]
                        cursor.execute('select precio from termolaminado where id_termolaminado=%s', (thermolaminated,))
                        result = cursor.fetchone()
                        price_thermolaminated = result[0]

                        total_quote = price_binding + price_design + (price_sheet_size * int_quantity) + price_elastic + price_thermolaminated

                        messagebox.showinfo("Cotización", "El valor es de: {}".format(total_quote))
                    else:
                        messagebox.showerror("Error", "La cantidad de hojas debe ser un número")
                else:
                    messagebox.showerror("Error", "Llene todos los campos obligatorios para la cotización")
            except:
                messagebox.showerror("Error", "Error asociado a la base de datos")

        def search_order(): # Buscar pedido
            if txt_id.get().isdigit():
                try:
                    cursor.execute('select * from pedidos where id_pedido=%s', (txt_id.get(),))
                    result = cursor.fetchone()
                    txt_rut_client.set(result[1])
                    txt_binding.set(result[4])
                    txt_design.set(result[5])
                    txt_sheet_size.set(result[6])
                    txt_quantity.set(result[7])
                    txt_elastic.set(result[8])
                    txt_thermolaminated.set(result[9])
                    txt_comentary.set(result[10])
                    txt_id.set("")
                except:
                    messagebox.showerror("Error", "No existe el pedido")
                    clear()
                    e_id.focus()
                    txt_id.set("")
            else:
                messagebox.showerror("Error", "Ingrese un ID numérico")
                clear()
                e_id.focus()

        def update_order(): # Actualizar pedido
            id_order = txt_id.get()
            rut_client = txt_rut_client.get()
            day = txt_admission_day.get()
            month = txt_admission_month.get()
            year = txt_admission_year.get()
            income = f"{year}-{month}-{day}" # Ajustar la fecha a la base de datos
            binding = txt_binding.get()
            design = txt_design.get()
            sheet_size = txt_sheet_size.get()
            quantity = txt_quantity.get()
            elastic = txt_elastic.get()
            thermolaminated = txt_thermolaminated.get()
            comentary = txt_comentary.get()
            if rut_client !="" and day !="" and month !="" and year !="" and binding !="" and design !="" and sheet_size !="" and quantity !="" and elastic !="" and thermolaminated !="" and id !="":
                if quantity.isdigit() and id_order.isdigit():
                # Extracción de precios
                    cursor.execute('select precio from encuadernacion where nombre=%s', (binding,))
                    result = cursor.fetchone()
                    price_binding = result[0]
                    cursor.execute('select precio from diseño where nombre=%s', (design,))
                    result = cursor.fetchone()
                    price_design = result[0]
                    cursor.execute('select precio from tamaño where nombre=%s', (sheet_size,))
                    result = cursor.fetchone()
                    price_sheet_size = result[0]
                    int_quantity = int(quantity)
                    cursor.execute('select precio from elasticos where nombre=%s', (elastic,))
                    result = cursor.fetchone()
                    price_elastic = result[0]
                    cursor.execute('select precio from termolaminado where nombre=%s', (thermolaminated,))
                    result = cursor.fetchone()
                    price_thermolaminated = result[0]
                    total_price = price_binding + price_design + (price_sheet_size * int_quantity) + price_elastic + price_thermolaminated
                    cursor.execute('update pedidos set rut_cliente=%s, fecha_ingreso=%s, tipo_encuadernacion=%s, tipo_diseño=%s, tamaño_hoja=%s, cantidad_hojas=%s, elastico=%s, termolaminado=%s, comentarios=%s, precio=%s where id_pedido=%s', (rut_client, income, binding, design, sheet_size, quantity, elastic, thermolaminated, comentary, total_price, id_order))
                    db.commit()
                    rows_affected = cursor.rowcount
                    fill_table()
                    clear()
                    if rows_affected > 0:
                        messagebox.showinfo("OK","El pedido ha sido actualizado correctamente")
                    else:
                        messagebox.showwarning("Advertencia", "El pedido no existe o ya caducó")
                else:
                    messagebox.showerror("Error", "La cantidad de hojas y el ID deben ser un número")
            else:
                messagebox.showerror("Error", "Llene todos los campos obligatorios")

        def finish_order(): # Finalizar pedido
            if txt_id.get().isdigit():
                try:
                    day = txt_finish_day.get()
                    month = txt_finish_month.get()
                    year = txt_finish_year.get()
                    finish = f"{year}-{month}-{day}"
                    cursor.execute('update pedidos set fecha_salida=%s where id_pedido=%s', (finish, txt_id.get()))
                    db.commit()
                    rows_affected = cursor.rowcount
                    fill_table()
                    clear()
                    if rows_affected > 0:
                        messagebox.showinfo("OK","El pedido {} ha sido finalizado".format(txt_id.get()))
                    else:
                        messagebox.showwarning("Advertencia", "El pedido no existe o caducó")
                except mysql.connector.Error as error:
                    print(f"Error: {error}")  
            else:
                messagebox.showerror("Error", "Ingrese un ID numérico")
                clear()
                e_id.focus()

        ########## GUI de orders_panel ##########

        # Labels
        Label(orders, text="ID pedido:", anchor="w", justify="left", width=13, font=font).grid(row=0, column=0, pady=5)
        Label(orders, text="RUT cliente:", anchor="w", justify="left", width=13, font=font).grid(row=1, column=0, pady=20)
        Label(orders, text="Fecha de ingreso", anchor="w", justify="left", width=13, font=font).grid(row=2, columnspan=2, pady=5)
        Label(orders, text="", anchor="w", justify="left", font=font).grid(row=3, column=1, pady=5)
        Label(orders, text="Día:", anchor="w", justify="left", width=5, font=font).place(x= 50, y=170)
        Label(orders, text="Mes:", anchor="w", justify="left", width=5, font=font).place(x= 195, y=170)
        Label(orders, text="Año:", anchor="w", justify="left", width=5, font=font).place(x= 345, y=170)
        Label(orders, text="Encuadernación:", anchor="w", justify="left", width=13, font=font).grid(row=5, column=0, pady=5)
        Label(orders, text="Diseño:", anchor="w", justify="left", width=13, font=font).grid(row=6, column=0, pady=5)
        Label(orders, text="Tamaño hoja:", anchor="w", justify="left", width=13, font=font).grid(row=7, column=0, pady=5)
        Label(orders, text="Cantidad hojas:", anchor="w", justify="left", width=13, font=font).grid(row=8, column=0, pady=5)
        Label(orders, text="Elastico:", anchor="w", justify="left", width=13, font=font).grid(row=9, column=0, pady=5)
        Label(orders, text="Termolaminado:", anchor="w", justify="left", width=13, font=font).grid(row=10, column=0, pady=5)
        Label(orders, text="Comentarios:", anchor="w", justify="left", width=13, font=font).grid(row=11, column=0, pady=5)
        Label(orders, text="Fecha finalización", anchor="w", justify="left", width=15, font=font).grid(row=14, columnspan=2, pady=5)
        Label(orders, text="Día:", anchor="w", justify="left", width=5, font=font).place(x= 50, y=700)
        Label(orders, text="Mes:", anchor="w", justify="left", width=5, font=font).place(x= 195, y=700)
        Label(orders, text="Año:", anchor="w", justify="left", width=5, font=font).place(x= 345, y=700)
        

        # Rellenar los Combobox
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

        # Entrys
        e_id = ttk.Entry(orders, font=font, textvariable=txt_id)
        e_id.grid(row=0, column=1, pady=5)

        e_rut_client = ttk.Entry(orders, font=font, textvariable=txt_rut_client)
        e_rut_client.grid(row=1, column=1, pady=5)

        e_day = ttk.Entry(orders, font=font, textvariable=txt_admission_day, width=5)
        e_day.place(x=110, y=170)

        e_month = ttk.Entry(orders, font=font, textvariable=txt_admission_month, width=5)
        e_month.place(x=260, y=170)

        e_year = ttk.Entry(orders, font=font, textvariable=txt_admission_year, width=5)
        e_year.place(x=410, y=170)

        e_binding = ttk.Combobox(orders, textvariable=txt_binding, values=binding, font="verdana, 19")
        e_binding.grid(row=5, column=1, pady=5)

        e_design = ttk.Combobox(orders, textvariable=txt_design, values=design, font="verdana, 19")
        e_design.grid(row=6, column=1, pady=5)

        e_sheet_size = ttk.Combobox(orders, textvariable=txt_sheet_size, values=sheet_size, font="verdana, 19")
        e_sheet_size.grid(row=7, column=1, pady=5)

        e_quantity = ttk.Entry(orders, font=font, textvariable=txt_quantity, width=5)
        e_quantity.grid(row=8, column=1, pady=5)

        e_elastic = ttk.Combobox(orders, textvariable=txt_elastic, values=elastic, font="verdana, 19")
        e_elastic.grid(row=9, column=1, pady=5)

        e_thermolaminated = ttk.Combobox(orders, textvariable=txt_thermolaminated, values=thermolaminated, font="verdana, 19")
        e_thermolaminated.grid(row=10, column=1, pady=5)

        e_comentary = ttk.Entry(orders, font=font, textvariable=txt_comentary)
        e_comentary.grid(row=11, column=1, pady=5)

        e_day_finish = ttk.Entry(orders, font=font, textvariable=txt_finish_day, width=5)
        e_day_finish.place(x=110, y=700)

        e_month_finish = ttk.Entry(orders, font=font, textvariable=txt_finish_month, width=5)
        e_month_finish.place(x=260, y=700)

        e_year_finish = ttk.Entry(orders, font=font, textvariable=txt_finish_year, width=5)
        e_year_finish.place(x=410, y=700)

        

        # Buttons
        ttk.Button(orders, text="Buscar", command=search_order, width=20).place(x=530, y=13)
        ttk.Button(orders, text="Agregar", command=save_order, width=20).grid(row=12, column=0, pady=10)
        ttk.Button(orders, text="Actualizar", command=update_order, width=20).grid(row=12, column=1, pady=10)
        ttk.Button(orders, text="Cotizar", command=quote, width=20).grid(row=13, column=1, pady=10)
        ttk.Button(orders, text="Volver", command=back, width=20).grid(row=13, column=0, pady=10)
        ttk.Button(orders, text="Finalizar", command=finish_order, width=20).place(x=200, y=760)

        # Tabla de clientes
        Label(orders, text="Lista de Pedidos", font="verdana, 24").place(x=1100, y=30)
        table = ttk.Treeview(orders)
        table.place(x=600, y=100)
        # Configuración de columnas
        table["columns"] = ("ID", "RUT_CLIENTE", "FECHA_INGRESO", "ENCUADERNACIÓN", "DISEÑO", "HOJA", "CANTIDAD", "ELASTICO", "TERMOLAMINADO", "COMENTARIOS", "PRECIO")
        table.column("#0", width=0, stretch=NO)
        table.column("ID", width=30, anchor=CENTER)
        table.column("RUT_CLIENTE", width=100, anchor=CENTER)
        table.column("FECHA_INGRESO", width=100, anchor=CENTER)
        table.column("ENCUADERNACIÓN", width=100, anchor=CENTER)
        table.column("DISEÑO", width=150, anchor=CENTER)
        table.column("HOJA", width=70, anchor=CENTER)
        table.column("CANTIDAD", width=70, anchor=CENTER)
        table.column("ELASTICO", width=120, anchor=CENTER)
        table.column("TERMOLAMINADO", width=100, anchor=CENTER)
        table.column("COMENTARIOS", width=350, anchor=CENTER)
        table.column("PRECIO", width=70, anchor=CENTER)

        table.heading("#0", text="")
        table.heading("ID", text="ID")
        table.heading("RUT_CLIENTE", text="Rut Cliente")
        table.heading("FECHA_INGRESO", text="Fecha de Ingreso")
        table.heading("ENCUADERNACIÓN", text="Encuadernación")
        table.heading("DISEÑO", text="Tipo de Diseño")
        table.heading("HOJA", text="Hoja")
        table.heading("CANTIDAD", text="Cantidad")
        table.heading("ELASTICO", text="Elástico")
        table.heading("TERMOLAMINADO", text="Termolaminado")
        table.heading("COMENTARIOS", text="Comentarios")
        table.heading("PRECIO", text="Precio")

        fill_table()
        # Iniciar ventana de pedidos
        orders.mainloop()

    def manage_clients(): # VENTANA DE GESTIÓN DE CLIENTES
        sell.destroy()
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
            seller_menu()
        
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

    def close_session(): # Cerrar la ventana de menú administrador y abrir la de logueo
        sell.destroy()
        Login.start()

    ########## GUI de seller_menu ##########
    font = "verdana, 20"

    # Label
    Label(sell, text="").pack()

    # Button
    ttk.Button(sell, text="Pedidos/Cotizar", width=30, command=orders_panel).pack(pady=5)
    ttk.Button(sell, text="Clientes", width=30, command=manage_clients).pack(pady=5)
    ttk.Button(sell, text="Cerrar Sesión", width=20, command=close_session).pack(pady=20)

    # Iniciar ventana de menú vendedor
    sell.mainloop()



if __name__ == '__main__':
    seller_menu()