import pygame
from Constantes import *
from Funciones import *

pygame.init()

boton_volver = crear_elemento_juego("./imgs/neon_1.png", 100, 40, 10, 10)


def mostrar_rankings(
    pantalla: pygame.Surface,
    cola_eventos: list[pygame.event.Event],
    lista_rankings: list,
) -> str:
    retorno = "rankings"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"

    # pantalla.fill(COLOR_BLANCO)
    fondo_pantalla = pygame.transform.scale(
        pygame.image.load("./imgs/ranking_fondo.png"), PANTALLA
    )
    pantalla.blit(fondo_pantalla, (0, 0))

    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])
    mostrar_texto(
        pantalla, f"TOP 10 JUGADORES", (150, 80), FUENTE_RANKING_TITULO, COLOR_BLANCO
    )

    i = 0
    while i < len(lista_rankings):
        jugador = lista_rankings[i]

        texto = (
            str(i + 1)
            + ". "
            + jugador["nombre"]
            + " - "
            + str(jugador["puntuacion"])
            + " pts - "
            + jugador["fecha"]
        )

        mostrar_texto(
            pantalla, texto, (110, 160 + i * 30), FUENTE_RANKING_JUGADOR, COLOR_BLANCO
        )

        i += 1

    mostrar_texto(
        boton_volver["superficie"], "VOLVER", (5, 5), FUENTE_RESPUESTA, COLOR_BLANCO
    )

    return retorno
