# -*- coding: utf-8 -*-
"""

"""

from scipy import misc
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage
from scipy.cluster.vq import vq, kmeans

#%%
imagen=scipy.misc.imread('./standard_test_images/house.png')
(n,m)=imagen.shape # filas y columnas de la imagen
plt.figure()    
plt.imshow(imagen, cmap=plt.cm.gray)
plt.show()
 






#%%

def toBlocks(img,fil,col):
    blockImage= np.zeros((int(fil*col/64),8,8))
    block=0
    for i in range(int(col/8)):
        for j in range(int(fil/8)):
            blockImage[block]= np.reshape(img[j*8:j*8+8,i*8:i*8+8],[8,8])
            block+=1
    return blockImage


def fromBlocks(blockImage,fil,col):
    img = np.array([np.array([None]*col) for i in range(fil)])
    z=0
    for i in range(int(col/8)):
        for j in range(int(fil/8)):
            img[j*8:j*8+8,i*8:i*8+8] = blockImage[z]
            z+=1
    return img

"""
Usando K-means http://docs.scipy.org/doc/scipy/reference/cluster.vq.html
crear un diccionario cuyas palabras sean bloques 8x8 con 512 entradas 
para la imagen house.png.

Dibujar el resultado de codificar house.png con dicho diccionario.

Calcular el error, la ratio de compresión y el número de bits por píxel
"""


def quantizarVectorial(imagen, entradas):
	blockImage = toBlocks(imagen, len(imagen),len(imagen[0]))
	flattenedBlocks = [np.ndarray.flatten(np.array(i)) for i in blockImage]
	flattenedBlocks = [[float(i) for i in row] for row in flattenedBlocks]
	#3r parametro num iteraciones
	means, _ = kmeans(flattenedBlocks, entradas)

	intmeans= []
	for i in range(len(means)):
		intmeans.append([])
		for j in means[i]:
			intmeans[i].append(int(j))
	referenced_image,_ = vq(flattenedBlocks,means)
	return referenced_image,intmeans

blockSize= 8
numEntradas=512
pixelBits=8
houseVec,kvalues =quantizarVectorial(imagen,numEntradas)
houseVec= [np.reshape(kvalues[i],[blockSize,blockSize]) for i in houseVec]
houseVec= [[list(row)for row in block]for block in houseVec]
houserecuperado = fromBlocks(houseVec,len(imagen),len(imagen[0]))

#error
sigma1 = np.sqrt(sum(sum((imagen-houserecuperado)**2))/(n*m))
print('error house: ' + str(sigma1))
#rati compresion
imgSize = len(imagen[0]) * len(imagen) *pixelBits
numBlocks = len(imagen[0]) * len(imagen) / (blockSize**2)
#los valores necesitaran un numero de bits proporcional al numero de entradas
encodedImageSize =  numBlocks * math.ceil(math.log(numEntradas,2))
#un bloque a guardar por entrada, cada bloque ocupa blockSize**2 pixeles
dictSize= numEntradas * (blockSize**2) *pixelBits
recoveredImgSize = encodedImageSize + dictSize
ratio_compresion = imgSize / recoveredImgSize
print('ratio compresion lena: ' + str(ratio_compresion))
bitsxPixel= recoveredImgSize / (len(imagen[0]) * len(imagen))
print('bitsxPixel lena: ' + str(bitsxPixel))
plt.imshow(houserecuperado.astype(np.uint8), cmap=plt.cm.gray)
plt.show()

print('---------------')
"""
Hacer lo mismo con la imagen cameraman.png

https://atenea.upc.edu/mod/folder/view.php?id=1833385
http://www.imageprocessingplace.com/downloads_V3/root_downloads/image_databases/standard_test_images.zip
"""


"""
Dibujar el resultado de codificar cameraman.png con el diccionarios obtenido
con la imagen house.png

Calcular el error.
"""



