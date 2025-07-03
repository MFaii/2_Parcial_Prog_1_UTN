import pygame
from Constantes import *
from Funciones import *

pygame.init()
cuadro_texto = crear_elemento_juego(
    "./imgs/textura_respuesta.jpg", ANCHO_CUADRO, ALTO_CUADRO, 200, 200
)


def mostrar_fin_juego(
    pantalla: pygame.Surface,
    cola_eventos: list[pygame.event.Event],
    datos_juego: dict,
    lista_rankings: list,
) -> str:
    retorno = "terminado"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # Cuando ingrese el nombre deberian haber botones que me permitan guardar los cambios
            pass
        elif evento.type == pygame.KEYDOWN:
            tecla_presionada = pygame.key.name(evento.key)
            bloc_mayus = pygame.key.get_mods()

            manejar_texto(cuadro_texto, tecla_presionada, bloc_mayus, datos_juego)

    # Metanle un fondo de pantalla al game over
    pantalla.fill(COLOR_BLANCO)
    pantalla.blit(cuadro_texto["superficie"], cuadro_texto["rectangulo"])
    mostrar_texto(
        pantalla,
        f"Usted obtuvo: {datos_juego["puntuacion"]} puntos",
        (250, 100),
        FUENTE_TEXTO,
        COLOR_NEGRO,
    )

    if datos_juego["nombre"] != "":
        limpiar_superficie(
            cuadro_texto, "./imgs/textura_respuesta.jpg", ANCHO_CUADRO, ALTO_CUADRO
        )
        mostrar_texto(
            cuadro_texto["superficie"],
            f"{datos_juego["nombre"]}",
            (10, 0),
            FUENTE_CUADRO_TEXTO,
            COLOR_BLANCO,
        )

        if random.randint(1, 2) == 1:
            mostrar_texto(
                cuadro_texto["superficie"],
                f"{datos_juego["nombre"]}|",
                (10, 0),
                FUENTE_CUADRO_TEXTO,
                COLOR_BLANCO,
            )

    else:
        mostrar_texto(
            cuadro_texto["superficie"],
            "INGRESE SU NOMBRE",
            (10, 15),
            FUENTE_RESPUESTA,
            "#736767",
        )

    return retorno
