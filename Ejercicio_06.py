# sistema_tareas.py

tareas = []

# Función para agregar una tarea
def agregar_tarea(*args, **kwargs):
    nombre = kwargs.get("nombre")
    prioridad = kwargs.get("prioridad", 1)
    estado = kwargs.get("estado", "pendiente")

    if not nombre:
        print("[!] Error: se requiere un nombre para la tarea.")
        return

    if any(t["nombre"] == nombre for t in tareas):
        print("[!] Ya existe una tarea con ese nombre.")
        return

    if estado not in ["pendiente", "en proceso", "completada"]:
        print("[!] Estado no válido. Usa: pendiente, en proceso, completada.")
        return

    try:
        prioridad = int(prioridad)
    except ValueError:
        print("[!] Prioridad debe ser un número entero.")
        return

    tarea = {
        "nombre": nombre,
        "prioridad": prioridad,
        "estado": estado
    }
    tareas.append(tarea)
    print(f"[+] Tarea '{nombre}' agregada.")

# Función para eliminar una tarea
def eliminar_tarea(*args, **kwargs):
    nombre = kwargs.get("nombre")
    if not nombre:
        print("[!] Especifica el nombre de la tarea a eliminar.")
        return

    for i, tarea in enumerate(tareas):
        if tarea["nombre"] == nombre:
            tareas.pop(i)
            print(f"[-] Tarea '{nombre}' eliminada.")
            return

    print("[!] Tarea no encontrada.")

# Función para listar tareas ordenadas por prioridad
def listar_tareas(*args, **kwargs):
    if not tareas:
        print("[~] No hay tareas.")
        return

    ordenadas = sorted(tareas, key=lambda x: x["prioridad"])
    print("\n--- Lista de Tareas (ordenadas por prioridad) ---")
    for tarea in ordenadas:
        print(f"- {tarea['nombre']} | Prioridad: {tarea['prioridad']} | Estado: {tarea['estado']}")
    print("--------------------------------------------------")

# Función de orden superior que delega a la función correspondiente
def gestionar_tareas(accion, *args, **kwargs):
    if callable(accion):
        return accion(*args, **kwargs)
    else:
        print("[!] Acción no válida, no es una función.")

# Menú interactivo (opcional)
def menu():
    while True:
        print("\n--- MENÚ ---")
        print("1. Agregar tarea")
        print("2. Eliminar tarea")
        print("3. Listar tareas")
        print("4. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            nombre = input("Nombre de la tarea: ")
            prioridad = input("Prioridad (número): ")
            estado = input("Estado (pendiente / en proceso / completada): ")
            gestionar_tareas(agregar_tarea, nombre=nombre, prioridad=prioridad, estado=estado)
        elif opcion == "2":
            nombre = input("Nombre de la tarea a eliminar: ")
            gestionar_tareas(eliminar_tarea, nombre=nombre)
        elif opcion == "3":
            gestionar_tareas(listar_tareas)
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("[!] Opción no válida.")

# Ejecución
if __name__ == "__main__":
    menu()
