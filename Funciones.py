import random
from Constantes import *
import pygame
import json
from datetime import datetime
import os


def mostrar_texto(surface, text, pos, font, color=pygame.Color("black")):
    words = [
        word.split(" ") for word in text.splitlines()
    ]  # 2D array where each row is a list of words.
    space = font.size(" ")[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, False, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


# GENERAL
def mezclar_lista(lista_preguntas: list) -> None:
    random.shuffle(lista_preguntas)


# GENERAL
def reiniciar_estadisticas(datos_juego: dict) -> None:
    datos_juego["puntuacion"] = 0
    datos_juego["vidas"] = CANTIDAD_VIDAS
    datos_juego["nombre"] = ""
    datos_juego["tiempo_restante"] = 30
    datos_juego["comodin_pasar_usado"] = False
    datos_juego["comodin_doble_usado"] = False
    datos_juego["x2_activado"] = False
    datos_juego["comodin_doble_chance"] = False
    datos_juego["doble_chance_activada"] = False
    datos_juego["respuestas_ocultas"] = []
    datos_juego["intento_extra"] = False
    datos_juego["comodin_bomba_usado"] = False
    datos_juego["respuestas_ocultadas_bomba"] = []


# GENERAL
def verificar_respuesta(datos_juego: dict, pregunta: dict, respuesta: int) -> bool:
    return respuesta == pregunta["respuesta_correcta"]


def crear_elemento_juego(
    textura: str, ancho: int, alto: int, pos_x: int, pos_y: int
) -> dict:
    elemento_juego = {}
    elemento_juego["superficie"] = pygame.transform.scale(
        pygame.image.load(textura), (ancho, alto)
    )
    elemento_juego["rectangulo"] = elemento_juego["superficie"].get_rect()
    elemento_juego["rectangulo"].x = pos_x
    elemento_juego["rectangulo"].y = pos_y

    return elemento_juego


def limpiar_superficie(
    elemento_juego: dict, textura: str, ancho: int, alto: int
) -> None:
    elemento_juego["superficie"] = pygame.transform.scale(
        pygame.image.load(textura), (ancho, alto)
    )


def obtener_respuesta_click(lista_respuestas: list, pos_click: tuple):
    respuesta = None

    for i in range(len(lista_respuestas)):
        if lista_respuestas[i]["rectangulo"].collidepoint(pos_click):
            respuesta = i + 1

    return respuesta


def cambiar_pregunta(
    lista_preguntas: list, indice: int, caja_pregunta: dict, lista_respuestas: list
) -> dict:
    pregunta_actual = lista_preguntas[indice]
    limpiar_superficie(
        caja_pregunta, "./imgs/textura_pregunta.jpg", ANCHO_PREGUNTA, ALTO_PREGUNTA
    )
    for i in range(len(lista_respuestas)):
        limpiar_superficie(
            lista_respuestas[i], "./imgs/textura_respuesta.jpg", ANCHO_BOTON, ALTO_BOTON
        )

    return pregunta_actual


def crear_botones_menu() -> list:
    lista_botones = []
    cantidad_botones = 4
    espacio = 20
    altura_total = cantidad_botones * ALTO_BOTON + (cantidad_botones - 1) * espacio
    pos_y = (600 - altura_total) // 2
    pos_x = (600 - ANCHO_BOTON) // 2

    for i in range(cantidad_botones):
        boton = crear_elemento_juego(
            "./imgs/textura_respuesta.jpg", ANCHO_BOTON, ALTO_BOTON, pos_x, pos_y
        )
        lista_botones.append(boton)
        pos_y += ALTO_BOTON + espacio

    return lista_botones


def crear_respuestas(
    textura: str,
    ancho: int,
    alto: int,
    pos_x: int,
    pos_y: int,
    cantidad_respuestas: int,
) -> list:
    lista_respuestas = []

    for i in range(cantidad_respuestas):
        boton_respuesta = crear_elemento_juego(textura, ancho, alto, pos_x, pos_y)
        lista_respuestas.append(boton_respuesta)
        pos_y += 80

    return lista_respuestas


def manejar_texto(
    cuadro_texto: dict,
    tecla_nombre: str,
    tecla_unicode: str,
    bloc_mayus: int,
    datos_juego: dict,
) -> None:
    # 1. Si se presiona la barra espaciadora
    if tecla_nombre == "space":
        CLICK_SONIDO.play()
        datos_juego["nombre"] += " "

    # 2. Si se presiona la tecla borrar (backspace) y hay texto para borrar
    elif tecla_nombre == "backspace" and len(datos_juego["nombre"]) > 0:
        datos_juego["nombre"] = datos_juego["nombre"][:-1]
        limpiar_superficie(
            cuadro_texto, "./imgs/textura_respuesta.jpg", ANCHO_CUADRO, ALTO_CUADRO
        )

    # 3. Si se presiona una letra, número o símbolo imprimible
    elif len(tecla_unicode) == 1 and tecla_unicode.isprintable():
        CLICK_SONIDO.play()

        # Si está activo Shift o Caps Lock, lo escribo en mayúscula
        if bloc_mayus & (pygame.KMOD_SHIFT | pygame.KMOD_CAPS):
            datos_juego["nombre"] += tecla_unicode.upper()
        else:
            datos_juego["nombre"] += tecla_unicode


def guardar_datos_jugador(
    datos_juego: dict, archivo: str = "./data/Partidas.json"
) -> None:
    guardar_datos = {
        "nombre": datos_juego["nombre"],
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "puntuacion": datos_juego["puntuacion"],
    }

    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            try:
                partidas = json.load(f)
            except json.JSONDecodeError:
                partidas = []

    else:
        partidas = []

    partidas.append(guardar_datos)

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(partidas, f, indent=4, ensure_ascii=False)


def cargar_top_jugadores(archivo="./data/Partidas.json") -> list:
    if not os.path.exists(archivo):
        return []

    with open(archivo, "r", encoding="utf-8") as f:
        try:
            partidas = json.load(f)
        except json.JSONDecodeError:
            return []

    top_10 = sorted(partidas, key=lambda p: p["puntuacion"], reverse=True)[:10]
    return top_10


def aplicar_comodin(comodin: str, datos_juego: dict, lista_preguntas: list) -> bool:
    if comodin == "pasar":
        if not datos_juego.get("comodin_pasar_usado", False):
            datos_juego["indice"] += 1
            if datos_juego["indice"] >= len(lista_preguntas):
                mezclar_lista(lista_preguntas)
                datos_juego["indice"] = 0
            datos_juego["comodin_pasar_usado"] = True
            return True

    elif comodin == "x2":
        if not datos_juego.get("comodin_doble_usado", False):
            datos_juego["x2_activado"] = True
            datos_juego["comodin_doble_usado"] = True
            return True

    elif comodin == "doble_chance":
        if not datos_juego.get("doble_chance_usado", False):
            datos_juego["doble_chance_activada"] = True
            datos_juego["doble_chance_usado"] = True
            datos_juego["respuestas_ocultas"] = []
            return True

    elif comodin == "bomba":
        if not datos_juego.get("comodin_bomba_usado", False):
            pregunta_actual = lista_preguntas[datos_juego["indice"]]
            correcta = pregunta_actual["respuesta_correcta"]
            todas = [1, 2, 3, 4]
            incorrectas = [r for r in todas if r != correcta]

            import random

            visible_incorrecta = random.choice(incorrectas)

            respuestas_a_ocultar = [r for r in incorrectas if r != visible_incorrecta]

            datos_juego["respuestas_ocultadas_bomba"] = respuestas_a_ocultar
            datos_juego["comodin_bomba_usado"] = True
            return True

    return False


def calcular_puntos(datos_juego: dict, es_correcta: bool) -> None:
    if es_correcta:
        puntos = PUNTUACION_ACIERTO
        if datos_juego.get("x2_activado", False):
            puntos *= 2
            datos_juego["x2_activado"] = False
        datos_juego["puntuacion"] += puntos
    else:
        datos_juego["puntuacion"] -= PUNTUACION_ERROR
