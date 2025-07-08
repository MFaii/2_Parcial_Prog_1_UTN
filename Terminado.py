import pygame
from Constantes import *
from Funciones import *
import json
from datetime import datetime
import os
from Validaciones import *

pygame.init()
cuadro_texto = crear_elemento_juego(
    "./imgs/neon_2.png", ANCHO_CUADRO, ALTO_CUADRO, 200, 200
)
imagen_boton_guardar = crear_boton_con_imagen("./imgs/neon_1.png", BOTON_GUARDAR)


def mostrar_fin_juego(
    pantalla: pygame.Surface,
    cola_eventos: list[pygame.event.Event],
    datos_juego: dict,
    lista_rankings: list,
    ya_guardado: dict,
) -> str:
    retorno = "terminado"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # Cuando ingrese el nombre deberian haber botones que me permitan guardar los cambios

            if BOTON_GUARDAR.collidepoint(evento.pos):
                nombre_ingresado = datos_juego["nombre"].strip()

                if not nombre_valido(nombre_ingresado):
                    print("Ingresá un nombre válido (letras, espacios, números).")

                elif not ya_guardado["guardado"]:
                    guardar_datos_jugador(datos_juego)
                    ya_guardado["guardado"] = True
                    print("Datos guardados correctamente")

                else:
                    print("Ya guardaste la partida")

        elif evento.type == pygame.KEYDOWN:
            tecla_unicode = evento.unicode
            tecla_nombre = pygame.key.name(evento.key)

            manejar_texto(
                cuadro_texto,
                tecla_nombre,
                tecla_unicode,
                pygame.key.get_mods(),
                datos_juego,
            )

    # TODO:Metanle un fondo de pantalla al game over

    fondo_pantalla = pygame.transform.scale(pygame.image.load("./imgs/3.png"), PANTALLA)
    pantalla.blit(fondo_pantalla, (0, 0))

    # pantalla.fill(COLOR_BLANCO)
    pantalla.blit(cuadro_texto["superficie"], cuadro_texto["rectangulo"])
    mostrar_texto(
        pantalla,
        f"Usted obtuvo: {datos_juego["puntuacion"]} puntos",
        (250, 100),
        FUENTE_TEXTO,
        COLOR_BLANCO,
    )

    if datos_juego["nombre"] != "":
        limpiar_superficie(cuadro_texto, "./imgs/neon_2.png", ANCHO_CUADRO, ALTO_CUADRO)
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

    pantalla.blit(imagen_boton_guardar, (BOTON_GUARDAR.x, BOTON_GUARDAR.y))
    mostrar_texto(
        pantalla,
        "Guardar partida",
        (BOTON_GUARDAR.x + 20, BOTON_GUARDAR.y + 10),
        FUENTE_RESPUESTA,
        COLOR_BLANCO,
    )

    return retorno
