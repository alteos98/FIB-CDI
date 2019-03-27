# -*- coding: utf-8 -*-
"""
@author: martinez
"""

import math
import random




#%%
"""
Dado un mensaje y su alfabeto con sus frecuencias dar el código 
que representa el mensaje utilizando precisión infinita (reescalado)

El intervalo de trabajo será: [0,R), R=2**k, k menor entero tal que R>4T

T: suma total de frecuencias

"""
def calculateR(sum_frecuencias):
	potencia = 1
	trobat = False
	r = sum_frecuencias * 4
	while not trobat:
		potencia *= 2 
		if potencia > r:
			trobat = True
			r = potencia
	return r

def check_reescalado_e1(l, u, l_initial, u_initial):
	if l >= l_initial and l < u_initial/2 and u >= l_initial and u < u_initial/2:
		return True
	return False

def check_reescalado_e2(l, u, u_initial):
	if l >= (u_initial)/2 and l < u_initial and u >= (u_initial)/2 and u < u_initial:
		return True
	return False

def check_reescalado_e3(l, u, u_initial):
	if l >= (u_initial)/4 and l < 3*(u_initial)/4 and u >= (u_initial)/4 and u < 3*(u_initial)/4:
		return True
	return False

def reescalado_e1(mensaje_codificado, l_anterior, u_anterior, contador):
	l = 2 * l_anterior
	u = 2 * u_anterior
	l = math.floor(l)
	u = math.floor(u)
	mensaje_codificado += '0'
	for x in range(contador):
		mensaje_codificado += '1'
	contador = 0
	return l, u, contador, mensaje_codificado

def reescalado_e2(mensaje_codificado, l_anterior, u_anterior, mitad_intervalo_inicial, contador):
	l = 2 * (l_anterior - mitad_intervalo_inicial)
	u = 2 * (u_anterior - mitad_intervalo_inicial)
	l = math.floor(l)
	u = math.floor(u)
	mensaje_codificado += '1'
	for x in range(contador):
		mensaje_codificado += '0'
	contador = 0
	return l, u, contador, mensaje_codificado

def reescalado_e3(l_anterior, u_anterior, cuarto_intervalo_inicial, contador):
	l = 2 * (l_anterior - cuarto_intervalo_inicial)
	u = 2 * (u_anterior - cuarto_intervalo_inicial)
	l = math.floor(l)
	u = math.floor(u)
	contador += 1
	return l, u, contador

def read_symbol(l_anterior, u_anterior, simbolo, indice_simbolo, frecuencias, sum_frecuencias):
	#print(indice_simbolo)
	sumatorio_parcial_frecuencias_l = sumatorio_parcial_frecuencias_u = 0
	for i in range(indice_simbolo):
		sumatorio_parcial_frecuencias_l += frecuencias[i]
	sumatorio_parcial_frecuencias_u = sumatorio_parcial_frecuencias_l + frecuencias[indice_simbolo]

	dif_intervalo = u_anterior - l_anterior
	l = (sumatorio_parcial_frecuencias_l * dif_intervalo/sum_frecuencias)
	l = math.floor(l) + l_anterior
	u = (sumatorio_parcial_frecuencias_u * dif_intervalo/sum_frecuencias)
	u = l_anterior + math.floor(u)
	return l, u

def IntegerArithmeticCode(mensaje, alfabeto, frecuencias):
	sum_frecuencias = sum(frecuencias)
	r = calculateR(sum_frecuencias)
	l = l_initial = 0
	u = u_initial = r
	contador = 0
	mensaje_codificado = ''
	simbolo_actual = 0
	while simbolo_actual < len(mensaje):
		#print("Lower: " + str(l))
		#print("Upper: " + str(u))
		if check_reescalado_e1(l, u, l_initial, u_initial):
			l, u, contador ,mensaje_codificado = reescalado_e1(mensaje_codificado, l, u, contador)
		elif check_reescalado_e2(l, u, u_initial):
			l, u, contador, mensaje_codificado = reescalado_e2(mensaje_codificado, l, u, r/2, contador)
		elif check_reescalado_e3(l, u, u_initial):
			l, u, contador = reescalado_e3(l, u, r/4, contador)
		else:
			for indice, simbolo in enumerate(alfabeto):
				if simbolo == mensaje[simbolo_actual]:
					l, u = read_symbol(l, u, simbolo, indice, frecuencias, sum_frecuencias)
					#print(mensaje[simbolo_actual])
					simbolo_actual += 1
					break
	return mensaje_codificado

#%%  
"""
Dada la representación binaria del número que representa un mensaje, la
longitud del mensaje y el alfabeto con sus frecuencias 
dar el mensaje original
"""

# returns the frequency value that corresponds to the next symbol
def NextFreq(t, l, u, sumFrec):
	return math.floor(((t - l + 1) * sumFrec - 1) / (u - l + 1))

def Freq2Symbol(frecuencias, new_frec, alfabeto):
	for index, frec in enumerate(frecuencias):
		if new_frec < frec:
			print(alfabeto[index-1])
			print(index)
			return alfabeto[index-1], index-1
	print("Error")

def UpdateLower(l_anterior, u_anterior, sumFrec, sumFrecParcialL):
	return l_anterior + math.floor(((u_anterior - l_anterior + 1) * sumFrecParcialL) / (sumFrec))

def UpdateUpper(l_anterior, u_anterior, sumFrec, sumFrecParcialU):
	return l_anterior + math.floor(((u_anterior - l_anterior + 1) * sumFrecParcialU) / (sumFrec)) - 1

# [0, frecuencias[0], frecuencias[0]+frecuencias[1], ..., sum(frecuencias)]
def SumaParcialFrec(frecuencias):
	sumaParcial = []
	sumaParcial.append(0)
	for indice, frec in enumerate(frecuencias):
		sumaParcial.append(sumaParcial[indice] + frec)
	return sumaParcial

def bin2dec(binario):
	dec = 0
	for i, x in enumerate(reversed(binario)):
		if x == '1':
			dec += pow(2, i)
	return dec

def SameMSB(l, u):
	if l[0] == u[0]:
		return True
	else:
		return False

def ShiftLeft(c):
	return c[1:]

## complementa el bit de mayor peso
def ComplementMSB(c):
	aux = list(c)
	if aux[0] == '0':
		aux[0] = '1'
	else:
		aux[0] = '0'
	s = ''.join(aux)
	#print(s)
	return s

## Rellena bin con ceros a la izquierda hasta que tiene longitud nElem
def fillBin(binario, nElem):
	binR = list(reversed(binario[2:]))
	while len(binR) < nElem:
		binR += '0'
	s = ''.join(list(reversed(binR)))
	return s

def IntegerArithmeticDecode(codigo, tamanyo_mensaje, alfabeto, frecuencias):
	mensaje_decodificado = ''
	sumFrec = sum(frecuencias)
	sumParcialFrec = SumaParcialFrec(frecuencias)
	t_bin = codigo[0:tamanyo_mensaje]
	t = bin2dec(t_bin)
	print(fillBin(bin(t), tamanyo_mensaje))
	l = 0
	u = u_inicial = pow(2, tamanyo_mensaje) - 1
	desfase = 0
	while (len(mensaje_decodificado) < tamanyo_mensaje):
		l_anterior = l
		u_anterior = u
		newFrec = NextFreq(t, l, u, sumFrec)
		print("newFrec: " + str(newFrec))
		symbol, symbolIndex = Freq2Symbol(sumParcialFrec, newFrec, alfabeto)
		mensaje_decodificado += str(symbol)
		#print(mensaje_decodificado)
		print(l)
		print(u)
		l = UpdateLower(l_anterior, u_anterior, sumFrec, sumParcialFrec[symbolIndex])
		u = UpdateUpper(l_anterior, u_anterior, sumFrec, sumParcialFrec[symbolIndex+1])
		l_bin = fillBin(bin(l), tamanyo_mensaje)
		u_bin = fillBin(bin(u), tamanyo_mensaje)
		print(l)
		print(u)
		while (SameMSB(l_bin, u_bin) or check_reescalado_e3(l, u, u_inicial+1)):
			if SameMSB(l_bin, u_bin):
				print('SameMSB')
				#print('Antes sameMSB: ' + str(l))
				#print('Antes sameMSB: ' + str(u))
				#print(l)
				#print(u)
				l_bin = ShiftLeft(l_bin)
				l_bin += '0'
				l = bin2dec(l_bin)
				u_bin = ShiftLeft(u_bin)
				u_bin += '1'
				u = bin2dec(u_bin)
				t_bin = ShiftLeft(t_bin)
				t_bin += codigo[tamanyo_mensaje + desfase]
				t = bin2dec(t_bin)
				desfase += 1
				#print('Despues sameMSB: ' + str(l))
				#print('Despues sameMSB: ' + str(u))
			if check_reescalado_e3(l, u, u_inicial+1):
				print('reescalado e3')
				#print('Antes e3: ' + str(l))
				#print('Antes e3: ' + str(u))
				l_bin = ShiftLeft(l_bin)
				l_bin += '0'
				u_bin = ShiftLeft(u_bin)
				u_bin += '1'
				t_bin = ShiftLeft(t_bin)
				t_bin += codigo[tamanyo_mensaje + desfase]
				desfase += 1
				l_bin = ComplementMSB(l_bin)
				u_bin = ComplementMSB(u_bin)
				t_bin = ComplementMSB(t_bin)
				#print(l_bin)
				#print(u_bin)
				l = bin2dec(l_bin)
				u = bin2dec(u_bin)
				t = bin2dec(t_bin)
				#print('Despues e3: ' + str(l))
				#print('Despues e3: ' + str(u))
	return mensaje_decodificado

#%%
"""
Definir una función que codifique un mensaje utilizando codificación aritmética con precisión infinita
obtenido a partir de las frecuencias de los caracteres del mensaje.

Definir otra función que decodifique los mensajes codificados con la función 
anterior. """

def findAlfabeto(mensaje):
	diccionario = {}
	for x in mensaje:
		if x not in diccionario:
			diccionario[x] =  1
		else:
			diccionario[x] += 1
	lista = []
	for key, value in diccionario.items():
		lista.append([key,value])
	lista.sort(key = lambda x: x[1])
	alfabeto = []
	frecuencias = []
	for p in lista:
		alfabeto.append(p[0])
		frecuencias.append(p[1])
	return alfabeto, frecuencias

def EncodeArithmetic(mensaje_a_codificar):
	alfabeto, frecuencias = findAlfabeto(mensaje_a_codificar)
	mensaje_codificado = IntegerArithmeticCode(mensaje_a_codificar, alfabeto, frecuencias)
	return mensaje_codificado,alfabeto,frecuencias
    
def DecodeArithmetic(mensaje_codificado,tamanyo_mensaje,alfabeto,frecuencias):
	mensaje_decodificado = IntegerArithmeticDecode(mensaje_codificado, tamanyo_mensaje, alfabeto, frecuencias)
	return mensaje_decodificado


#%%
'''
Ejemplo (!El mismo mensaje se puede codificar con varios códigos¡)

lista_C=['010001110110000000001000000111111000000100010000000000001100000010001111001100001000000',
         '01000111011000000000100000011111100000010001000000000000110000001000111100110000100000000']
print(lista_C[0])
print(lista_C[1])

alfabeto=['a','b','c','d']
frecuencias=[1,10,20,300]
mensaje='dddcabccacabadac'
tamanyo_mensaje=len(mensaje)  

for C in lista_C:
    mensaje_recuperado=DecodeArithmetic(C,tamanyo_mensaje,alfabeto,frecuencias)
    print(mensaje==mensaje_recuperado)

'''

#%%

'''
Ejemplo

'''


#mensaje='La heroica ciudad dormía la siesta. El viento Sur, caliente y perezoso, empujaba las nubes blanquecinas que se rasgaban al correr hacia el Norte. En las calles no había más ruido que el rumor estridente de los remolinos de polvo, trapos, pajas y papeles que iban de arroyo en arroyo, de acera en acera, de esquina en esquina revolando y persiguiéndose, como mariposas que se buscan y huyen y que el aire envuelve en sus pliegues invisibles. Cual turbas de pilluelos, aquellas migajas de la basura, aquellas sobras de todo se juntaban en un montón, parábanse como dormidas un momento y brincaban de nuevo sobresaltadas, dispersándose, trepando unas por las paredes hasta los cristales temblorosos de los faroles, otras hasta los carteles de papel mal pegado a las esquinas, y había pluma que llegaba a un tercer piso, y arenilla que se incrustaba para días, o para años, en la vidriera de un escaparate, agarrada a un plomo. Vetusta, la muy noble y leal ciudad, corte en lejano siglo, hacía la digestión del cocido y de la olla podrida, y descansaba oyendo entre sueños el monótono y familiar zumbido de la campana de coro, que retumbaba allá en lo alto de la esbeltatorre en la Santa Basílica. La torre de la catedral, poema romántico de piedra,delicado himno, de dulces líneas de belleza muda y perenne, era obra del siglo diez y seis, aunque antes comenzada, de estilo gótico, pero, cabe decir, moderado por uninstinto de prudencia y armonía que modificaba las vulgares exageraciones de estaarquitectura. La vista no se fatigaba contemplando horas y horas aquel índice depiedra que señalaba al cielo; no era una de esas torres cuya aguja se quiebra desutil, más flacas que esbeltas, amaneradas, como señoritas cursis que aprietandemasiado el corsé; era maciza sin perder nada de su espiritual grandeza, y hasta sussegundos corredores, elegante balaustrada, subía como fuerte castillo, lanzándosedesde allí en pirámide de ángulo gracioso, inimitable en sus medidas y proporciones.Como haz de músculos y nervios la piedra enroscándose en la piedra trepaba a la altura, haciendo equilibrios de acróbata en el aire; y como prodigio de juegosmalabares, en una punta de caliza se mantenía, cual imantada, una bola grande debronce dorado, y encima otra más pequenya, y sobre ésta una cruz de hierro que acababaen pararrayos.'
#mensaje_codificado, alfabeto, frecuencias = EncodeArithmetic(mensaje)

'''
alfabeto=['a','b','c','d']
frecuencias=[1,10,20,300]
mensaje='dddcabccacabadac'
mensaje_codificado = IntegerArithmeticCode(mensaje, alfabeto, frecuencias)

print(mensaje_codificado)
print(alfabeto)
print(frecuencias)
'''

"""
mensaje_recuperado=DecodeArithmetic(mensaje_codificado,len(mensaje),alfabeto,frecuencias)

ratio_compresion=8*len(mensaje)/len(mensaje_codificado)
print(ratio_compresion)

if (mensaje!=mensaje_recuperado):
        print('!!!!!!!!!!!!!!  ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
"""
alfabeto=['a','b','c','d']
frecuencias=[1,10,20,300]
mensaje='dddcabccacabadac'
lista_C=['010001110110000000001000000111111000000100010000000000001100000010001111001100001000000',
         '01000111011000000000100000011111100000010001000000000000110000001000111100110000100000000']

code = IntegerArithmeticCode(mensaje, alfabeto, frecuencias)

tamanyo_mensaje = len(mensaje)
mensaje_recuperado=DecodeArithmetic(code, tamanyo_mensaje, alfabeto, frecuencias)

print("RESULTADOS:")

print("1. " + code)
print("A: " + lista_C[0])
print("B: " + lista_C[1])

print("Original: " + str(mensaje))
print("Nuestro:  " + str(mensaje_recuperado))