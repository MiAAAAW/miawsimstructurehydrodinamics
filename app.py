# 

import tkinter as tk
from tkinter import messagebox
import modulos.SPH as SPH

class Interfaz(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Creamos el menú
        self.crear_menu()

        # Iniciar SPH por defecto
        self.cambiar_sph()

    def crear_menu(self):
        # Menú para la aplicación
        self.barra_menu = tk.Menu(self)

        # Menú de archivo con opción para salir
        menu_archivo = tk.Menu(self.barra_menu, tearoff=0)
        menu_archivo.add_command(label="Salir", command=self.quit)
        self.barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

        # Menú de ayuda
        menu_ayuda = tk.Menu(self.barra_menu, tearoff=0)
        menu_ayuda.add_command(label="Ayuda", command=self.ayuda_sph)
        menu_ayuda.add_command(label="Acerca de", command=self.acerca_de)
        self.barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

        self.config(menu=self.barra_menu)

    def ayuda_sph(self):
        texto_ayuda = (
            "Programa de simulación de fluidos mediante el método SPH (Smoothed-Particle Hydrodynamics).\n\n"
            "Características principales:\n"
            "- **Método sin Malla:** Permite simular grandes deformaciones y movimientos relativos sin necesidad de una malla fija.\n"
            "- **Seguimiento Lagrangiano:** Cada partícula representa una porción del fluido, facilitando el seguimiento de su trayectoria.\n"
            "- **Funciones de Suavizado:** Calcula propiedades físicas como densidad y presión utilizando partículas vecinas.\n"
            "- **Interacción Fluidos-Estructuras (FFE):** Simula de manera eficiente la interacción entre fluidos y estructuras sólidas.\n\n"
            "Aplicaciones:\n"
            "- Ingeniería Civil: Modelado de inundaciones y comportamiento de estructuras ante flujos de agua.\n"
            "- Ingeniería Aeroespacial: Análisis del flujo de aire alrededor de aeronaves.\n"
            "- Animación por Computadora: Creación de efectos realistas de líquidos.\n\n"
            "Para más información, consulte la documentación oficial o contacte al desarrollador."
        )
        messagebox.showinfo("Ayuda SPHMODELX", texto_ayuda)

    def acerca_de(self):
        texto_acerca_de = (
            "SPHMODELX - Simulación de Fluidos con Hidrodinámica de Partículas Suavizadas (SPH)\n\n"
            "Versión: 1.0.0\n"
            "Fecha de lanzamiento: Abril 2024\n\n"
            "Desarrollado por:\n"
            "- Juan Pérez\n"
            "- María López\n"
            "- Carlos Gómez\n\n"
            "Descripción:\n"
            "SPHMODELX es una aplicación diseñada para simular el comportamiento de fluidos y su interacción con estructuras sólidas utilizando el método SPH. Ideal para estudiantes, investigadores y profesionales en los campos de la física, ingeniería y animación por computadora.\n\n"
            "Licencia:\n"
            "Este software es de código abierto y está disponible bajo la licencia MIT.\n\n"
            "Contacto:\n"
            "correo@ejemplo.com\n"
            "Sitio web: www.sphmodelx.com"
        )
        messagebox.showinfo("Acerca de", texto_acerca_de)

    def cambiar_sph(self):
        # Iniciar SPH
        print("Cambiando a SPHMODELX")
        self.app = SPH.SPH(self)
        self.app.run()

if __name__ == "__main__":
    interfaz = Interfaz()
