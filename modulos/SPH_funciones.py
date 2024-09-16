
import numpy as np
from modulos.SPH_particula import*

#--------------------------------------------------------Funciones de densidad, presión y viscosidad
def func_dens(lista_particulas):
    '''Función que calcula la densidad de una partícula en el vecindario de cada partícula'''
    
    for particula in lista_particulas:
        densidad = 0.0
        densidad_cercana = 0.0
        for particula_b in particula.vecindario:
            d = np.linalg.norm(particula.posicion - particula_b.posicion) # Distancia entre las partículas
            R = (particula.radio + particula_b.radio) / 1.5
            d_norm = 1 - d / R # Normalización y adimensionalización
            
            if d < R:
                # Definimos una densidad y una densidad cercana
                densidad += d_norm**2
                densidad_cercana += d_norm**3
                particula_b.rho += d_norm**2
                particula_b.rho_cercana += d_norm**3
        
        particula.rho += densidad
        particula.rho_cercana += densidad_cercana
                
def func_presion_visc(lista_particulas):
    '''Función que calcula las fuerzas de presión y viscosidad que experimenta cada partícula en su vecindario'''
    
    for particula in lista_particulas:
        for particula_b in particula.vecindario:

            d = np.linalg.norm(particula.posicion - particula_b.posicion)
            R = (particula.radio + particula_b.radio) / 1.5
            
            # Cálculo de las fuerzas de presión normalizadas
            d_norm = 1 - d / R
            ptot = (particula.presion + particula_b.presion) * d_norm**2 + (particula.presion_cercana + particula_b.presion_cercana) * d_norm**3
            pvect = (particula_b.posicion - particula.posicion) * ptot / d
            pvect[np.isnan(pvect[0])] = np.array([0,0])
            particula_b.fuerza += pvect / 2
            particula.fuerza -= pvect / 2

            diff_pos = particula_b.posicion - particula.posicion
            norm_pos = diff_pos / d
            d_relativa = d / R
            if norm_pos[0] != 0 and norm_pos[1] != 0:
                diff_v = (particula.velocidad[0] - particula_b.velocidad[0]) / norm_pos[0] + (particula.velocidad[1] - particula_b.velocidad[1]) / norm_pos[1] 

            elif norm_pos[0] == 0 and norm_pos[1] != 0:
                diff_v = (particula.velocidad[1] - particula_b.velocidad[1]) / norm_pos[1]

            elif norm_pos[0] != 0 and norm_pos[1] == 0:
                diff_v = (particula.velocidad[0] - particula_b.velocidad[0]) / norm_pos[0]
            
            elif norm_pos == [0,0]:
                diff_v = 0


            # Cálculo de las fuerzas de viscosidad normalizadas
            if diff_v >= 0 and particula.posicion[1] > R and particula_b.posicion[1] > R:
                fuerza_viscosidad = (1 - d_relativa) * mu * diff_v * norm_pos
                particula.velocidad -= fuerza_viscosidad
                particula_b.velocidad += fuerza_viscosidad
