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
plt.show() 
        
"""
Mostrar la imagen habiendo cuantizado los valores de los píxeles en
2**k niveles, k=1..8

Para cada cuantización dar la ratio de compresión y Sigma

Sigma=np.sqrt(sum(sum((imagenOriginal-imagenCuantizada)**2)))/(n*m)

"""

def cuantizacionPixel (imagen, niveles = [1,2,3,4,5,6,7,8]):
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

        ## Mostrar imagen
        plt.imshow(imageCopy, cmap=plt.cm.gray)
        plt.show()

#cuantizacionPixel(imagen)
#%%
"""
Mostrar la imagen cuantizando los valores de los pixeles de cada bloque
n_bloque x n_bloque en 2^k niveles, siendo n_bloque=8 y k=2

Calcular Sigma y la ratio de compresión (para cada bloque 
es necesario guardar 16 bits extra para los valores máximos 
y mínimos del bloque, esto supone 16/n_bloque**2 bits más por pixel).
"""

def toBlocks(img,fil,col):
    blockImage= np.zeros((int(fil*col/64),8,8))
    block=0
    for i in range(int(col/8)):
        for j in range(int(fil/8)):
            blockImage[block]= np.reshape(img[j*8:j*8+8,i*8:i*8+8],[8,8])
            block+=1
    return blockImage


def fromBlocks(blockImage,fil,col):
    img = np.zeros((fil,col))
    z=0
    for i in range(int(col/8)):
        for j in range(int(fil/8)):
            img[j*8:j*8+8,i*8:i*8+8] = blockImage[z]
            z+=1
    return img


def quantizarAPixelesyBloques(imagen,n_bloque=8,k=2):
    imagenOriginal= imagen.copy()
    imagenBlocks= toBlocks(imagenOriginal,len(imagen),len(imagen[0]))
    numero_bloques = len(imagenBlocks)
	
    for i in range(len(imagenBlocks)):
        maximo= np.max(imagenBlocks[i])
        minimo= np.min(imagenBlocks[i])
        q= np.floor((maximo - minimo)/(2**k))
        if q != 0 : 
            #cuantizo a valores 0..2**k
            imagenBlocks[i] = np.floor(imagenBlocks[i]-minimo)/q
            #recupero valores 0..255
            imagenBlocks[i]= np.round((imagenBlocks[i] + 0.5 )*q) + minimo
    imagenCuantizada = fromBlocks(imagenBlocks,len(imagen),len(imagen[0]))
    valores= len(imagen)*len(imagen[0])
    tamanyo_compr= valores *k + numero_bloques*8*2#maximo y minimo bloque
    ratio_compresion =  valores*8 / tamanyo_compr
    print('ratio_compresion:' + str(ratio_compresion))
    sigma = np.sqrt(sum(sum((imagenOriginal-imagenCuantizada)**2))/(n*m))
    print('sigma:' + str(sigma))
    plt.imshow(imagenCuantizada, cmap=plt.cm.gray)
    #plt.show()
	

quantizarAPixelesyBloques(imagen)