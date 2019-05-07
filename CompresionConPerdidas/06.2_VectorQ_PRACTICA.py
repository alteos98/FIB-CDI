# -*- coding: utf-8 -*-
"""

"""

from scipy import misc
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage
import math
from scipy.cluster.vq import vq, kmeans

#%%
imagen=scipy.misc.imread('/Users/ariadna/Desktop/FIB-CDI-1/CompresionConPerdidas/standard_test_images/house.png')
(n,m)=imagen.shape # filas y columnas de la imagen
plt.figure()    
plt.imshow(imagen, cmap=plt.cm.gray)
plt.show()
 

#%%
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

"""
Usando K-means http://docs.scipy.org/doc/scipy/reference/cluster.vq.html
crear un diccionario cuyas palabras sean bloques 8x8 con 512 entradas 
para la imagen house.png.

Dibujar el resultado de codificar house.png con dicho diccionario.

Calcular el error, la ratio de compresión y el número de bits por píxel
"""


def quantizarVectorial(imagen, entradas):
	blockImage = pasarABloques(imagen, len(imagen),len(imagen[0]))
	bloque = [np.ndarray.flatten(np.array(i)) for i in blockImage]
	bloque = [[float(i) for i in row] for row in bloque]
	means, _ = kmeans(bloque, entradas)
	intmeans= []
	for i in range(len(means)):
		intmeans.append([])
		for j in means[i]:
			intmeans[i].append(int(j))
	imagen_rec,_ = vq(bloque,means)
	return imagen_rec,intmeans

sizeBloque= 8
numEntradas=512
pixelBits=8
houseVec,housekvalues =quantizarVectorial(imagen,numEntradas)
houseVec= [np.reshape(housekvalues[i],[sizeBloque,sizeBloque]) for i in houseVec]
houseVec= [[list(row)for row in block]for block in houseVec]
houserecuperado = pasarDeBloques(houseVec,len(imagen),len(imagen[0]))

#calculo del error 
sigmahouse = np.sqrt(sum(sum((imagen-houserecuperado)**2))/(n*m))
print('error house: ' + str(sigmahouse))

#ratio compresion 
ImgSizehouse = len(imagen[0]) * len(imagen) *pixelBits
numBloquesHouse= len(imagen[0]) * len(imagen) / (sizeBloque**2)
dicthouse_size= numEntradas * (sizeBloque**2) * pixelBits
e_imgsizehouse =  numBloquesHouse * math.ceil(math.log(numEntradas,2))
imgsizehouse_rec = e_imgsizehouse + dicthouse_size
ratiocompresion_house = ImgSizehouse / imgsizehouse_rec
print('ratio compresion house: ' + str(ratiocompresion_house))

#bits por pixel
bitsPixel= imgsizehouse_rec / (len(imagen[0]) * len(imagen))
print('bits por pixel house: ' + str(bitsPixel))

#imagen recuperada
plt.imshow(houserecuperado.astype(np.uint8), cmap=plt.cm.gray)
plt.show()

"""
Hacer lo mismo con la imagen cameraman.png

https://atenea.upc.edu/mod/folder/view.php?id=1833385
http://www.imageprocessingplace.com/downloads_V3/root_downloads/image_databases/standard_test_images.zip
"""
#valores diccionario
sizeBloque= 8
numEntradas=512
pixelBits=8

#carga imagen
imagencamera=scipy.misc.imread('/Users/ariadna/Desktop/FIB-CDI-1/CompresionConPerdidas/standard_test_images/cameraman.png')
(n,m)=imagencamera.shape # filas y columnas de la imagen
plt.figure()    
plt.imshow(imagencamera, cmap=plt.cm.gray)
plt.show()


cameraVec,camerakvalues =quantizarVectorial(imagencamera,numEntradas)
cameraVec= [np.reshape(camerakvalues[i],[sizeBloque,sizeBloque]) for i in cameraVec]
cameraVec= [[list(row)for row in block]for block in cameraVec]
camerarecuperado = pasarDeBloques(cameraVec,len(imagencamera),len(imagencamera[0]))

#calculo del error
sigmacamera = np.sqrt(sum(sum((imagen-camerarecuperado)**2))/(n*m))
print('error cameraman: ' + str(sigmacamera))

#ratio de compresion
imgSizeCamera = len(imagencamera[0]) * len(imagencamera) *pixelBits
numBloquescamera = len(imagencamera[0]) * len(imagencamera) / (sizeBloque**2)
dictcamera_size= numEntradas * (sizeBloque**2) *pixelBits
e_imgsizecamera =  numBloquescamera * math.ceil(math.log(numEntradas,2))
imgsizecamera_rec = e_imgsizecamera + dictcamera_size
ratio_compresion = imgSizeCamera / imgsizecamera_rec
print('ratio compresion cameraman: ' + str(ratio_compresion))

#bits por pixel cameraman
bitsPixelCamera = imgsizecamera_rec / (len(imagencamera[0]) * len(imagencamera))
print('bits por pixel cameraman: ' + str(bitsPixelCamera))

#imagen recuperada
plt.imshow(camerarecuperado.astype(np.uint8), cmap=plt.cm.gray)
plt.show()

"""
Dibujar el resultado de codificar cameraman.png con el diccionarios obtenido
con la imagen house.png

Calcular el error.
"""

cameraVec = pasarABloques(imagencamera, len(imagencamera),len(imagencamera[0]))
cameraVec1 = [np.ndarray.flatten(np.array(i)) for i in cameraVec]
cameraVec1 = [[float(i) for i in row] for row in cameraVec1]

cameraVechouse,_ =vq(cameraVec1,housekvalues)
cameraVec= [np.reshape(housekvalues[i],[sizeBloque,sizeBloque]) for i in cameraVechouse]
cameraVec= [[list(row)for row in block]for block in cameraVec]
camerarecuperado = pasarDeBloques(cameraVec,len(imagencamera),len(imagencamera[0]))

#calculo del error
sigmacamera = np.sqrt(sum(sum((imagencamera-camerarecuperado)**2))/(n*m))
print('error cameraman con diccionario house: ' + str(sigmacamera))

#imagen original
plt.imshow(imagencamera, cmap=plt.cm.gray)
plt.show()

#imagen recuperada
plt.imshow(camerarecuperado.astype(np.uint8), cmap=plt.cm.gray)
plt.show()
