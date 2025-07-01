import random
from Constantes import *
import pygame


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


def obtener_respuesta_click(
    boton_respuesta_uno: dict,
    boton_respuesta_dos: dict,
    boton_respuesta_tres: dict,
    pos_click: tuple,
):
    lista_aux = [
        boton_respuesta_uno["rectangulo"],
        boton_respuesta_dos["rectangulo"],
        boton_respuesta_tres["rectangulo"],
    ]
    respuesta = None

    for i in range(len(lista_aux)):
        if lista_aux[i].collidepoint(pos_click):
            respuesta = i + 1

    return respuesta


def cambiar_pregunta(
    lista_preguntas: list,
    indice: int,
    caja_pregunta: dict,
    boton_respuesta_uno: dict,
    boton_respuesta_dos: dict,
    boton_respuesta_tres: dict,
) -> dict:
    pregunta_actual = lista_preguntas[indice]
    limpiar_superficie(
        caja_pregunta, "./imgs/textura_pregunta.jpg", ANCHO_PREGUNTA, ALTO_PREGUNTA
    )
    limpiar_superficie(
        boton_respuesta_uno, "./imgs/textura_respuesta.jpg", ANCHO_BOTON, ALTO_BOTON
    )
    limpiar_superficie(
        boton_respuesta_dos, "./imgs/textura_respuesta.jpg", ANCHO_BOTON, ALTO_BOTON
    )
    limpiar_superficie(
        boton_respuesta_tres, "./imgs/textura_respuesta.jpg", ANCHO_BOTON, ALTO_BOTON
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
