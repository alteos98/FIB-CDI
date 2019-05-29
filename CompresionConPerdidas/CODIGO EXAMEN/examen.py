"""
from numpy import array
from numpy.linalg import inv
from math import sqrt

matriz = array([
[sqrt(3)/3, sqrt(3)/3, sqrt(3)/3],
[-sqrt(2)/2, sqrt(2)/2, 0],
[-sqrt(6)/6, -sqrt(6)/6, sqrt(6)/3]])
print(matriz)
print()
print(inv(matriz))
print()
print(matriz.transpose())
"""




import numpy as np
from scipy import misc
from math import sqrt,log
import matplotlib.pyplot as plt
import pywt

def log2(X):
	return log(X,2)

def idct_bloque(p):
    
    c = np.array([[1/(sqrt(2)),1/(sqrt(2)),0,0],
                  [1/(sqrt(2)),-1/(sqrt(2)),0,0],
                  [0,0,1/(sqrt(2)),1/(sqrt(2))],
                  [0,0,1/(sqrt(2)),-1/(sqrt(2))]])
    
    
    c1 = np.array([[0,0,0,1],
                  [0,0,1,0],
                  [0,1,0,0],
                  [1,0,0,0]])
    
    c2 = np.array([[1,0,0,0],
                  [0,1,0,0],
                  [0,0,1,0],
                  [0,0,0,1]])
    ct = np.transpose(c1)
    return (np.tensordot(np.tensordot(ct,p,axes=([1],[0])),c,axes = ([1],[0]))).reshape(-1)


fig = plt.figure()
array = np.zeros((4,4))
array = array.astype(int)
for i in range(4):
    for j in range(4):
        array[i][j] = 1
        m = idct_bloque(array)
        img = np.asarray(m)
        fig.add_subplot(4,4,i*4+j+1).axis('off')
        plt.imshow(img.reshape((4,4))) 
        plt.xticks([])
        plt.yticks([])
        #plt.show() 
        array[i][j] = 0
        
        
#%%------  
def ratio_de_compression(pixeles,escala,entradas,pixelesB):
    num = pixeles*pixeles*log2(escala)
    den = (pixeles/pixelesB)*(pixeles/pixelesB)*log2(entradas) + entradas*pixelesB*pixelesB*log2(escala)
    return num/den



print('-------------COMPRESION RATIO----------------------')
print(ratio_de_compression(1024,64,256,16))



print('-------------ORTOGONAL----------------------')
#Pregunta de Transformacion ortogonal
#%%------

matriz1 =[[(sqrt(11)/11),(sqrt(11)/11),((3*sqrt(11))/11)],
        [(sqrt(2)/2),(sqrt(2)/2),(3*sqrt(2)/2)],
        [(-3*sqrt(22))/22,(-3*sqrt(22))/22,sqrt(22)/11]]

matriz2 =[[3,1,3],
        [-1,3,0],
        [-9,-3,10]]

matriz3 =[[3,1,3],
        [6,2,6],
        [-9,-3,10]]


matriz4= [[3*sqrt(19)/19,sqrt(19)/19,3*sqrt(19)/19],
        [3*sqrt(10)/10,sqrt(10)/10,3*sqrt(10)/10],
        [-9*sqrt(190)/190,-3*sqrt(190)/190,sqrt(190)/190]]

matriz =[[3*sqrt(19)/19,sqrt(19)/19,3*sqrt(19)/19],
        [-sqrt(10)/10,3*sqrt(10)/10,0],
        [-9*sqrt(190)/190,-3*sqrt(190)/190,sqrt(190)/19]]

mat = np.asarray(matriz)
#print(np.linalg.inv(mat))
print(mat.transpose())
print(np.dot(mat,mat.transpose()))


#%%------
#Pregunta wavelet
#l = [0.2,0.8294,0.5071,-0.1223]
print("recorda +,+,+,-")
l2 = [0.28,0.8481,0.4271,-0.141]
l3= [-0.32,0.2481,-0.1729,-0.741]
l = [0.28,0.8481,0.4271,-0.141]
suman = 0
suma2 = 0
for i in l:
    suman += i
    suma2 += (i**2)
print(suman,"=", sqrt(2))
print("1 =",suma2)
print((l[2]*l[0])+(l[3]*l[1]))
#%%------
