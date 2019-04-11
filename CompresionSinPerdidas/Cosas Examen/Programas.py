import math
import numpy as np
import matplotlib.pyplot as plt




###############################LZ77#############################
def LZ77Code(mensaje,S=12,W=18):
	code=[[0,0,mensaje[0]]]
	mydict=[[0,0,mensaje[0]]]
	i=1#donde estamos leyendo carácteres
	ahead=W-S
	lookahead=mensaje[1:1+ahead]
	old=str(mensaje[max(0,i-S-1):max(0,i)])
	while i < len(mensaje):
		offset=0
		length=0
		char=lookahead[0]
		window = old+lookahead
		#miramos matches 
		for j in range(len(old)-1,-1,-1):
			if old[j] == lookahead[0]:
				#tenemos algun match
				match=True
				izq=j+1
				der=len(old)+1
				maxlen=1
				#longest prefix match
				while match and der <len(window):
					if window[izq] == window[der]:
						izq+=1
						der+=1
						maxlen+=1
					else: 
						match=False
				#extendemos carácteres extra
				if maxlen> length :
					offset= len(old) -j
					length= maxlen
					try :
						char= window[der]
					except:
						try:
							char= window[i+length]
						except:
							char=window[der-1]
							length -=1
							if length == 0:
								offset=0
							
		code=code+[[offset,length,char]]
		i += length+1
		old=str(mensaje[max(0,i-S):i])
		lookahead= str(mensaje[i:ahead+i])
	code[-1]=[code[-1][0],code[-1][1]+1,'EOF']
	return code


#####################DECODE PREGUNTA 7########################
def LZ77Decode(codigo):
	mensaje=''
	for i in codigo:
		if i[0] != 0:
			pos=len(mensaje)-i[0]
			word=mensaje[pos:pos+ i[1]] 
			extension= ""
			mensaje += word 
			if i[0] <= i[1]:#debemos extender el último simbolo
				mensaje += mensaje[i[0]+1:i[1]+1] 
		mensaje+= i[2]
	return mensaje[:-3]
########################PREGUNTA 2, MENSAJE ORIGINAL###############



alfabeto = ['a','b','c','d']
probabilidades = [0.2,0.1,0.1,0.6]
longitud = 5
valor = 0.7775
###########################################

###########PREGUNTA 4 #####################

def H1(p):
    sum = 0.0
    for x in p:
        if x != 0:
            sum += x * math.log2(x)
    return -sum
'''
VALOR DE L ESTA ENTRE EL VALOR DE H1 Y H1 + 1
'''
#########################################

########### PREGUNTA 8 ###################



##################################################
##############PREGUNTA 10, KRAFT CON LONGITUDES ################

def  kraft2(L, q=2):
    l = max(L)
    res = pow(2, l)
    for x in L:
        res -= (pow(2, l) / pow(2, x))
    return round(res)

L = [2,2,3,7,8,8,8]
print("PREGUNTA 10: kraft " + str(kraft2(L)))
###############################################
