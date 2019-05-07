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

# número de cambios de signo en una fila
def numeroCambiosSimbolo(row):
	counter = 0
	ant = row[0]
	for x in row:
		aux = x
		if ant != aux:
			counter += 1
		ant = aux
	return counter

# dada una matriz m, se ordenan sus filas en función del número
# de cambios de signo en cada fila
def ordenarPorCambiosSigno(m):
	# inicializaciones
	N = len(m)
	m_aux = np.zeros((N, N))

	# ordenar
	for row in m:
		n_cambiosSimbolo = numeroCambiosSimbolo(row)
		m_aux[n_cambiosSimbolo] = row

	return m_aux

def H_WH(N_max):
	# inicializaciones
	hN_ant = np.array([1])
	hN_new = np.array([1])
	N = 2

	while (N <= N_max):
		# creación nueva matriz
		hN_new = np.zeros((N, N))

		# replicar la matriz para los 4 cuadrantes (cambiando de signo el último)
		n_bloque = int(N / 2)
		for row in range(int(N / n_bloque)):
			for col in range(int(N / n_bloque)):
				x_ini = col * n_bloque
				x_fi = x_ini + n_bloque
				y_ini = row * n_bloque
				y_fi = y_ini + n_bloque

				# cambiar el signo del cuarto
				if (N / n_bloque) - 1 == row and row == col:
					hN_new[x_ini:x_fi, y_ini:y_fi] = -hN_ant
				else:
					hN_new[x_ini:x_fi, y_ini:y_fi] = hN_ant

		# ordenar según los cambios de signo
		hN_new = ordenarPorCambiosSigno(hN_new)

		# actualizar matriz anterior
		hN_ant = hN_new

		# tamaño siguiente matriz NxN
		N = N * 2

	# multiplicar por 1/sqrt(N)
	hN_new = (1/np.sqrt(N / 2)) * hN_new

	return hN_new

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

#def dwht_bloque(p):




#def idwht_bloque(p):


"""
Reproducir los bloques base de la transformación para los casos N=4,8,16
Ver imágenes adjuntas
"""


