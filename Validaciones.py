import re


def nombre_valido(nombre: str) -> bool:
    nombre = nombre.strip()

    if len(nombre) < 1:
        return False

    # isalpha devuelve true para letras
    if not any(c.isalpha() for c in nombre):
        return False

    # Solo letras, espacios y opcionalmente números (ajustable)
    patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 ]+$"
    if not re.match(patron, nombre):
        return False

    return True
