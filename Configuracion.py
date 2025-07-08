import pygame
from Constantes import *
from Funciones import *

pygame.init()

boton_volver = crear_elemento_juego("./imgs/neon_2.png", 120, 50, 10, 10)
boton_suma = crear_elemento_juego("./imgs/mas.webp", 60, 60, 520, 530)
boton_resta = crear_elemento_juego("./imgs/menos.webp", 60, 60, 20, 530)
boton_mute = crear_elemento_juego("./imgs/neon_2.png", 150, 50, 225, 530)

fondo_config = pygame.transform.scale(
    pygame.image.load("./imgs/configuracion_fondo.jpg"), PANTALLA
)


def mostrar_ajustes(
    pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict
) -> str:
    """
    Muestra la pantalla de ajustes y gestiona la interacción con sus botones.

    Args:
        pantalla: Superficie donde se dibujan los elementos de ajustes.
        cola_eventos: Lista de eventos de Pygame.
        datos_juego: Diccionario con los datos del juego (incluye volumen).

    Returns:
        str: Nombre de la siguiente pantalla a mostrar ("ajustes", "menu" o "salir").
    """
    retorno = "ajustes"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_suma["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] <= 95:
                        datos_juego["volumen_musica"] += 5
                        CLICK_SONIDO.play()
                    else:
                        ERROR_SONIDO.play()
                elif boton_resta["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] > 0:
                        datos_juego["volumen_musica"] -= 5
                        CLICK_SONIDO.play()
                    else:
                        ERROR_SONIDO.play()
                elif boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"
                elif boton_mute["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] > 0:
                        datos_juego["volumen_anterior"] = datos_juego["volumen_musica"]
                        datos_juego["volumen_musica"] = 0
                    else:
                        datos_juego["volumen_musica"] = datos_juego.get(
                            "volumen_anterior", 50
                        )

                    pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
                    CLICK_SONIDO.play()

    pantalla.blit(fondo_config, (0, 0))

    pantalla.blit(boton_suma["superficie"], boton_suma["rectangulo"])
    pantalla.blit(boton_resta["superficie"], boton_resta["rectangulo"])
    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])
    pantalla.blit(boton_mute["superficie"], boton_mute["rectangulo"])

    mostrar_texto(
        pantalla,
        f"{datos_juego["volumen_musica"]} %",
        (230, 250),
        FUENTE_VOLUMEN,
        COLOR_BLANCO,
    )
    mostrar_texto(
        boton_volver["superficie"], "VOLVER", (5, 5), FUENTE_RESPUESTA, COLOR_BLANCO
    )
    mostrar_texto(
        boton_mute["superficie"],
        "MUTE",
        (47, 15),
        FUENTE_RESPUESTA,
        COLOR_BLANCO,
    )

    return retorno
