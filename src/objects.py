# Librerías y dependencias
from tkinter import ttk
from tkinter import *
import sqlite3
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Producto:
    db = 'databases/Productos.db'
    editar = False

    def __init__(self, root):
        self.ventana = root
        self.ventana.title('App Gestor de Productos')
        self.ventana.resizable(1, 1)
        self.ventana.wm_iconbitmap('img/M6_P2_icon.ico')

        # Crear pestañas
        tabControl = ttk.Notebook(self.ventana)
        self.tab1 = ttk.Frame(tabControl)
        self.tab2 = ttk.Frame(tabControl)
        tabControl.add(self.tab1, text='Gestion')
        tabControl.add(self.tab2 , text='Analisis')

        # 1. Creación del contenedor Frame principal
        frame = LabelFrame(self.ventana, text='Registrar un nuevo Producto')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # 2. Label Nombre
        self.etiqueta_nombre = Label(frame, text='Nombre: ')
        self.etiqueta_nombre.grid(row=1, column=0)
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1,columnspan = 2, sticky = W + E)

        # 4. Precio
        self.etiqueta_precio = Label(frame, text='Precio: ')
        self.etiqueta_precio.grid(row=2, column=0)
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1,columnspan = 2, sticky = W + E)

        # 6. Entry stock
        self.etiqueta_stock = Label(frame, text='Stock: ')
        self.etiqueta_stock.grid(row=3, column=0)
        self.stock = Entry(frame)
        self.stock.grid(row=3, column=1,columnspan = 2, sticky = W + E)

        # 7. Entry categoria
        self.etiqueta_categoria = Label(frame, text='Categoria: ')
        self.etiqueta_categoria.grid(row=4, column=0)
        categorias = ['Tecnologia', 'Musica', 'Juegos', 'Cursos', 'Libros', 'Otros']
        self.categoria_usuario = StringVar(self.ventana)
        self.categoria_usuario.set(categorias[0])
        self.categoria = OptionMenu(frame, self.categoria_usuario, *categorias)
        self.categoria.grid(row=4, column=1, columnspan = 2, sticky = W + E)


        # 6. Botón de Añadir Producto
        style = ttk.Style()
        style.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_aniadir = ttk.Button(frame, text = 'Guardar Producto', command = self.add_producto, style='my.TButton')
        self.boton_aniadir.grid(row=5, columnspan = 2, sticky = W + E)

        # 8. Botón de Editar Producto
        style = ttk.Style()
        style.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_editar = ttk.Button(frame, text='Editar Producto', command=self.editar_producto, style='my.TButton')
        self.boton_editar.grid(row=6, column=0, sticky=W + E)

        # 9. Botón de Eliminar Producto
        style = ttk.Style()
        style.configure('my.TButton1', font=('Calibri', 14, 'bold'))
        self.boton_eliminar = ttk.Button(frame, text='Eliminar Producto', command=self.delete_producto, style='my.TButton')
        self.boton_eliminar.grid(row=6, column=1, sticky=W + E)

        # 7. Label de mensajes de productos
        self.mensaje = Label(text='', fg='red')
        self.mensaje.grid(row=7, column=1, sticky=W + E)

        # 10. Tabla de Productos
        style = ttk.Style()

        # 11.1 Modificar la fuente de la tabla.
        style.configure('mystyle.Treeview', highlightthickness=0, bd=0, font=('Calibri', 11))

        # 11.2. Modificar fuente de las cabeceras
        style.configure('mystyle.Treeview.Heading', font=('Calibri', 13, 'bold'))

        # 11.3. Eliminar borders
        style.layout('mystyle.Treeview', [('mystyle.Treeview.treearea', {'sticky':'nswe'})])

        # 11.4 Estructura de la tabla
        self.tabla = ttk.Treeview(frame, heigh=10, columns=4, style='mystyle.Treeview')
        self.tabla['columns'] = ['Precio', 'Categoria', 'Stock']
        self.tabla.grid(row=8, column=0, columnspan=2)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)
        self.tabla.heading('Precio', text='Precio', anchor=CENTER)
        self.tabla.heading('Categoria', text='Categoria', anchor=CENTER)
        self.tabla.heading('Stock', text='Stock', anchor=CENTER)

        # 12. Añadir productos a la tabla
        productos = self.get_productos()

    def db_query(self, query, parametros = ()):
        """
        Realizar consulta en la base de datos

        Args:
            query [str] -- Consulta tipo SELECT para la base de datos.
            parametros [tuple] -- Tupla de parámetros
        """
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            resultado = cursor.execute(query, parametros)
            conn.commit()
        return resultado

    def get_productos(self):
        """
        Función que permite enviar una consulta para recibir todos los productos de la bbdd.
        """
        # 1. Eliminar valores de la tabla
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        # Consultar productos de la tabla
        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_query(query)

        productos = list()
        for fila in registros:
            productos.append({'nombre':fila[1], 'precio':fila[2], 'categoria':fila[3], 'stock':fila[4]})
            self.tabla.insert('', 0, text=fila[1], values=(fila[2], fila[3], fila[4]))

        if len(productos)>0:
            self.barplot_numero_productos(productos)

        return productos

    def validacion_nombre(self):
        """
        Comprobar que el campo de nombre no está vacío cuando se guarda el producto.
        :return:
        """
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0

    def validacion_precio(self):
        """
        Comprobar que el campo de precio no está vacío cuando se guarda el producto.
        :return:
        """
        try:
            precio_introducido_por_usuario = float(self.precio.get())
        except Exception as e:
            return False
        else:
            return precio_introducido_por_usuario !=0

    def validacion_categoria(self):
        """
        Validación campo categoría está completo.
        :return:
        """
        return len(self.categoria_usuario.get()) != 0

    def validacion_stock(self):
        """
        Validación campo stock
        :return:
        """
        try:
            precio_introducido_por_usuario = int(self.stock.get())
        except Exception as e:
            return False
        else:
            return precio_introducido_por_usuario

    def add_producto(self):
        """
        Añadir producto a la base de datos.
        :return:
        """
        self.mensaje['text'] = ''

        if self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() and self.validacion_stock():
            query = 'INSERT INTO producto VALUES(NULL, ?, ?, ?, ?)'
            parametros = (self.nombre.get(), self.precio.get(), self.categoria_usuario.get(), self.stock.get())
            productos = self.get_productos()
            print(self.nombre.get())
            print(self.precio.get())
            if self.editar:
                self.editar = False
                self.db_query(query, parametros)
                print('Producto guardado')
                productos = self.get_productos()

            else:
                if self.nombre.get() in [p['nombre'] for p in productos]:
                    error_msg = 'El producto ya existe! Escoge otro nombre'
                    print(error_msg)
                    self.mensaje['text'] = error_msg
                else:
                    self.db_query(query, parametros)
                    print('Producto guardado')
                    productos = self.get_productos()

        else:
            error_msg = 'Por favor, complete todos los campos'
            print(error_msg)
            self.mensaje['text'] = error_msg

    def delete_producto(self):
        """
        Eliminar elemento de la tabla
        """
        self.mensaje['text'] = ''
        print(self.tabla.item(self.tabla.selection()))
        nombre = self.tabla.item(self.tabla.selection())['text']
        query = 'DELETE FROM producto WHERE nombre = ?'
        self.db_query(query, (nombre,))
        productos = self.get_productos()

    def editar_producto(self):
        """
        Editar un producto de la lista.
        :return:
        """
        self.mensaje['text'] = ''
        print(self.tabla.item(self.tabla.selection()))
        nombre = self.tabla.item(self.tabla.selection())['text']
        if nombre == '':
            self.mensaje['text'] = 'Debe seleccionar un producto de la lista para editar'

        elif self.validacion_nombre() and self.validacion_precio() and self.validacion_stock() and self.validacion_categoria():
            query = 'DELETE FROM producto WHERE nombre = ?'
            print('eliminar producto',nombre)
            self.db_query(query, (nombre,))
            self.editar = True
            self.add_producto()
        else:
            error_msg = f'Debe completar un campo para modificar el producto {nombre} al del nombre.'
            print(error_msg)
            self.mensaje['text'] = error_msg

        productos = self.get_productos()

    def barplot_numero_productos(self, productos):
        """
        Barplot representando el número de productos por tipo categoría
        """

        frame = LabelFrame(self.ventana)
        frame.grid(row=8, column=0, columnspan=3, pady=10)

        # Countplot número productos por categoria
        fig, (ax1, ax2)  = plt.subplots(nrows=1, ncols=2, figsize=(6,2))
        countplot_productos = FigureCanvasTkAgg(fig, frame)
        countplot_productos.get_tk_widget().grid(row=0, column=3)

        productos_df = pd.DataFrame(productos)
        productos_df['coste'] = productos_df['precio'] * productos_df['stock']

        # Pie df
        pie_df = productos_df.groupby('categoria')[['stock']].sum()
        pie_df['stock_pct'] = pie_df['stock']/productos_df['stock'].sum(axis=0)
        labels = pie_df.index.tolist()
        _ = ax1.pie(x=pie_df['stock_pct'], labels=labels, autopct='%1.1f%%', textprops={'fontsize':6})
        _ = ax1.set_title('Productos en stock por categoría',weight='bold',fontsize=6)
        _ = ax1.set_xlabel('')
        _ = ax1.set_ylabel('')

        # Barplot
        barplot_df = productos_df.groupby('categoria')[['coste']].sum().sort_values('coste')
        _ = sns.barplot(data=barplot_df, x=barplot_df.index,y='coste', order=barplot_df.index,ax=ax2)
        _ = ax2.set_title('Precio de productos por categoría',weight='bold',fontsize=6)
        _ = ax2.set_xlabel('')
        _ = ax2.set_ylabel('')
        _ = ax2.tick_params(axis='x', labelsize=4)
        _ = ax2.tick_params(axis='y', labelsize=4)

        plt.tight_layout()
        plt.close(fig)
