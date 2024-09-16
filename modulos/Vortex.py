import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

class Vortex:
    def __init__(self, frame):
        self.frame = frame
        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        
        self.ax.set_xlim(-50, 50)
        self.ax.set_ylim(-50, 50)
        self.ax.set_aspect('equal')

        # Parámetros iniciales
        self.num_particulas = 100  # Valor por defecto
        self.velocidad_expansion = 0.05
        self.velocidad_angular = 0.05

        # Inicialización de las partículas
        self.particulas = np.random.uniform(-30, 30, (self.num_particulas, 2))
        self.velocidades = np.zeros((self.num_particulas, 2))  # Inicialmente quietas

        # Agregar centro del vórtice
        self.centro_vortice = np.array([0, 0])

        # Crear los puntos de las partículas en el gráfico
        self.scatter = self.ax.scatter(self.particulas[:, 0], self.particulas[:, 1], s=10, c='blue')

        # Crear el punto central del vórtice
        self.centro_punto, = self.ax.plot(0, 0, 'ro', markersize=8)

        self.animacion = None

        # Canvas para dibujar en Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Barra de progreso
        self.progress_bar = ttk.Progressbar(self.frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progress_bar.pack(side=tk.BOTTOM)

        # Botón para iniciar simulación
        self.boton_iniciar = tk.Button(self.frame, text="Iniciar Simulación", command=self.iniciar_simulacion)
        self.boton_iniciar.pack(side=tk.BOTTOM)

        # Etiquetas e Inputs para cambiar los parámetros
        tk.Label(self.frame, text="Velocidad de Expansión:").pack(side=tk.BOTTOM)
        self.entrada_vel_expansion = tk.Entry(self.frame)
        self.entrada_vel_expansion.pack(side=tk.BOTTOM)
        self.entrada_vel_expansion.insert(0, str(self.velocidad_expansion))

        tk.Label(self.frame, text="Velocidad Angular:").pack(side=tk.BOTTOM)
        self.entrada_vel_angular = tk.Entry(self.frame)
        self.entrada_vel_angular.pack(side=tk.BOTTOM)
        self.entrada_vel_angular.insert(0, str(self.velocidad_angular))

        tk.Label(self.frame, text="Número de Partículas:").pack(side=tk.BOTTOM)
        self.entrada_num_part = tk.Entry(self.frame)
        self.entrada_num_part.pack(side=tk.BOTTOM)
        self.entrada_num_part.insert(0, str(self.num_particulas))

    def actualizar_parametros(self):
        # Actualizamos los parámetros para la simulación del vórtice desde la interfaz
        try:
            self.num_particulas = int(self.entrada_num_part.get())
            self.velocidad_expansion = float(self.entrada_vel_expansion.get())
            self.velocidad_angular = float(self.entrada_vel_angular.get())
        except ValueError:
            print("Por favor ingresa valores numéricos válidos.")
            return

        # Recalcular las partículas
        self.particulas = np.random.uniform(-30, 30, (self.num_particulas, 2))
        self.velocidades = np.zeros((self.num_particulas, 2))  # Reiniciar velocidades
        self.scatter.set_offsets(self.particulas)

    def iniciar_simulacion(self):
        self.actualizar_parametros()  # Actualizar los parámetros antes de la simulación

        if self.animacion is not None:
            self.animacion.event_source.stop()

        self.animacion = FuncAnimation(self.fig, self.actualizar, frames=200, interval=50, blit=True)
        self.canvas.draw()

    def actualizar(self, frame):
        # Actualizar barra de progreso
        self.progress_bar['value'] = (frame / 200) * 100

        # Calcular las fuerzas de expansión y rotación
        for i, particula in enumerate(self.particulas):
            # Distancia al centro del vórtice
            distancia_centro = np.linalg.norm(particula - self.centro_vortice)
            
            if distancia_centro > 0:
                # Vector hacia el centro
                vector_centro = (self.centro_vortice - particula) / distancia_centro

                # Expansión y contracción radial
                fuerza_expansion = vector_centro * self.velocidad_expansion

                # Rotación alrededor del centro del vórtice
                fuerza_rotacional = np.array([-vector_centro[1], vector_centro[0]]) * self.velocidad_angular

                # Sumar fuerzas para obtener la nueva velocidad
                self.velocidades[i] += fuerza_expansion + fuerza_rotacional

        # Mover las partículas
        self.particulas += self.velocidades * 0.5  # Ajuste del tiempo de simulación

        # Actualizar los datos de las partículas en el gráfico
        self.scatter.set_offsets(self.particulas)
        return self.scatter,
