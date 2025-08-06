# ascii_utils.py

def ascii_pares(cadena):
    """Devuelve los caracteres cuyo valor ASCII es par."""
    return [char for char in cadena if ord(char) % 2 == 0]
