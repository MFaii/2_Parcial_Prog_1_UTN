import pygame
from Constantes import *
from Funciones import *

pygame.init()

boton_suma = crear_elemento_juego("./imgs/mas.webp", 60, 60, 420, 200)
boton_resta = crear_elemento_juego("./imgs/menos.webp", 60, 60, 20, 200)
boton_volver = crear_elemento_juego("./imgs/textura_respuesta.jpg", 100, 40, 10, 10)
boton_mute = crear_elemento_juego("./imgs/textura_respuesta.jpg", 100, 100, 200, 400)


def mostrar_ajustes(
    pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict
) -> str:
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
                        datos_juego["volumen_musica"] = datos_juego.get("volumen_anterior", 50)

                    pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
                    CLICK_SONIDO.play()


    pantalla.fill(COLOR_BLANCO)

    pantalla.blit(boton_suma["superficie"], boton_suma["rectangulo"])
    pantalla.blit(boton_resta["superficie"], boton_resta["rectangulo"])
    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])
    pantalla.blit(boton_mute["superficie"], boton_mute["rectangulo"])


    mostrar_texto(
        pantalla,
        f"{datos_juego["volumen_musica"]} %",
        (200, 200),
        FUENTE_VOLUMEN,
        COLOR_NEGRO,
    )
    mostrar_texto(
        boton_volver["superficie"], "VOLVER", (5, 5), FUENTE_RESPUESTA, COLOR_BLANCO
    )
    texto_mute = "DESMUTEAR" if datos_juego["volumen_musica"] == 0 else "MUTE"
    mostrar_texto(
        boton_mute["superficie"],
        texto_mute,
        (10, 5),
        FUENTE_RESPUESTA,
        COLOR_BLANCO,
    )


    return retorno
