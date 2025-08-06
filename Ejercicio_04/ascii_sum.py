# ascii_sum.py

def suma_ascii(cadena):
    """Suma los valores ASCII de todos los caracteres en la cadena."""
    return sum(ord(char) for char in cadena)
