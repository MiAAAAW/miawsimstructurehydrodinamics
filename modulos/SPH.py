import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.ttk as ttk
import datetime
from tkinter import messagebox

# Módulos gráficos
import matplotlib as mpl
mpl.rcParams['path.simplify'] = True
mpl.rcParams['path.simplify_threshold'] = 1
import matplotlib.style as mplstyle
mplstyle.use(['dark_background', 'fast'])
save_count = 60

# Módulos específicos
from modulos.SPH_particula import *
from modulos.SPH_funciones import *
from matplotlib.animation import PillowWriter
from tkinter import messagebox, PhotoImage
import shutil

class SPH():
    #----------------------------------------- Constantes de clase (modificables)
    g = 9.81             # gravedad
    rho0 = 1.0            # densidad base
    mu = 0.0020           # factor de viscosidad
    K = 10                # factor de presión
    K_CERCANA = K * 2     # factor de presión cerca de la partícula
    n = 15
    R1, M, T = 3.5, 0.85, 90

    def __init__(self, master)-> None: 
        self.master = master
        self.NOM_APPLI = "SPHMODELX"
        self.anim = None
        self.configurar_ventana(master)
        self.crear_widgets()

    def configurar_ventana(self, master):
        self.root = master
        self.root.configure(bg="black")

    def crear_widgets(self):
        self.crear_ventana_parametros()
        self.crear_figura()
        self.crear_ventana_simulacion()

    def crear_figura(self):
        # Vamos a crear la figura
        if not hasattr(self, 'fig'):
            self.fig = plt.Figure(figsize=(5, 5), dpi=100)
            self.ax = self.fig.add_subplot(111)

        self.lista_particulas = self.generar_lista_particulas()
        N = len(self.lista_particulas)
        radio = 4.85
        tamaño = 100
        x0, y0 = [self.lista_particulas[i].todas_posiciones[0][0] for i in range(N)], [self.lista_particulas[i].todas_posiciones[0][1] for i in range(N)]
        self.puntos = self.ax.scatter(x0, y0, s=50 * 2 ** (radio), alpha=0.90)
        self.ax.set_xlim(0, tamaño)
        self.ax.set_ylim(radio, tamaño / 1.5)
        self.ax.set_aspect('equal')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')

    def crear_ventana_parametros(self):
        # Crear una ventana de parámetros
        self.frame_parametros = tk.Frame(self.root, bg="white")
        self.frame_parametros.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Primer parámetro: número de partículas
        self.etiqueta_num_part = tk.Label(self.frame_parametros, text="Número de partículas")
        self.etiqueta_num_part.grid(row=0, column=0)
        self.entrada_num_part = tk.Entry(self.frame_parametros, width=10)
        self.entrada_num_part.insert(0, "120")
        self.entrada_num_part.grid(row=0, column=1)

        # Cuarto parámetro: número de iteraciones
        self.etiqueta_num_iter = tk.Label(self.frame_parametros, text="Número de iteraciones")
        self.etiqueta_num_iter.grid(row=1, column=0)
        self.entrada_num_iter = tk.Entry(self.frame_parametros, width=10)
        self.entrada_num_iter.insert(0, "250")
        self.entrada_num_iter.grid(row=1, column=1)

        # Botón para iniciar la simulación
        self.boton_iniciar = tk.Button(self.frame_parametros, text="Iniciar simulación", command=self.iniciar_simulacion)
        self.boton_iniciar.grid(row=4, column=0, columnspan=2)

        # Botón para guardar la simulación
        self.boton_guardar = tk.Button(self.frame_parametros, text="Guardar", command=self.guardar_simulacion)
        self.boton_guardar.grid(row=5, column=0, columnspan=2)

        # Barra de progreso
        self.barra_progreso = ttk.Progressbar(self.frame_parametros, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.barra_progreso.grid(row=6, column=0, columnspan=2)
        self.barra_progreso['value'] = 0

    def guardar_simulacion(self):
        # Guardar la simulación
        N = int(self.entrada_num_part.get())
        num_iteraciones = int(self.entrada_num_iter.get())

        # Crear el nombre del archivo
        nombre_archivo = "SPH_"
        nombre_archivo += str(N) + "_"
        nombre_archivo += str(num_iteraciones) + "_"
        nombre_archivo += str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        nombre_archivo += ".gif"

        # Verificar si ya se ha lanzado una simulación
        if self.anim is None:
            messagebox.showerror("Error", "Aún no has iniciado ninguna simulación")
            return

        # Usar Pillow para guardar la animación
        writer = PillowWriter(fps=60)
        self.anim.save(nombre_archivo, writer=writer)
        messagebox.showinfo("Guardar", f"Simulación guardada como {nombre_archivo}")

    #-------------------------------------------------------- Funciones de generación de partículas y propiedades
    def generar_lista_particulas(self):
        '''Creación de listas de partículas con estados iniciales aleatorios'''
        N = int(self.entrada_num_part.get())
        tamaño = 90
        radio = 4.85
        masa = 0.85

        lista_particulas = []
        for i in range(N):
            pos = radio + np.random.rand(2) * (tamaño / 1.3 - 2 * radio)
            v = np.random.rand(2) * 1
            lista_particulas.append(Particula(radio, masa, pos, v, tamaño))
        return lista_particulas

    def actualizar_todo(self, lista_particulas, dt):
        '''Función que actualiza el estado del sistema después de un tiempo dt'''

        # Actualización de las partículas
        for particula in lista_particulas:
            particula.actualizar_particula(dt)

        # Actualización de los vecindarios
        for particula in lista_particulas:
            for particula_b in lista_particulas:
                particula.actualizar_vecindario(particula_b)

        # Cálculo de la densidad
        func_dens(lista_particulas)

        # Cálculo de la presión
        for particula in lista_particulas:
            particula.calcular_presion()

        # Aplicación de las fuerzas de presión y viscosidad
        func_presion_visc(lista_particulas)

    def iniciar_simulacion(self):
        # Iniciar la simulación
        self.boton_iniciar["state"] = "disabled"
        self.boton_guardar["state"] = "disabled"
        self.N = int(self.entrada_num_part.get())
        self.tamaño = 100
        self.num_iteraciones = int(self.entrada_num_iter.get())
        self.radio = 4.85
        self.masa = 0.85

        # Si la simulación ya está lanzada, detenerla
        if self.anim is not None:
            self.anim.event_source.stop()
            self.anim._stop()
            self.anim = None
        self.ax.clear()
        self.crear_figura()

        # Crear lista de partículas
        dt = 0.15
        self.frames = []
        for i in range(self.num_iteraciones):
            self.frames.append(self.lista_particulas)
            self.actualizar_todo(self.lista_particulas, dt)
            self.barra_progreso["value"] = i / self.num_iteraciones * 100
            self.root.update()
            if i % 40 == 0:
                print("Iteración número ", i, "...")
        print("Fin de la simulación")

        # Actualización de partículas
        self.anim = FuncAnimation(self.fig, self.actualizar, frames=int(self.entrada_num_iter.get()), interval=15)
        self.canvas_simulacion.draw()
        self.boton_iniciar["state"] = "normal"
        self.boton_guardar["state"] = "normal"

    def actualizar(self, i):
        global lista_particulas
        dt = 0.15

        self.lista_particulas = self.frames[i]
        N = len(self.lista_particulas)
        # Actualización del scatter plot (posición de las partículas)
        x = [self.lista_particulas[j].todas_posiciones[i][0] for j in range(N)]
        y = [self.lista_particulas[j].todas_posiciones[i][1] for j in range(N)]
        self.puntos.set_offsets(np.transpose([x, y]))
        self.puntos.set_color((0, 2.5 / 4, 1))
        self.canvas_simulacion.draw()
        self.root.update()
        return self.puntos,

    def crear_ventana_simulacion(self):
        # Crear la ventana de simulación, usando matplotlib, por lo que crearemos un canvas especial
        self.frame_simulacion = tk.Frame(self.root)
        self.frame_simulacion.grid(row=0, column=0)

        self.canvas_simulacion = FigureCanvasTkAgg(self.fig, master=self.frame_simulacion)  # Un área de dibujo en tk.
        self.canvas_simulacion.draw()
        self.canvas_simulacion.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def run(self):
        # Correr el mainloop de tkinter para la simulación SPH
        self.root.mainloop()
