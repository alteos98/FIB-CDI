# -*- coding: utf-8 -*-
"""

"""

'''
Dada la lista L de longitudes de las palabras de un código 
q-ario, decidir si pueden definir un código.

'''

def  kraft1(L, q=2):
    res = 0
    for x in L:
        res += (1 / pow(q,x))

    if res <= 1:
        return True
    else:
        return False
        
'''
Dada la lista L de longitudes de las palabras de un código 
q-ario, calcular el máximo número de palabras de longitud 
máxima, max(L), que se pueden añadir y seguir siendo un código.

'''

def  kraft2(L, q=2):
    l = max(L)
    res = pow(2, l)
    for x in L:
        res -= (pow(2, l) / pow(2, x))
    return round(res)

'''
Dada la lista L de longitudes de las palabras de un  
código q-ario, calcular el máximo número de palabras 
de longitud Ln, que se pueden añadir y seguir siendo 
un código.
'''

def  kraft3(L, Ln, q=2):
    res = pow(2, Ln)
    for x in L:
        res -= (pow(2, Ln) / pow(2, x))
    return round(res)

'''
Dada la lista L de longitudes de las palabras de un  
código q-ario, hallar un código prefijo con palabras 
con dichas longitudes
'''
'''
Pre: entra una llista de candidats a ser paraules i la q
Post: hem afegit a 'candidates' totes les paraules amb 1 símbol més (a partir de les que hi havien a 'candidates')
'''
def generateCandidates(candidates, q):
    newCandidates = []
    for c in candidates:
        for x in range(q):
            newCandidates.append(c + str(x))
    return newCandidates

def Code(L,q=2):
    L.sort()
    candidates = ['']
    prefixCode = []
    actualLength = 0
    for l in L:
        while actualLength < l:
            candidates = generateCandidates(candidates, q)
            actualLength += 1
        prefixCode.append(candidates[0])
        candidates.pop(0)
    return prefixCode

#%%

'''
Ejemplos
'''
#%%

L=[2,3,3,3,4,4,4,6]
q=2

print("\n",sorted(L),' codigo final:',Code(L,q))
print(kraft1(L,q))
print(kraft2(L,q))
print(kraft3(L,max(L)+1,q))

#%%
L=[1,3,5,5,3,5,7,2,2,2]
q=3

print(sorted(L),' codigo final:',Code(L,q))
print(kraft1(L,q))