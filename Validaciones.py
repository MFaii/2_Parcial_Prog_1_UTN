def es_letra_o_espacio(caracter: str) -> None:
    return ("A" <= caracter <= "Z") or ("a" <= caracter <= "z") or caracter == " "


def nombre_valido(nombre: str) -> bool:
    contador_letras = 0
    valido = True

    i = 0

    while i < len(nombre):
        letra = nombre[i]

        if letra != " ":
            contador_letras += 1

        if not es_letra_o_espacio(letra):
            valido = False

        i += 1

    if contador_letras < 3:
        valido = False

    return valido
