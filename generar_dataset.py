###############################################################################
# Curso: ANÁLISIS INTELIGENTE DE DATOS EN ENTORNOS DE BIG DATA
# Profesor: Dr. José Ángel Olivas Varela
# Alumno: Lic. Ariel Maiorano
# Mayo de 2018
###############################################################################
# Generación del dataset
###############################################################################
# Tipos posibles:
# 1. f (x0,x1, . . . ,xn−1) = x0 + xa + xb + xc * xd
# 2. f (x0,x1, . . . ,xn−1) = x0 + xa + xb * xc + xd * xe
# 3. f (x0,x1, . . . ,xn−1) = x0 + xa + xb + xc + xd + xe * xh
#
# Ejemplos en archivos .txt:
# 0,1,2,(1,2)
# 0,1,2,(2,4)
# 0,1,3,(1,5)
# ...
# 0,1,(1,2),(2,3)
# 0,2,(1,2),(1,3)
# ...


# archivos con nlfsrS de período máximo según E. Dubrova, 'dubrova-n4.txt' , 'dubrova-n5.txt', ...
ARCHIVOS_DUBROVA_FORMATO = 'dubrova-n{0}.txt'
# tamaños de registro
N_MINIMO = 4
N_MAXIMO = 8
# archivo de salida
ARCHIVO_SALIDA = 'dataset.csv'
# para campos de salida: N, tipo = 1/2/3, a, b, ..., h, es de período máximo? = 0/1
FORMATO_SALIDA = '{0},{1},{2},{3},{4},{5},{6},{7},{8}'


# obtener nlfsrS de período máximo
maximos_por_n = []
for n in range(N_MINIMO, N_MAXIMO + 1):
	archivo = ARCHIVOS_DUBROVA_FORMATO.format(n)
	with open(archivo) as f:
		contenido = f.readlines()
		for linea in contenido:
			linea = linea.strip()
			if linea == '':
				continue
			maximos_por_n.append(linea + '-' + str(n))
print('Total de registros en archivos "Dubrova": ' + str(len(maximos_por_n)))

# proceso de todas las configuraciones y escritura a archivo de salida (dataset)
contador_maximos = 0
contador_total = 0
# volver a escribir cada vez archivo de salida
f = open(ARCHIVO_SALIDA,'w')
# imprimir encabezado
print('n,tipo,a,b,c,d,e,h,peridodo_maximo', file=f)
# ciclo principal para todas las posibilidades
for n in range(N_MINIMO, N_MAXIMO + 1):
	for a in range(1, n):
		for b in range(1, n):
			for c in range(1, n):
				for d in range(1, n):
					# tipo 1
					if a < b and c < d:	# evitar repticiones a+/*a, a+/*b y b+/*a
						tmp = "0,{0},{1},({2},{3})-{4}".format(a, b, c, d, n)
						es_maximo = 0
						if tmp in maximos_por_n:
							es_maximo = 1
							contador_maximos = contador_maximos + 1
						print(FORMATO_SALIDA.format(n, 1, a, b, c, d, 0, 0, es_maximo), file=f)
						contador_total = contador_total + 1
					for e in range(1, n):
						# tipo 2
						if b < c and d < e and (b < d or c < e):
							tmp = "0,{0},({1},{2}),({3},{4})-{5}".format(a, b, c, d, e, n)
							es_maximo = 0
							if tmp in maximos_por_n:
								es_maximo = 1
								contador_maximos = contador_maximos + 1
							print(FORMATO_SALIDA.format(n, 2, a, b, c, d, e, 0, es_maximo), file=f)
							contador_total = contador_total + 1

						for h in range(1, n):
							# tipo 3
							if a < b and b < c and c < d and e < h:
								tmp = "0,{0},{1},{2},{3},({4},{5})-{6}".format(a, b, c, d, e, h, n)
								es_maximo = 0
								if tmp in maximos_por_n:
									es_maximo = 1
									contador_maximos = contador_maximos + 1
								print(FORMATO_SALIDA.format(n, 3, a, b, c, d, e, h, es_maximo), file=f)
								contador_total = contador_total + 1
f.close()

# impresión de totales a consola
print('Proceso finalizado.')
print('Registros de p. máximo: ' + str(contador_maximos))
print('Total de registros: ' + str(contador_total))

