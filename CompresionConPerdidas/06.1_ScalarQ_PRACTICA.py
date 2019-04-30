# -*- coding: utf-8 -*-

from scipy import misc
import numpy as np
import matplotlib.pyplot as plt


import scipy.ndimage
from scipy.cluster.vq import vq, kmeans

#%%
imagen = misc.ascent()#Leo la imagen
(n,m)=imagen.shape # filas y columnas de la imagen
plt.imshow(imagen, cmap=plt.cm.gray) 
plt.xticks([])
plt.yticks([])
#plt.show() 
        
"""
Mostrar la imagen habiendo cuantizado los valores de los píxeles en
2**k niveles, k=1..8

Para cada cuantización dar la ratio de compresión y Sigma

Sigma=np.sqrt(sum(sum((imagenOriginal-imagenCuantizada)**2)))/(n*m)

"""

def cuantizacionPixel (imagen, niveles = [1,2,3,4,5,6,7,8]):
    print('CUANTIZACION POR PIXEL')

    for k in niveles:
        shift = 2 ** (8 - k + 1)
        imageCopy = imagen.copy()
        imageCopy = [[np.round(j /shift) for j in i] for i in imageCopy]
        """
        for j in range(len(imageCopy)):
            for i in range(len(imageCopy[j])):
                imageCopy[i][j] = np.round(imageCopy[i][j] / shift);
        """
        ## Sigma y RC
        sigma = np.sqrt(sum(sum((imagen-imageCopy)**2)))/(n*m)
        ratioCompresion = 8 / k
        print('Nivel ' + str(k))
        print('Sigma: ' + str(sigma))
        print('Ratio de compresion: ' + str(ratioCompresion))
        print()

        ## Mostrar imagen
        plt.imshow(imageCopy, cmap=plt.cm.gray)
        #plt.show()

#%%
"""
Mostrar la imagen cuantizando los valores de los pixeles de cada bloque
n_bloque x n_bloque en 2^k niveles, siendo n_bloque=8 y k=2

Calcular Sigma y la ratio de compresión (para cada bloque 
es necesario guardar 16 bits extra para los valores máximos 
y mínimos del bloque, esto supone 16/n_bloque**2 bits más por pixel).
"""

def pasarABloques(image, rows, cols):
    blockImage = np.zeros((int(rows * cols / 64), 8, 8))
    block = 0
    for i in range(int(cols / 8)):
        for j in range(int(rows / 8)):
            blockImage[block] = np.reshape(image[j*8:j*8+8, i*8:i*8+8], [8,8])
            block += 1
    return blockImage

def pasarDeBloques(blockImage, rows, cols):
    img = np.zeros((rows, cols))
    z = 0
    for i in range(int(cols / 8)):
        for j in range(int(rows / 8)):
            img[j*8:j*8+8, i*8:i*8+8] = blockImage[z]
            z += 1
    return img

def cuantizacionBloques (imagen, n_bloque=8, k=2):
    imagenCopy = imagen.copy()
    imagenBlocks = pasarABloques(imagenCopy, len(imagen), len(imagen[0]))
    n_bloques = len(imagenBlocks)
	
    ## Cuantificación
    for i in range(len(imagenBlocks)):
        maximo = np.max(imagenBlocks[i])
        minimo = np.min(imagenBlocks[i])
        q = np.floor((maximo - minimo) / (2**k))
        if q != 0 :
            imagenBlocks[i] = np.floor(imagenBlocks[i] - minimo) / q
            imagenBlocks[i]= np.round((imagenBlocks[i] + 0.5 ) * q) + minimo
    imagenCuantizada = pasarDeBloques(imagenBlocks, len(imagen), len(imagen[0]))

    ## Sigma y RC
    n_pixeles = len(imagen) * len(imagen[0])
    tamanyo_compr = n_pixeles * k + n_bloques * 8 * 2
    sigma = np.sqrt(sum(sum((imagenCopy - imagenCuantizada)**2))) / (n * m)
    ratio_compresion = n_pixeles * 8 / tamanyo_compr
    print('CUANTIZACION POR BLOQUE')
    print('Sigma: ' + str(sigma))
    print('Ratio de compresion: ' + str(ratio_compresion))
    print()

    ## Mostrar imagen
    plt.imshow(imagenCuantizada, cmap=plt.cm.gray)
    #plt.show()


"""
MAIN
"""
cuantizacionPixel(imagen)
cuantizacionBloques(imagen)