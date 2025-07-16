import numpy as np
def suma(a,b):
    sumax = a+b
    return sumax

def resta(a,b):
    restax = a-b
    return restax

def multi(a,b):
    multix = a*b
    return multix

def divi(a,b):
    divix= a/b
    return divix

def trans(a):
    transx = np.transpose(a)
    return transx

def crear_matriz(filas, columnas):
    return np.random.randint(0, 10, (filas, columnas))

def matriz_manual(filas, columnas):
    matriz = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            valor = int(input(f"Ingrese el valor para la posición [{i}][{j}]: "))
            fila.append(valor)
        matriz.append(fila)
    return np.array(matriz)

eleccion=input("¿Qué operación matricial desea realizar? \n\t1) Suma \n\t2) Resta \n\t3) Multiplicación \n\t4) División \n\t5) Transposición: ")
creacion=input("¿Desea utilizar las matrices de ejemplo, aleatorias o manuales? \n\t1) Ejemplo \n\t2) Aleatoria \n\t3) Manual: ")

if creacion.lower()=="ejemplo" or creacion=="1":
    matriz1 = np.array([[1,2,3],[4,5,6],[7,8,9]])
    matriz2 = np.array([[9,8,7],[6,5,4],[3,2,1]])
    
elif creacion.lower()=="aleatorias" or creacion=="2":
    tama=int(input("Introduzca el tamaño de la matriz nxn: "))
    matriz1 = crear_matriz(tama, tama)
    matriz2 = crear_matriz(tama, tama)
else:
    tama=int(input("Introduzca el tamaño de la matriz nxn: "))
    matriz1 = matriz_manual(tama, tama)
    matriz2 = matriz_manual(tama, tama)

if eleccion == "1":
    resultado=suma(matriz1,matriz2)
elif eleccion == "2":
    resultado=resta(matriz1,matriz2)
elif eleccion == "3":
    resultado=multi(matriz1,matriz2)
elif eleccion == "4":
    resultado=divi(matriz1,matriz2)
elif eleccion == "5":
    print("Solo se utilizó la matriz 1")
    resultado=trans(matriz1)

print(resultado)