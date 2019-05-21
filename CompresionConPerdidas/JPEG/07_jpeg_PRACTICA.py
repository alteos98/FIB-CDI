# -*- coding: utf-8 -*-

import numpy as np
import scipy
import scipy.ndimage
import math
from scipy.fftpack import dct, idct
pi=math.pi

import matplotlib.pyplot as plt
import time
       
"""
Matrices de cuantización, estándares y otras
"""

    
Q_Luminance=np.array([
[16 ,11, 10, 16,  24,  40,  51,  61],
[12, 12, 14, 19,  26,  58,  60,  55],
[14, 13, 16, 24,  40,  57,  69,  56],
[14, 17, 22, 29,  51,  87,  80,  62],
[18, 22, 37, 56,  68, 109, 103,  77],
[24, 35, 55, 64,  81, 104, 113,  92],
[49, 64, 78, 87, 103, 121, 120, 101],
[72, 92, 95, 98, 112, 100, 103, 99]])

Q_Chrominance=np.array([
[17, 18, 24, 47, 99, 99, 99, 99],
[18, 21, 26, 66, 99, 99, 99, 99],
[24, 26, 56, 99, 99, 99, 99, 99],
[47, 66, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99]])

def Q_matrix(r=1):
    m=np.zeros((8,8))
    for i in range(8):
        for j in range(8):
            m[i,j]=(1+i+j)*r
    return m

"""
Implementar la DCT (Discrete Cosine Transform) 
y su inversa para bloques NxN

dct_bloque(p,N)
idct_bloque(p,N)

p bloque NxN

"""

def getTransform(N):
    res = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
                aux1 = np.sqrt(2/N)
                aux2 = (2*j+1)*i*pi
                aux2 /= (2*N)
                aux2 = np.cos(aux2)
                if i==0:
                    res[i,j] = aux1 * aux2 * (1/np.sqrt(2))
                else:
                    res[i,j] = aux1 * aux2
    return res

def dct_bloque(p):
    return dct(dct(p, axis = 0, norm = 'ortho'), axis = 1, norm = 'ortho')

def idct_bloque(p):
   return idct(idct(p, axis = 0, norm = 'ortho'), axis = 1, norm = 'ortho')

"""
Reproducir los bloques base de la transformación para los casos N=4,8
Ver imágenes adjuntas.
"""

N = 4
while N <= 8:
    t = getTransform(N)
    for row in range(N):
        for col in range(N):
            baseImage = np.tensordot(t[row], np.transpose(t[col]), 0)
            plt.imshow(baseImage) 
            plt.xticks([])
            plt.yticks([])
            plt.show() 
    N *= 2

"""
Implementar la función jpeg_gris(imagen_gray) que: 
1. dibuje el resultado de aplicar la DCT y la cuantización 
(y sus inversas) a la imagen de grises 'imagen_gray' 

2. haga una estimación de la ratio de compresión
según los coeficientes nulos de la transformación: 
(#coeficientes/#coeficientes no nulos).

3. haga una estimación del error
Sigma=np.sqrt(sum(sum((imagen_gray-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_gray)**2)))


"""

def adjustMatrix(originalX, originalY, imagen):
    x = originalX
    y = originalY
    if originalX % 8 != 0:
        x += 8 - (originalX % 8)
    if originalY % 8 != 0:
        y += 8 - (originalY % 8)
    res = np.zeros((x,y))
    aux1 = np.zeros((x,originalY))
    aux1[:originalX, :originalY] = imagen
    for i in range(x - originalX):
        aux1[originalX+i] = imagen[-1]
    res[:x, :originalY] = aux1
    for j in range(y - originalY):
        res[:, originalY+j] = aux1[:, -1]
    return res

def firstReshape(x, y, image):
    res = np.zeros((int((x*y)/64),8,8))
    z = 0
    for n1 in range(int(y/8)):
        for n2 in range(int(x/8)):		
            bx1=n2*8
            bx2=bx1+8
            bz1=n1*8
            bz2=bz1+8
            res[z]= image[bx1:bx2,bz1:bz2].reshape(8,8)
            z+=1
    return res

def secondReshape(x, y, image):
    res = np.zeros((x,y))
    z = 0
    for n1 in range(int(y/8)):
        for n2 in range(int(x/8)):
            bx1=n2*8
            bx2=bx1+8
            bz1=n1*8
            bz2=bz1+8
            res[bx1:bx2,bz1:bz2] = image[z]
            z+=1
    return res

def jpeg_gris(imagen_gray):
    # Paso 1

    # Ajustar el tamaño de la imagen
    # Dividir en bloques 8x8
    originalX, originalY = imagen_gray.shape
    x = originalX
    y = originalY
    imagen_reshaped = adjustMatrix(originalX, originalY, imagen_gray)
    ImageInBlocs = firstReshape(x, y, imagen_reshaped)

    # Se desplaza la imagen 128 y se aplica DCT sobre los bloques de la imagen
    ImageInBlocs -= 128
    numBloc = int((x*y)/(8*8))
    for i in range(numBloc):
        ImageInBlocs[i] = dct_bloque(ImageInBlocs[i])

    # Se cuantizan los valores de los bloques
    for i in range(numBloc):
        for w in range(8):
            for z in range(8):
                ImageInBlocs[i,w,z] /= Q_Luminance[w,z]
                ImageInBlocs[i,w,z] = round(ImageInBlocs[i,w,z],0)


    # Paso 2    
    # Ratio de compresión
    ImagenCuantizada = secondReshape(x,y,ImageInBlocs)[:originalX, :originalY]
    coef = x*y
    coefNul = (ImagenCuantizada == 0.).sum()
    CRatio = coef/(coef-coefNul)
    

    # Paso 3
    # Reversión de los cambios hechos sobre la imagen
    # Se aplica iDCT a los bloques de la imagen
    for i in range(numBloc):
        ImageInBlocs[i] = idct_bloque(ImageInBlocs[i])
        
    # Reshape de la imagen cuantizada
    x,y = imagen_reshaped.shape
    imagenInv = secondReshape(x, y, ImageInBlocs)
    
    # Eliminar las filas y columnas de más
    imagen_jpeg = imagenInv[:originalX, :originalY]
    

    # Paso 4
    # Pintar imagen
    plt.imshow(imagen_jpeg, cmap=plt.cm.gray) 
    plt.xticks([])
    plt.yticks([])
    plt.show() 
    

    # Paso 5
    # Estimación del error
    sigma = np.sqrt(sum(sum((imagen_gray-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_gray)**2)))


    # Paso 6
    # Printear datos
    print('JPEG GRIS')
    print('Estimación del error: ', sigma)
    print('Ratio de compresión:', CRatio)

    return imagen_jpeg


"""
Implementar la función jpeg_color(imagen_color) que: 
1. dibuje el resultado de aplicar la DCT y la cuantización 
(y sus inversas) a la imagen RGB 'imagen_color' 

2. haga una estimación de la ratio de compresión
según los coeficientes nulos de la transformación: 
(#coeficientes/#coeficientes no nulos).

3. haga una estimación del error para cada una de las componentes RGB
sigma=np.sqrt(sum(sum((imagen_color-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_color)**2)))

"""

def jpeg_color(imagen_color):
    # Paso 1
    # Compresión de la imagen

    # Transformación del espacio de colores
    originalX, originalY, originalZ = imagen_color.shape
    imagenY = np.zeros((originalX,originalY))
    imagenCb = np.zeros((originalX,originalY))
    imagenCr = np.zeros((originalX,originalY))
    for i in range(originalX):
        for j in range(originalY):
            R = imagen_color[i,j,0]
            G = imagen_color[i,j,1]
            B = imagen_color[i,j,2]
            Y = (75/256)*R + (150/256)*G + (29/256)*B
            Cb = -(44/256)*R - (87/256)*G + (131/256)*B + 128
            Cr = (131/256)*R - (110/256)*G - (21/256)*B + 128
            imagenY[i,j] = Y
            imagenCb[i,j] = Cb
            imagenCr[i,j] = Cr
            
    # Ajustar tamaño de la matriz, añadir filas y columnas extra
    imagenY_reshaped = adjustMatrix(originalX,originalY,imagenY)
    x, y = imagenY_reshaped.shape
    imagenY_reshaped = firstReshape(x,y,imagenY_reshaped)
    imagenCb_reshaped = adjustMatrix(originalX,originalY,imagenCb)
    imagenCb_reshaped = firstReshape(x,y,imagenCb_reshaped)
    imagenCr_reshaped = adjustMatrix(originalX,originalY,imagenCr)
    imagenCr_reshaped = firstReshape(x,y,imagenCr_reshaped)
    
    # Desplazar 128 y aplicar dct a los bloques de la imagen
    imagenY_reshaped -= 128
    imagenCb_reshaped -= 128
    imagenCr_reshaped -= 128
    numBloc = int((x*y)/(8*8))
    for i in range(numBloc):
        imagenY_reshaped[i]=dct_bloque(imagenY_reshaped[i])
        imagenCb_reshaped[i]=dct_bloque(imagenCb_reshaped[i])
        imagenCr_reshaped[i]=dct_bloque(imagenCr_reshaped[i])
    
    # Cuantización de los valores
    Q = Q_matrix()
    for i in range(numBloc):
        for w in range(8):
            for z in range(8):
                imagenY_reshaped[i,w,z] /= Q_Luminance[w,z]
                imagenY_reshaped[i,w,z] = round(imagenY_reshaped[i,w,z],0)

                imagenCb_reshaped[i,w,z] /= Q[w,z]
                imagenCb_reshaped[i,w,z] = round(imagenCb_reshaped[i,w,z],0)

                imagenCr_reshaped[i,w,z] /= Q_Chrominance[w,z]
                imagenCr_reshaped[i,w,z] = round(imagenCr_reshaped[i,w,z],0)
    

    # Paso 2
    # Calculo de la ratio de compresión aproximada
    coef = originalX*originalY*originalZ
    coefNul = (imagenY_reshaped == 0).sum() + (imagenCb_reshaped == 0).sum() + (imagenCr_reshaped ==0).sum()
    CRatio = coef/(coef-coefNul)
    

    # Paso 3
    # Proceso inverso

    # iDCT a los bloques
    for i in range(numBloc):
        imagenY_reshaped[i] = idct_bloque(imagenY_reshaped[i])
        imagenCb_reshaped[i] = idct_bloque(imagenCb_reshaped[i])
        imagenCr_reshaped[i] = idct_bloque(imagenCr_reshaped[i])
        
    # Reshape de la matriz
    imagenY_inv = secondReshape(x,y,imagenY_reshaped)
    imagenCb_inv = secondReshape(x,y,imagenCb_reshaped)
    imagenCr_inv = secondReshape(x,y,imagenCr_reshaped)
    
    # Cambio al espacio de color RGB
    imagen_jpeg = np.zeros((originalX,originalY,originalZ))
    for i in range(originalX):
        for j in range(originalY):
            Y = imagenY[i,j]
            Cb = imagenCb[i,j]
            Cr = imagenCr[i,j]
            R = Y + (1.371*(Cr-128))
            G = Y - (0.698*(Cr-128))-(0.336*(Cb-128))
            B = Y + (1.732*(Cb-128))
            imagen_jpeg[i,j,0] = R
            imagen_jpeg[i,j,1] = G
            imagen_jpeg[i,j,2] = B
            

    # Paso 4
    # Pintar imagen       
    plt.imshow(imagen_jpeg.astype(np.uint8)) 
    plt.xticks([])
    plt.yticks([])
    plt.show() 
    

    # Paso 5
    # Estimación del error
    imagen_jpeg = imagen_jpeg.astype(np.int64)
    sigma = np.sqrt(sum(sum((imagen_color-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_color)**2)))


    # Paso 6
    # Printear datos
    print('JPEG COLOR')
    print('Estimación del error: ', sigma)
    print('Ratio de compresión:', CRatio)
    
    return imagen_jpeg


"""
#--------------------------------------------------------------------------
Imagen de GRISES

#--------------------------------------------------------------------------
"""
### .astype es para que lo lea como enteros de 32 bits, si no se
### pone lo lee como entero positivo sin signo de 8 bits uint8 y por ejemplo al 
### restar 128 puede devolver un valor positivo mayor que 128

direccion_imagen_gray = 'C:/Users/alteo/Documents/GitHub/CDI/CompresionConPerdidas/JPEG/mandril_gray.png'
mandril_gray=scipy.ndimage.imread(direccion_imagen_gray).astype(np.int32)

start = time.time()
mandril_jpeg = jpeg_gris(mandril_gray)
end = time.time()
print("tiempo", (end-start))


"""
#--------------------------------------------------------------------------
Imagen COLOR
#--------------------------------------------------------------------------
"""
## Aplico.astype pero después lo convertiré a 
## uint8 para dibujar y a int64 para calcular el error

direccion_imagen_color = 'C:/Users/alteo/Documents/GitHub/CDI/CompresionConPerdidas/JPEG/mandril_color.png'
mandril_color=scipy.misc.imread(direccion_imagen_color).astype(np.int32)

start = time.time()
mandril_jpeg = jpeg_color(mandril_color)
end = time.time()
print("tiempo", (end-start))
