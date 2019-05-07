# -*- coding: utf-8 -*-


########################################################

import numpy as np
import matplotlib.pyplot as plt


"""
Implementar una funcion H_WH(N) que devuelva la matriz NxN asociada a la transformación de Walsh-Hadamard

H_WH(4)=
      [[ 0.5,  0.5,  0.5,  0.5],
       [ 0.5,  0.5, -0.5, -0.5],
       [ 0.5, -0.5, -0.5,  0.5],
       [ 0.5, -0.5,  0.5, -0.5]]
"""

def H_WH(N):


"""
Implementar la DWHT (Discrete Walsh-Hadamard Transform) y su inversa
para bloques NxN

dwht_bloque(p) 
idwht_bloque(p) 

p bloque NxN

dwht_bloque(
            [[217,   8, 248, 199],
             [215, 189, 242,  10],
             [200,  65, 191,  92],
             [174, 239, 237, 118]]
            )=
            [[ 661,   -7.5, -48.5, 201],
             [   3,  -27.5,  25.5,  57],
             [  59,  -74.5,  36.5, -45],
             [ -51, -112.5, 146.5,  45]]

"""



def dwht_bloque(p):
      b = p.transpose
      y = np.tensordot (b,p,0)
      return y


def idwht_bloque(p):
      if (np.linalg.det(p)) != 0.0 :
            B = np.linalg.inv(p)
      return B




Q = np.array([
      [217,   8, 248, 199],
      [215, 189, 242,  10],
      [200,  65, 191,  92],
      [174, 239, 237, 118]
      ])

print(dwht_bloque(Q))







def determinante(A):
    # Copia CORRECTA de la matriz A en la de B.
    B = [k[:] for k in A]
    n = len(A)
    suma = 0.0
    if n > 2: # Si el rango es mayor que 2
        for i in range(n):
            factor = B[0][i] # saca el factor de la primera fila i
            signo = -2 * (i % 2) + 1 # calcula su signo
            B.remove(B[0]) # Borra la primera fila
            for j in range(0, n - 1):
                # B[j].remove(B[j][i]). NO SE PUEDE PONER REMOVE porque lo que quita es el elemento de la primera posición
                B[j].pop(i) # Quita, de cada fila de B, el factor i, o sea, quita esa columna.
            suma = suma + factor * signo * determinante(B) # El determinante es la suma anterior más lo que calcule
            B = [k[:] for k in A] # reconstruye la matriz B
        return suma # retorna la suma
    else:
        return (B[0][0] * B[1][1]) - (B[0][1] * B[1][0]) # devuelve el determinante del rango 2


"""
Reproducir los bloques base de la transformación para los casos N=4,8,16
Ver imágenes adjuntas
"""


