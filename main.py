# Librerías y dependencias
from tkinter import ttk
from tkinter import *
import sqlite3
from src.objects import Producto


if __name__ == '__main__':
    # Instancia de la ventana principal
    root = Tk()
    # root.iconphot(False, PhotoImage(file='img/M6_P2_icon.ico')) # Para Mac.

    # Clase que define la aplicación
    app = Producto(root)
    root.mainloop()
