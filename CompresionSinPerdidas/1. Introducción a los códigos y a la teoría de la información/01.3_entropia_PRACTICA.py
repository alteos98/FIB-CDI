# -*- coding: utf-8 -*-
"""

"""
import math
import numpy as np
import matplotlib.pyplot as plt


'''
Dada una lista p, decidir si es una distribución de probabilidad (ddp)
0<=p[i]<=1, sum(p[i])=1.
'''
def es_ddp(p,tolerancia=10**(-5)):
    for x in p:
        if x > 1 or x < 0:
            return False
    if sum(p) == 1:
        return True
    else:
        return False


'''
Dado un código C y una ddp p, hallar la longitud media del código.
'''

def LongitudMedia(C,p):
    sum = 0
    i = 0
    for x in C:
        sum += len(x) * p[i]
        i += 1
    return sum
    
'''
Dada una ddp p, hallar su entropía.
'''
def H1(p):
    sum = 0.0
    for x in p:
        if x != 0:
            sum += x * math.log2(x)
    return -sum

'''
Dada una lista de frecuencias n, hallar su entropía.
'''
def H2(n):
    frecuenciaTotal = sum(n)
    sumatorio = 0.0
    for x in n:
        if x != 0:
            sumatorio += (x / frecuenciaTotal) * math.log2((x / frecuenciaTotal))
    return -sumatorio



'''
Ejemplos
'''
C=['001','101','11','0001','000000001','0001','0000000000']
p=[0.5,0.1,0.1,0.1,0.1,0.1,0]
n=[5,2,1,1,1]

print(es_ddp(p))
print(H1(p))
print(H2(n))
print(LongitudMedia(C,p))



'''
Dibujar H([p,1-p])
'''
p = np.linspace(0,1,100)
y = [H1([p[i],1-p[i]]) for i in range(len(p))]
plt.plot(p,y)
plt.show()

