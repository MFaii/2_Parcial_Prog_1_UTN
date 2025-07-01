import pygame
from Constantes import *
from Preguntas import *
from Funciones import *

pygame.init()

pygame.display.set_caption("PREGUNTADOS")
icono = pygame.image.load("./imgs/icono.png")
pygame.display.set_icon(icono)

pantalla = pygame.display.set_mode(PANTALLA)
datos_juego = {
    "puntuacion": 0,
    "vidas": CANTIDAD_VIDAS,
    "nombre": "",
    "tiempo_restante": 30,
}
fondo_pantalla = pygame.transform.scale(pygame.image.load("./imgs/fondo.jpg"), PANTALLA)

# Elemento del juego
caja_pregunta = crear_elemento_juego(
    "./imgs/textura_pregunta.jpg", ANCHO_PREGUNTA, ALTO_PREGUNTA, 80, 80
)
boton_respuesta_uno = crear_elemento_juego(
    "./imgs/textura_respuesta.jpg", ANCHO_BOTON, ALTO_BOTON, 125, 245
)
boton_respuesta_dos = crear_elemento_juego(
    "./imgs/textura_respuesta.jpg", ANCHO_BOTON, ALTO_BOTON, 125, 315
)
boton_respuesta_tres = crear_elemento_juego(
    "./imgs/textura_respuesta.jpg", ANCHO_BOTON, ALTO_BOTON, 125, 385
)

mezclar_lista(lista_preguntas)

corriendo = True
reloj = pygame.time.Clock()
evento_tiempo = pygame.USEREVENT
pygame.time.set_timer(evento_tiempo, 1000)


def mostrar_juego(
    pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict
) -> str:
    retorno = "juego"
    pregunta_actual = lista_preguntas[datos_juego["indice"]]

    if datos_juego["vidas"] == 0 or datos_juego["tiempo_restante"] == 0:
        retorno = "menu"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                respuesta = obtener_respuesta_click(
                    boton_respuesta_uno,
                    boton_respuesta_dos,
                    boton_respuesta_tres,
                    evento.pos,
                )
                if respuesta != None:
                    if (
                        verificar_respuesta(datos_juego, pregunta_actual, respuesta)
                        == True
                    ):
                        # Recomiendo sonido de respuesta correcta
                        CLICK_SONIDO.play()
                    else:
                        ERROR_SONIDO.play()
                    datos_juego["indice"] += 1
                    if datos_juego["indice"] == len(lista_preguntas):
                        mezclar_lista(lista_preguntas)
                        datos_juego["indice"] = 0

                    pregunta_actual = cambiar_pregunta(
                        lista_preguntas,
                        datos_juego["indice"],
                        caja_pregunta,
                        boton_respuesta_uno,
                        boton_respuesta_dos,
                        boton_respuesta_tres,
                    )

        elif evento.type == evento_tiempo:
            datos_juego["tiempo_restante"] -= 1

    pantalla.blit(fondo_pantalla, (0, 0))
    pantalla.blit(caja_pregunta["superficie"], caja_pregunta["rectangulo"])
    pantalla.blit(boton_respuesta_uno["superficie"], boton_respuesta_uno["rectangulo"])
    pantalla.blit(boton_respuesta_dos["superficie"], boton_respuesta_dos["rectangulo"])
    pantalla.blit(
        boton_respuesta_tres["superficie"], boton_respuesta_tres["rectangulo"]
    )

    mostrar_texto(
        caja_pregunta["superficie"],
        pregunta_actual["pregunta"],
        (20, 20),
        FUENTE_PREGUNTA,
        COLOR_NEGRO,
    )
    mostrar_texto(
        boton_respuesta_uno["superficie"],
        pregunta_actual["respuesta_1"],
        (20, 20),
        FUENTE_RESPUESTA,
        COLOR_BLANCO,
    )
    mostrar_texto(
        boton_respuesta_dos["superficie"],
        pregunta_actual["respuesta_2"],
        (20, 20),
        FUENTE_RESPUESTA,
        COLOR_BLANCO,
    )
    mostrar_texto(
        boton_respuesta_tres["superficie"],
        pregunta_actual["respuesta_3"],
        (20, 20),
        FUENTE_RESPUESTA,
        COLOR_BLANCO,
    )

    mostrar_texto(pantalla, f"VIDAS: {datos_juego['vidas']}", (10, 10), FUENTE_TEXTO)
    mostrar_texto(
        pantalla, f"PUNTUACION: {datos_juego['puntuacion']}", (10, 40), FUENTE_TEXTO
    )
    mostrar_texto(
        pantalla, f"TIEMPO: {datos_juego['tiempo_restante']} s", (300, 10), FUENTE_TEXTO
    )

    return retorno
