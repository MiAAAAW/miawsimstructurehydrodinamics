import tkinter as tk
from tkinter import messagebox
import modules.SPH as SPH

class Interface(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Creamos el menú
        self.create_menu()

        # Iniciar SPH por defecto
        self.switch_sph()

    def create_menu(self):
        # Menú para la aplicación
        self.menu_bar = tk.Menu(self)

        # Menú de archivo con opción para salir
        sph_menu = tk.Menu(self.menu_bar, tearoff=0)
        sph_menu.add_command(label="Salir", command=self.quit)
        self.menu_bar.add_cascade(label="Archivo", menu=sph_menu)

        # Menú de ayuda
        ayuda_menu = tk.Menu(self.menu_bar, tearoff=0)
        ayuda_menu.add_command(label="Ayuda", command=self.ayuda_sph)
        ayuda_menu.add_command(label="Acerca de", command=self.acerca_de)
        self.menu_bar.add_cascade(label="Ayuda", menu=ayuda_menu)

        self.config(menu=self.menu_bar)

    def ayuda_sph(self):
        ayuda_texto = (
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
        messagebox.showinfo("Ayuda SPHMODELX", ayuda_texto)

    def acerca_de(self):
        acerca_de_texto = (
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
        messagebox.showinfo("Acerca de", acerca_de_texto)

    def switch_sph(self):
        # Iniciar SPH
        print("Cambiando a SPHMODELX")
        self.app = SPH.SPH(self)
        self.app.run()

if __name__ == "__main__":
    interface = Interface()