import tkinter as tk
from tkinter import messagebox
import modulos.SPH as SPH
import modulos.Vortex as Vortex  # Importamos el módulo del vórtice

class Interfaz(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configuración de la ventana principal
        self.title("Simulación SPH y Vórtices")
        self.geometry("1300x800")
        self.resizable(False, False)

        # Menú superior
        self.crear_menu()

        # Layout de dos columnas
        self.columnconfigure(0, weight=1)  # Columna para SPH
        self.columnconfigure(1, weight=1)  # Columna para Vórtice

        # Crear el frame para la simulación SPH y Vortex
        self.frame_sph = tk.Frame(self)
        self.frame_sph.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.frame_vortex = tk.Frame(self)
        self.frame_vortex.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Inicializar las simulaciones
        self.app_sph = SPH.SPH(self.frame_sph)  # El módulo SPH se encarga de sus propios botones
        self.app_vortex = Vortex.Vortex(self.frame_vortex)  # El módulo Vortex se encargará de su simulación

    def crear_menu(self):
        """Crear el menú superior."""
        barra_menu = tk.Menu(self)
        menu_archivo = tk.Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label="Salir", command=self.quit)
        barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

        menu_ayuda = tk.Menu(barra_menu, tearoff=0)
        menu_ayuda.add_command(label="Ayuda", command=self.ayuda_sph)
        barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

        self.config(menu=barra_menu)

    def iniciar_simulaciones(self):
        """Iniciar las simulaciones de SPH y Vórtices."""
        self.app_sph.iniciar_simulacion()  # Iniciar simulación en SPH
        self.app_vortex.iniciar_simulacion()  # Iniciar simulación en Vortex

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
            "Versión: 3.2.2\n"
            "Fecha de lanzamiento: SEPTIEMBRE 2024\n\n"
            "Desarrollado por:\n"
            "MIAW"
            "Descripción:\n"
            "SPHMODELX es una aplicación diseñada para simular el comportamiento de fluidos y su interacción con estructuras sólidas utilizando el método SPH. Ideal para estudiantes, investigadores y profesionales en los campos de la física, ingeniería y animación por computadora.\n\n"
            "Este software es de código abierto \n\n"
            "Contacto:\n"
        )
        messagebox.showinfo("Acerca de", texto_acerca_de)

    
if __name__ == "__main__":
    interfaz = Interfaz()
    interfaz.mainloop()
