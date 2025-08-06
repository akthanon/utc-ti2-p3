def mostrar_menu():
    print("\n--- Gestor de Estudiantes ---")
    print("1. Agregar estudiante")
    print("2. Mostrar todos los estudiantes")
    print("3. Calcular promedio de un estudiante")
    print("4. Eliminar estudiante")
    print("5. Salir")

def agregar_estudiante(estudiantes):
    id_estudiante = input("Ingrese el ID del estudiante (ej. A003): ").strip()
    if id_estudiante in estudiantes:
        print("⚠️ Ya existe un estudiante con ese ID.")
        return

    nombre = input("Ingrese el nombre completo: ").strip()
    try:
        edad = int(input("Ingrese la edad: "))
    except ValueError:
        print("⚠️ Edad no válida. Debe ser un número.")
        return

    calificaciones = []
    while True:
        entrada = input("Ingrese una calificación (o 'fin' para terminar): ")
        if entrada.lower() == 'fin':
            break
        try:
            nota = float(entrada)
            calificaciones.append(nota)
        except ValueError:
            print("⚠️ Calificación no válida. Intente de nuevo.")

    estudiantes[id_estudiante] = {
        "nombre": nombre,
        "edad": edad,
        "calificaciones": calificaciones
    }
    print(f"✅ Estudiante {id_estudiante} agregado con éxito.")

def mostrar_estudiantes(estudiantes):
    if not estudiantes:
        print("📭 No hay estudiantes registrados.")
        return
    print("\n--- Lista de Estudiantes ---")
    for id_est, info in estudiantes.items():
        nombre = info['nombre']
        edad = info['edad']
        calif = info['calificaciones']
        promedio = sum(calif) / len(calif) if calif else 0
        print(f"{id_est} - {nombre} ({edad} años) - Promedio: {promedio:.2f}")

def calcular_promedio(estudiantes):
    id_est = input("Ingrese el ID del estudiante: ").strip()
    if id_est not in estudiantes:
        print("⚠️ No se encontró un estudiante con ese ID.")
        return
    calif = estudiantes[id_est]['calificaciones']
    if not calif:
        print(f"{id_est} - {estudiantes[id_est]['nombre']} - Sin calificaciones registradas.")
    else:
        promedio = sum(calif) / len(calif)
        print(f"{id_est} - {estudiantes[id_est]['nombre']} - Promedio: {promedio:.2f}")

def eliminar_estudiante(estudiantes):
    id_est = input("Ingrese el ID del estudiante a eliminar: ").strip()
    if id_est in estudiantes:
        del estudiantes[id_est]
        print(f"🗑️ Estudiante {id_est} eliminado.")
    else:
        print("⚠️ No existe un estudiante con ese ID.")

# Diccionario principal
estudiantes = {
    "A001": {"nombre": "Ana Torres", "edad": 20, "calificaciones": [90, 85, 78]},
    "A002": {"nombre": "Luis Pérez", "edad": 22, "calificaciones": [88, 91, 79]}
}

# Bucle principal
while True:
    mostrar_menu()
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
        agregar_estudiante(estudiantes)
    elif opcion == "2":
        mostrar_estudiantes(estudiantes)
    elif opcion == "3":
        calcular_promedio(estudiantes)
    elif opcion == "4":
        eliminar_estudiante(estudiantes)
    elif opcion == "5":
        print("👋 Saliendo del programa.")
        break
    else:
        print("⚠️ Opción no válida. Intente de nuevo.")
