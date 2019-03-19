def calculoR(frecuencias):
	potencia = 1
	trobat = 0
	r = sum(frecuencias)* 4
	while trobat ==  0:
		potencia = pow(potencia,2) 
		if potencia > r:
			trobat = 1
			r = potencia
	return r
        


def IntegerArithmeticCode(mensaje,alfabeto,frecuencias):
    r = calculoR(frecuencias)
    print(r)

alfabeto=['a','b','c','d']
frecuencias=[1,10,20,300]
mensaje='dddcabccacabadac'
tamanyo_mensaje=len(mensaje)  
IntegerArithmeticCode(mensaje,alfabeto,frecuencias)