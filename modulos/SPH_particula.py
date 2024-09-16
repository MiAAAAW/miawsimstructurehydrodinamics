
import numpy as np
import scipy.integrate as itg

#----------------------------------------- Constantes
g =  9.81             # gravedad
rho0 = 1.0            # densidad base
mu = 0.0020           # factor de viscosidad
K = 10                # factor de presión
K_CERCANA = K*2       # factor de presión cercana a la partícula
R = 4
n = 15

# Funciones utilizadas por ODEint
def RFD(v, t, F, m):
    [Fx, Fy] = F
    [vx, vy] = v
    dvdt = [Fx/m, Fy/m]
    return dvdt

def base_int(y, t, v):
    [vx, vy] = v
    dydt = [vx, vy]
    return dydt

#-----------------------------------------  Clase que define las partículas
class Particula():
    '''La clase permite crear partículas, con sus características propias, que se actualizan durante la animación'''
    
    def __init__(self, radio, masa, posicion, velocidad, tamano):
        '''Inicializa los parámetros principales de la partícula'''
        
        # Características principales
        self.tamano = tamano
        self.masa = masa
        self.radio = radio
        self.vecindario = []
        
        self.posicion = np.array(posicion) 
        self.velocidad = np.array(velocidad)
        self.fuerza = np.array([0, -self.masa*g])

        # Densidad y presión
        self.rho = 0.0
        self.rho_cercana = 0.0
        self.presion = 0.0
        self.presion_cercana = 0.0
        
        # Almacenamiento de posiciones y velocidades durante la simulación
        self.todas_posiciones = [np.copy(self.posicion)]
        self.todas_velocidades = [np.copy(self.velocidad)]
        self.todas_fuerzas = [np.copy(self.fuerza)]
        self.norma_velocidad = [np.linalg.norm(np.copy(self.velocidad))]

    def actualizar_vecindario(self, particula):
        '''Permite agregar una partícula al vecindario si están lo suficientemente cerca'''
        d = np.linalg.norm(self.posicion - particula.posicion)
        R = self.radio + particula.radio
        if d < R and d != 0:
            self.vecindario.append(particula)

    def actualizar_particula(self, dt):
        '''Función de actualización de la partícula'''
        
        # Actualización de la velocidad, según RFD: mdv/dt = F
        [vx, vy] = self.velocidad
        [Fx, Fy] = self.fuerza
        m = self.masa
        sol = np.transpose(itg.odeint(RFD, [vx, vy], t=[0, dt], args=([Fx, Fy], m)))
        self.velocidad = np.array([sol[0, 1], sol[1, 1]])
        
        # Actualización de la posición, por derivación: dx/dt = v
        [vx, vy] = self.velocidad
        [x, y] = self.posicion
        sol2 = np.transpose(itg.odeint(base_int, [x, y], t=[0, dt], args=([vx, vy],)))
        self.posicion = np.array([sol2[0, 1], sol2[1, 1]])
        
        # Restablecimiento de la fuerza a g
        self.fuerza = np.array([0, -self.masa*g])

        # Reduce la velocidad si se vuelve demasiado alta
        if np.linalg.norm(self.velocidad) > 5.0:
            self.velocidad *= 0.5
            
        elif np.linalg.norm(self.velocidad[0]) > 4:
            self.velocidad[0] *= 0.01

        # Restricciones del suelo y las paredes
        if (self.posicion[1] - self.radio) < 0:
            self.fuerza[1] = self.masa * (abs(self.velocidad[1]) / dt)
            self.posicion[1] = self.radio
            
            if self.posicion[0] < 0:
                self.fuerza[0] = self.masa * (abs(self.velocidad[0]) / dt)

            elif self.posicion[0] > self.tamano:
                self.fuerza[0] = self.masa * (-abs(self.velocidad[0]) / dt)
                
        if self.posicion[0] - self.radio < 0:
            self.fuerza[0] = self.masa * (abs(self.velocidad[0]) / dt)
            
        elif self.posicion[0] + self.radio > self.tamano:
            self.fuerza[0] = self.masa * (-abs(self.velocidad[0]) / dt)
        
        # Reducción de la velocidad en las capas bajas
        for i in range(n):
            if self.posicion[1] <= self.radio + i and self.posicion[1] >= self.radio + i - 1:
                if self.velocidad[0] > 0:
                    self.velocidad[0] -= (1 - i/n) * self.velocidad[0]
                elif self.velocidad[0] < 0:
                    self.velocidad[0] -= (1 - i/n) * self.velocidad[0]
                    
        # Actualización de todas las posiciones
        self.todas_posiciones.append(np.copy(self.posicion)) 
        self.todas_velocidades.append(np.copy(self.velocidad)) 
        self.norma_velocidad.append(np.linalg.norm(np.copy(self.velocidad))) 

        # Reinicio de la densidad, presión y vecindario
        self.rho = 0.0
        self.rho_cercana = 0.0
        self.presion = 0.0
        self.presion_cercana = 0.0
        self.vecindario = []
        
    def calcular_presion(self):
        '''Cálculo de la presión propia de la partícula'''
        
        self.presion = K * (self.rho - rho0)
        self.presion_cercana = K_CERCANA * self.rho_cercana
