def leer_estudiantes(nombre_archivo):
    estudiantes = []
    try:
        with open(nombre_archivo, 'r') as archivo:
            for linea in archivo:
                try:
                    nombre, calificacion = linea.strip().split(",")
                    estudiantes.append((nombre, float(calificacion)))
                except ValueError:
                    print(f"[!] Formato incorrecto en línea: {linea.strip()}")
    except FileNotFoundError:
        print(f"[!] El archivo {nombre_archivo} no existe. Se creará uno nuevo.")
        with open(nombre_archivo, 'w') as f:
            pass  # Crea archivo vacío
    return estudiantes

def calcular_promedio(estudiantes):
    if not estudiantes:
        return 0
    total = sum(calificacion for _, calificacion in estudiantes)
    return total / len(estudiantes)

def generar_reporte(estudiantes, archivo_reporte):
    promedio = calcular_promedio(estudiantes)
    try:
        with open(archivo_reporte, 'w') as archivo:
            for nombre, calificacion in estudiantes:
                archivo.write(f"{nombre},{calificacion}\n")
            archivo.write(f"Promedio general: {promedio:.1f}\n")
        print("[✓] Reporte generado correctamente en 'reporte.txt'")
    except Exception as e:
        print(f"[!] Error al escribir el reporte: {e}")

def agregar_estudiante(nombre_archivo):
    nombre = input("Nombre del estudiante: ").strip()
    try:
        calificacion = float(input("Calificación del estudiante: "))
        if calificacion < 0 or calificacion > 100:
            print("[!] La calificación debe estar entre 0 y 100.")
            return
        with open(nombre_archivo, 'a') as archivo:
            archivo.write(f"{nombre},{calificacion}\n")
        print("[+] Estudiante agregado correctamente.")
    except ValueError:
        print("[!] Calificación inválida. Debe ser un número.")

def menu():
    archivo_estudiantes = "estudiantes.txt"
    archivo_reporte = "reporte.txt"

    while True:
        print("\n--- Menú ---")
        print("1. Mostrar promedio actual")
        print("2. Generar reporte")
        print("3. Agregar nuevo estudiante")
        print("4. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            estudiantes = leer_estudiantes(archivo_estudiantes)
            promedio = calcular_promedio(estudiantes)
            print(f"Promedio general: {promedio:.1f}")
        elif opcion == "2":
            estudiantes = leer_estudiantes(archivo_estudiantes)
            generar_reporte(estudiantes, archivo_reporte)
        elif opcion == "3":
            agregar_estudiante(archivo_estudiantes)
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("[!] Opción no válida.")

if __name__ == "__main__":
    menu()
