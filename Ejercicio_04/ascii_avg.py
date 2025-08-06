# ascii_avg.py

def promedio_ascii(cadena):
    """Calcula el promedio de los valores ASCII de los caracteres en la cadena."""
    if not cadena:
        return 0
    return sum(ord(char) for char in cadena) / len(cadena)
