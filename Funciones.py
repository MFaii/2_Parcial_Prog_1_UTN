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


# GENERAL
def verificar_respuesta(datos_juego: dict, pregunta: dict, respuesta: int) -> bool:
    if respuesta == pregunta["respuesta_correcta"]:
        datos_juego["puntuacion"] += PUNTUACION_ACIERTO
        retorno = True
    else:
        datos_juego["vidas"] -= 1
        datos_juego["puntuacion"] -= PUNTUACION_ERROR
        retorno = False

    return retorno


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
    pos_y = 115

    for i in range(4):
        boton = crear_elemento_juego(
            "./imgs/textura_respuesta.jpg", ANCHO_BOTON, ALTO_BOTON, 125, pos_y
        )
        pos_y += 80
        lista_botones.append(boton)

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
