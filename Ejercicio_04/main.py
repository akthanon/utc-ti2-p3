# main.py

import ascii_sum
import ascii_avg
import ascii_utils

def menu():
    print("\n--- Sumador ASCII ---")
    print("1. Sumar valores ASCII")
    print("2. Promedio de valores ASCII")
    print("3. Mostrar caracteres con ASCII par")
    print("4. Salir")

def main():
    while True:
        menu()
        opcion = input("Selecciona una opción: ")
        if opcion == "4":
            print("¡Hasta luego!")
            break

        cadena = input("Introduce una cadena de texto: ")

        if opcion == "1":
            resultado = ascii_sum.suma_ascii(cadena)
            print(f"Suma ASCII: {resultado}")
        elif opcion == "2":
            resultado = ascii_avg.promedio_ascii(cadena)
            print(f"Promedio ASCII: {resultado:.2f}")
        elif opcion == "3":
            resultado = ascii_utils.ascii_pares(cadena)
            print("Caracteres con ASCII par:", resultado)
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()
