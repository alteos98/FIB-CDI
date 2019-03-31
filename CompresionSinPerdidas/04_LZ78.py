# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 11:28:56 2015

@author: martinez
"""
import time
import cdi
import math

#%%
"""
Dado un mensaje dar su codificación  usando el
algoritmo LZ78


mensaje='wabba wabba wabba wabba woo woo woo'
LZ78Code(mensaje)=[[0, 'w'], [0, 'a'], [0, 'b'], [3, 'a'], 
                   [0, ' '], [1, 'a'], [3, 'b'], [2, ' '], 
                   [6, 'b'], [4, ' '], [9, 'b'], [8, 'w'], 
                   [0, 'o'], [13, ' '], [1, 'o'], [14, 'w'], 
                   [13, 'o'], [0, 'EOF']]
  
"""

def LZ78Code(mensaje,debug=False):
    n=len(mensaje)
    codigo=[]
    diccionario=[]
    posicion=0
    while(posicion<n):
        indice=0
        l=1
        cadena=mensaje[posicion:posicion+l]
        
        if debug:
            print(cdi.green(mensaje[:posicion])+cdi.red(mensaje[posicion:]))
            
        while True:
            try:
                indice=diccionario.index(cadena)+1
                l+=1
                if posicion+l>n: break
                cadena=mensaje[posicion:posicion+l]
            except:
                break
        posicion+=l
        if posicion<n:
            diccionario+=[cadena]
            
            if debug:
                print([indice,mensaje[posicion-1]],'\n',diccionario)
                
            codigo+=[[indice,mensaje[posicion-1]]]
        elif posicion==n:
            diccionario+=[cadena]
            
            if debug:
                print([indice,mensaje[posicion-1]],'\n',diccionario)
                
            codigo+=[[indice,mensaje[posicion-1]]]            
            codigo+=[[0,'EOF']]
        else:
            diccionario+=[cadena]
            
            if debug:
                print([indice,'EOF'],'\n',diccionario)
                
            codigo+=[[indice,'EOF']]
    return codigo 
    
 #%%   
"""
Dado un mensaje codificado con el algoritmo LZ78 hallar el mensaje 
correspondiente 

code=

LZ78Decode(mensaje)=
"""    
def LZ78Decode(codigo,debug=False):
    mensaje=''
    diccionario=[]
    n=len(codigo)
    for i in range(n-1):
        indice=codigo[i][0]
        letra=codigo[i][1]
        
        if debug:
            print(codigo[i])
            
        if indice==0:
            mensaje+=letra
            diccionario+=[letra]
            
            if debug:
                print(cdi.green(mensaje[:-1])+cdi.red(letra))
                cdi.escribe(diccionario,debug)
        else:
            palabra=diccionario[indice-1]+letra
            mensaje+=palabra
            diccionario+=[palabra]
            
            if debug:
                print(cdi.green(mensaje[:-len(palabra)])+cdi.blue(diccionario[indice-1])+cdi.red(letra))
                cdi.escribe(diccionario,debug)
            
    indice=codigo[n-1][0]
    letra=codigo[n-1][1]

    if indice>0:
        palabra=diccionario[indice-1]
        mensaje+=palabra
      
    return mensaje, diccionario

#%%    
"""

LZW

"""    
    
def LZWCode(mensaje,debug=False):
    n=len(mensaje)
    codigo=[]
    diccionario=list(set(mensaje))
    diccionario.sort()
    diccionarioInicial=diccionario[:]
    if debug:
        print(diccionario)
    posicion=0
    while(posicion<n):
        indice=0
        l=1
        cadena=mensaje[posicion:posicion+l]
        if debug:
#            print(green(mensaje[:posicion])+red(mensaje[posicion:]))
            if posicion>0:
                print(cdi.green(mensaje[:posicion])+cdi.blue(mensaje[posicion:posicion+1])+cdi.red(mensaje[posicion+1:]))
            else:
                print(cdi.green(mensaje[:posicion])+cdi.red(mensaje[posicion:]))
            print('+'+cadena)
        while True:  
            try:
                indice=diccionario.index(cadena)+1
                l+=1
                if posicion+l>n: break
                cadena=mensaje[posicion:posicion+l]
                if debug:
                    print('+'+cadena)
            except:
                break
        posicion+=l-1
        if posicion<n:
            diccionario+=[cadena]
            if debug:
                print([indice])
                print(diccionario)
            codigo+=[indice]
        elif posicion==n:
            diccionario+=[cadena]
            if debug:
                print([indice])
                print(diccionario)
            codigo+=[indice]            
            codigo+=[0]
        else:
            diccionario+=[cadena]
            if debug:
                print([indice])
                print(diccionario)
            codigo+=[indice]
    return codigo, diccionarioInicial 
 
#mensaje_original="ababababba".upper()
##mensaje_original="accdaaacffaeafabdbbafafcaaecfccffa"
#mensaje_codificado, diccionarioInicial=LZWCode(mensaje_original,debug=True)   
#print(mensaje_codificado, diccionarioInicial)    
   
#%% 
def LZWDecode(codigo, diccionarioInicial, debug=False):
    indice=codigo[0]-1
    mensaje=diccionarioInicial[indice]
    diccionario=diccionarioInicial
    inicio_nueva_palabra_del_diccionario=diccionarioInicial[indice]
    if debug:
        print('Leo '+str(codigo[0])+' que corresponde a: '+diccionarioInicial[indice])       
        print('Inicio de la nueva palabra del diccionario: '+inicio_nueva_palabra_del_diccionario+'?')
    n=len(codigo)
    for i in range(1,n-1):
        indice=codigo[i]-1
        if indice<len(diccionario):
            palabra=diccionario[indice]
            if debug:
                print('\nLeo '+str(codigo[i])+' que corresponde a: '+diccionarioInicial[indice])       
                print('Nueva palabra del diccionario: '+inicio_nueva_palabra_del_diccionario+palabra[0])
            mensaje+=palabra
            diccionario+=[inicio_nueva_palabra_del_diccionario+palabra[0]]
            inicio_nueva_palabra_del_diccionario=palabra
            if debug:
                print('Inicio de la nueva palabra del diccionario: '+inicio_nueva_palabra_del_diccionario+'?')
            
        else:
            #La palabra aún no está en el diccionario, la construyo
            palabra=inicio_nueva_palabra_del_diccionario+inicio_nueva_palabra_del_diccionario[0]
            if debug:
                print('\nLeo '+str(codigo[i])+' que corresponde a: '+cdi.red(inicio_nueva_palabra_del_diccionario+'?')+cdi.blue(' NO ESTÁ COMPLETA'))       
                print(cdi.green('Se completa con la primera letra de la última plababra del diccionario leída que es el inicio de la palabra por completar: ')+cdi.red(inicio_nueva_palabra_del_diccionario[0]))       
                print('Por lo tanto  '+str(codigo[i])+' se corresponde a: '+cdi.red(inicio_nueva_palabra_del_diccionario+palabra[0])+cdi.blue(' YA ESTÁ COMPLETA'))       

                print('Nueva palabra del diccionario: '+inicio_nueva_palabra_del_diccionario+palabra[0])
            mensaje+=palabra
            diccionario+=[inicio_nueva_palabra_del_diccionario+palabra[0]]
            inicio_nueva_palabra_del_diccionario=palabra
        if debug:
            print('Mensaje: '+mensaje)
            print('Diccionario: ',diccionario+[inicio_nueva_palabra_del_diccionario+'?'])
    
    return mensaje, diccionario

#mensaje_original="ababababba".upper()
##mensaje_original="accdaaacffaeafabdbbafafcaaecfccffa"
#mensaje_codificado, diccionarioInicial=LZWCode(mensaje_original,debug=False)   
#print(mensaje_codificado, diccionarioInicial)    
#print()    
#mensaje_recuperado, diccionarioRecuperado= LZWDecode(mensaje_codificado, diccionarioInicial, True)

#%%
print()
print()
print()
#m = accdaaacffaeafabdbbafafcaaecfccffa
#mr= accdaaacffaeaffbdbbeaeacaaeaaccccfa
mensaje_original="ababababba".upper()
mensaje_original="accdaaacffaeafabdbbafafcaaecfccffa"
mensaje_codificado, diccionarioInicial=LZWCode(mensaje_original, True)   
print(mensaje_codificado, diccionarioInicial)    
mensaje_recuperado, diccionarioRecuperado= LZWDecode(mensaje_codificado, diccionarioInicial, True)
if mensaje_original!=mensaje_recuperado:
    print("EEEEEEEEEEEEEEEERRRRRRRRRRRRRRRROOOOOOOOOOOOOOOOOORRRRRR")
if  diccionarioInicial!= diccionarioInicial:
    print("------------------------------")
print()
print()
print()   

#%% 

#print()    
#mensaje='wabba wabba wabba wabba woo woo woo' 
#mensaje_codificado=LZ78Code(mensaje)
#print(mensaje)
#print('Código: ',mensaje_codificado)   
#mensaje_recuperado, diccionario=LZ78Decode(mensaje_codificado)
##print('Código: ',mensaje_codificado)   
#print('Diccionario: ',diccionario)
#print(mensaje_recuperado)
#if (mensaje!=mensaje_recuperado):
#        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

#%%


#mensaje='En muchas de las civilizaciones más tranquilas del margen oriental de la galaxia la "Guía del autoestopista galáctico" ya ha sustituido a la gran "Enciclopedia galáctica" como la fuente reconocida de todo el conocimiento y la sabiduría, porque si bien incurre en muchas omisiones y contiene abundantes hechos de autenticidad dudosa, supera a la segunda obra, más antigua y prosaica, en dos aspectos importantes. En primer lugar, es un poco más barata; luego, grabada en la portada con simpáticas letras grandes, ostenta la leyenda NO SE ASUSTE.'
#mensaje='In many of the more relaxed civilizations on the Outer Eastern Rim of the Galaxy, the Hitchhiker’s Guide has already supplanted the great Encyclopaedia Galactica as the standard repository of all knowledge and wisdom, for though it has many omissions and contains much that is apocryphal, or at least wildly inaccurate, it scores over the older, more pedestrian work in two important respects. First, it is slightly cheaper; and secondly it has the words DON’T PANIC inscribed in large friendly letters on its cover.'
#mensaje="I've seen things you people wouldn't believe. Attack ships on fire off the shoulder of Orion. I watched C-beams glitter in the darkness at Tannhäuser Gate. All those moments will be lost in time like tears in rain. Time to die."
#mensaje="Doublethink means the power of holding two contradictory beliefs in one's mind simultaneously, and accepting both of them."
#mensaje="All right,’ said Deep Thought. ‘The Answer to the Great Question...Of Life, the Universe and Everything...’ said Deep Thought. ‘Is ...Forty-two,’ said Deep Thought, with infinite majesty and calm."
mensaje="‘The Babel fish,’ said The Hitchhiker’s Guide to the Galaxy quietly, ‘is small, yellow and leech-like, and probably the oddest thing in the Universe. It feeds on brainwave energy received not from its own carrier but from those around it. It absorbs all unconscious mental frequencies from this brainwave energy to nourish itself with. It then excretes into the mind of its carrier a telepathic matrix formed by combining the conscious thought frequencies with nerve signals picked up from the speech centres of the brain which has supplied them. The practical upshot of all this is that if you stick a Babel fish in your ear you can instantly understand anything said to you in any form of language. The speech patterns you actually hear decode the brainwave matrix which has been fed into your mind by your Babel fish."
#mensaje="What counts is not what sounds plausible, not what we would like to believe, not what one or two witnesses claim, but only what is supported by hard evidence rigorously and skeptically examined. Extraordinary claims require extraordinary evidence."
#mensaje='no olvides ninguna palabra pero que ninguna palabra pero que ninguna' 
#mensaje='abracadabrapatadecabracabracabracabracabraabracadabrapatadecabra'

#mensaje_codificado=LZ78Code(mensaje,True)
mensaje_codificado=LZWCode(mensaje,True)
print('Código: ',mensaje_codificado)   

#mensaje_recuperado, diccionario=LZ78Decode(mensaje_codificado,True)
#print(mensaje)
#print(mensaje_recuperado)
#if (mensaje!=mensaje_recuperado):
#        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')


#%%
print()
print()
print()
mensaje='mississippi mississippi river' 
mensaje_codificado=LZ78Code(mensaje,True)
print('\nCódigo: ',mensaje_codificado)   
mensaje_recuperado, diccionario=LZ78Decode(mensaje_codificado)
print('\nDiccionario: ',diccionario)
#print(mensaje)
#print(mensaje_recuperado)
if (mensaje!=mensaje_recuperado):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print()
print()
print()

#%%
print()
regenta='La heroica ciudad dormía la siesta. El viento Sur, caliente y perezoso, empujaba las nubes blanquecinas que se rasgaban al correr hacia el Norte. En las calles no había más ruido que el rumor estridente de los remolinos de polvo, trapos, pajas y papeles que iban de arroyo en arroyo, de acera en acera, de esquina en esquina revolando y persiguiéndose, como mariposas que se buscan y huyen y que el aire envuelve en sus pliegues invisibles. Cual turbas de pilluelos, aquellas migajas de la basura, aquellas sobras de todo se juntaban en un montón, parábanse como dormidas un momento y brincaban de nuevo sobresaltadas, dispersándose, trepando unas por las paredes hasta los cristales temblorosos de los faroles, otras hasta los carteles de papel mal pegado a las esquinas, y había pluma que llegaba a un tercer piso, y arenilla que se incrustaba para días, o para años, en la vidriera de un escaparate, agarrada a un plomo. Vetusta, la muy noble y leal ciudad, corte en lejano siglo, hacía la digestión del cocido y de la olla podrida, y descansaba oyendo entre sueños el monótono y familiar zumbido de la campana de coro, que retumbaba allá en lo alto de la esbeltatorre en la Santa Basílica. La torre de la catedral, poema romántico de piedra,delicado himno, de dulces líneas de belleza muda y perenne, era obra del siglo diez y seis, aunque antes comenzada, de estilo gótico, pero, cabe decir, moderado por uninstinto de prudencia y armonía que modificaba las vulgares exageraciones de estaarquitectura. La vista no se fatigaba contemplando horas y horas aquel índice depiedra que señalaba al cielo; no era una de esas torres cuya aguja se quiebra desutil, más flacas que esbeltas, amaneradas, como señoritas cursis que aprietandemasiado el corsé; era maciza sin perder nada de su espiritual grandeza, y hasta sussegundos corredores, elegante balaustrada, subía como fuerte castillo, lanzándosedesde allí en pirámide de ángulo gracioso, inimitable en sus medidas y proporciones.Como haz de músculos y nervios la piedra enroscándose en la piedra trepaba a la altura, haciendo equilibrios de acróbata en el aire; y como prodigio de juegosmalabares, en una punta de caliza se mantenía, cual imantada, una bola grande debronce dorado, y encima otra más pequenya, y sobre ésta una cruz de hierro que acababaen pararrayos.'
mensaje=1*regenta
start_time = time.clock()
mensaje_codificado=LZ78Code(mensaje)
print (time.clock() - start_time, "seconds CODE")
start_time = time.clock()
mensaje_recuperado, diccionario=LZ78Decode(mensaje_codificado)
print (time.clock() - start_time, "seconds DECODE")
bits_indice=math.ceil(math.log(len(diccionario),2))
print("Tamaño del diccionario: ",len(diccionario),"("+str(bits_indice)+" bits por entrada)")
ratio_compresion=8*len(mensaje)/((bits_indice+8)*len(mensaje_codificado))
print("Ratio de compresión: ",ratio_compresion)
if (mensaje!=mensaje_recuperado):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(len(mensaje),len(mensaje_recuperado))
        print(mensaje[-5:],mensaje_recuperado[-5:])
        
        
#%%


"""
Comparacion LZ78 LZW
"""
print()
#with open ("la_regenta_capitulo1", "r") as myfile:
with open ("la_regenta_utf8", "r") as myfile:
    mensaje_leido=myfile.read().replace('\n', '')
    
mensaje=mensaje_leido[0:100000]    
start_time = time.clock()
mensaje_codificado=LZ78Code(mensaje)
print (time.clock() - start_time, "seconds CODE LZ78")
start_time = time.clock()
mensaje_recuperado, diccionario=LZ78Decode(mensaje_codificado)
print (time.clock() - start_time, "seconds DECODE LZ78")
bits_indice=math.ceil(math.log(len(diccionario),2))
print("Tamaño código LZ78: ",len(mensaje_codificado))
print("Tamaño del diccionario LZ78: ",len(diccionario),"("+str(bits_indice)+" bits por entrada)")
ratio_compresion=8*len(mensaje)/((bits_indice+8)*len(mensaje_codificado))
print("Ratio de compresión LZ78: ",ratio_compresion)
if (mensaje!=mensaje_recuperado):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(len(mensaje),len(mensaje_recuperado))
        print(mensaje[-5:],mensaje_recuperado[-5:])
#%%
mensaje=mensaje_leido[0:200000]        
start_time = time.clock()
mensaje_codificado, diccionario=LZWCode(mensaje)
print (time.clock() - start_time, "seconds CODE LZW")
start_time = time.clock()
mensaje_recuperado, diccionario=LZWDecode(mensaje_codificado, diccionario)
print (time.clock() - start_time, "seconds DECODE LZW")
bits_indice=math.ceil(math.log(len(diccionario),2))
print("Tamaño código LZW: ",len(mensaje_codificado))
print("Tamaño del diccionario LZW: ",len(diccionario),"("+str(bits_indice)+" bits por entrada)")
ratio_compresion=8*len(mensaje)/((bits_indice)*len(mensaje_codificado))
print("Ratio de compresión LZW: ",ratio_compresion)
if (mensaje!=mensaje_recuperado):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(len(mensaje),len(mensaje_recuperado))
        print(mensaje[-5:],mensaje_recuperado[-5:])

 
#%%

#'''
#Generar 10 mensajes aleatorios M de longitud 10<=n<=100 aleatoria 
#con las frecuencias esperadas 50, 20, 15, 10 y 5 para los caracteres
#'a', 'b', 'c', 'd', 'e' y codificarlo.
#'''
#alfabeto=['a','b','c','d','e','f']
#frecuencias=[50,20,15,10,5,30]
#indice=dict([(alfabeto[i],i+1) for i in range(len(alfabeto))])
#
#U=''
#for i in range(len(alfabeto)):
#    U=U+alfabeto[i]*frecuencias[i]
#print(U)
#def rd_choice(X,k = 1):
#    Y = []
#    for _ in range(k):
#        Y +=[random.choice(X)]
#    return Y
#
## TAMANYO MUUUUUUUUUUUUUUUUUUUY GRANDE DEL MENSAJE
#l_max=1000
#
#
#errores=0
#numero_de_pruebas=1000
#
#start_time = time.clock()
#for _ in range(numero_de_pruebas):
#    n=random.randint(10,l_max)
#    L = rd_choice(U, n)
#    mensaje = ''
#    for x in L:
#        mensaje += x
#    mensaje_c, diccionarioInicial=LZWCode(mensaje)    
#    mensaje_r, diccionarioRecuperado= LZWDecode(mensaje_c, diccionarioInicial) 
#    if (mensaje!=mensaje_r):
#        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
#        print('m =',mensaje)
#        print('mr=',mensaje_r)
#        errores+=1
#print (time.clock() - start_time, "Tiempo pruebas")
#print("ERRORES: ",errores)


#print()
#print()
#print()
#mensaje=1000000*'a'
#start_time = time.clock()
#mensaje_codificado=LZ78Code(mensaje)
#print (time.clock() - start_time, "seconds CODE AAAAAAAAAAAAAA")
#start_time = time.clock()
#mensaje_recuperado, diccionario=LZ78Decode(mensaje_codificado)
#print (time.clock() - start_time, "seconds DECODE")
#bits_indice=math.ceil(math.log(len(diccionario),2))
#print("Tamaño del diccionario: ",len(diccionario),"("+str(bits_indice)+" bits por entrada)")
#ratio_compresion=8*len(mensaje)/((bits_indice+8)*len(mensaje_codificado))
#print("Ratio de compresión AAAAAAAAAAAAAA: ",ratio_compresion)
#if (mensaje!=mensaje_recuperado):
#        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
#        print(len(mensaje),len(mensaje_recuperado))
#        print(mensaje[-5:],mensaje_recuperado[-5:])

