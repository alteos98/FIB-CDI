# -*- coding: utf-8 -*-

import random

'''
0. Dada una codificación R, construir un diccionario para codificar m2c y otro para decodificar c2m
'''
R = [('a','0'), ('b','11'), ('c','100'), ('d','1010'), ('e','1011')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])


'''
1. Definir una función Encode(M, m2c) que, dado un mensaje M y un diccionario 
de codificación m2c, devuelva el mensaje codificado C.
'''

def Encode(M, m2c):
    C = ''
    for x in M:
        C = C + m2c[x]
    return C

''' 
2. Definir una función Decode(C, c2m) que, dado un mensaje codificado C y un diccionario 
de decodificación c2m, devuelva el mensaje original M.
'''
def Decode(C,c2m):
    M = ''
    while len(C):
        aux = C[0]
        C = C[1:]
        while aux not in c2m: 
            aux += C[0]
            C = C[1:]
        M = M + c2m[aux]
    return M

#------------------------------------------------------------------------
# Ejemplo 1
#------------------------------------------------------------------------

R = [('a','0'), ('b','11'), ('c','100'), ('d','1010'), ('e','1011')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])







#------------------------------------------------------------------------
# Ejemplo 2
#------------------------------------------------------------------------
R = [('a','0'), ('b','10'), ('c','110'), ('d','1110'), ('e','1111')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])

''' 
3.
Codificar y decodificar 20 mensajes aleatorios de longitudes también aleatorias.  
Comprobar si los mensajes decodificados coinciden con los originales.
'''
M = ['aebcd', 'abc', 'dbbb', 'cdbaabdddcebbb', 'aaaaaa', 'bb', 'abcabc', 'decba', 'aaaaaaaaaaaaaaaabddbdbbcbdbdeeee', 'eedebababceeddde']

for m in M:
    encode = Encode(m,m2c)
    print(encode)
    decode = Decode(encode,c2m)
    print(decode)

#------------------------------------------------------------------------
# Ejemplo 3 
#------------------------------------------------------------------------
R = [('a','0'), ('b','01'), ('c','011'), ('d','0111'), ('e','1111')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])

''' 
4. Codificar y decodificar los mensajes  'ae' y 'be'. 
Comprobar si los mensajes decodificados coinciden con los originales.
'''
M1 = 'ae'
M2 = 'be'

res = Encode(M1,m2c)
print(res)
res = Decode(res,c2m)
print(res)

res = Encode(M2,m2c)
print(res)
res = Decode(res,c2m)
print(res)

'''
¿Por qué da error?
No sabe diferenciar entre a, b, c o d ya que empiezan todos ellos por 0.
En el caso 'ae' vemos que no falla, solamente en los casos en que hay b, c o d.

(No es necesario volver a implementar Decode(C, m2c) para que no dé error)
'''



  




