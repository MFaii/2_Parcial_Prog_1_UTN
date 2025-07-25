import pygame
from Constantes import *
from Preguntas import *
from Funciones import *

pygame.init()

pygame.display.set_caption("PREGUNTADOS")
icono = pygame.image.load("./imgs/icono.png")
pygame.display.set_icon(icono)

pantalla = pygame.display.set_mode(PANTALLA)
fondo_pantalla = pygame.transform.scale(pygame.image.load("./imgs/3.png"), PANTALLA)
corazon_img = pygame.image.load("./imgs/corazon.png")
corazon_img = pygame.transform.scale(corazon_img, (30, 30))


# -------------------------
# CENTRADO Y SETUP INICIAL
# -------------------------

lista_preguntas = cargar_preguntas_csv()
mezclar_lista(lista_preguntas)

caja_pregunta = crear_elemento_juego(
    "./imgs/neon_1.png",
    ANCHO_PREGUNTA,
    ALTO_PREGUNTA,
    (600 - ANCHO_PREGUNTA) // 2,  # Centrado horizontal
    80,
)

lista_respuestas = crear_respuestas(
    "./imgs/neon_2.png",
    ANCHO_BOTON,
    ALTO_BOTON,
    (600 - ANCHO_BOTON) // 2,  # Centrado horizontal
    245,  # Primer respuesta
    4,  # Cantidad de respuestas
)


evento_tiempo = pygame.USEREVENT
pygame.time.set_timer(evento_tiempo, 1000)

# -------------------------------
# FUNCION PRINCIPAL DEL JUEGO
# -------------------------------


def mostrar_juego(
    pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict
) -> str:
    """
    Muestra la pantalla principal del juego, procesa eventos y actualiza el estado del juego.

    Args:
        pantalla: Superficie principal del juego.
        cola_eventos: Lista de eventos Pygame.
        datos_juego: Diccionario con el estado actual del juego.

    Returns:
        str: Nombre del estado siguiente ("juego", "terminado" o "salir").
    """
    retorno = "juego"
    pregunta_actual = lista_preguntas[datos_juego["indice"]]

    if datos_juego["vidas"] == 0 or datos_juego["tiempo_restante"] == 0:
        return "terminado"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            return "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if BOTON_COMODIN.collidepoint(evento.pos):
                    if aplicar_comodin("pasar", datos_juego, lista_preguntas):
                        pregunta_actual = cambiar_pregunta(
                            lista_preguntas,
                            datos_juego["indice"],
                            caja_pregunta,
                            lista_respuestas,
                        )
                        CLICK_SONIDO.play()

                elif BOTON_X2.collidepoint(evento.pos):
                    if aplicar_comodin("x2", datos_juego, lista_preguntas):
                        CLICK_SONIDO.play()

                elif BOTON_DOBLE_CHANCE.collidepoint(evento.pos):
                    if aplicar_comodin("doble_chance", datos_juego, lista_preguntas):
                        CLICK_SONIDO.play()

                elif BOTON_BOMBA.collidepoint(evento.pos):
                    if aplicar_comodin("bomba", datos_juego, lista_preguntas):
                        CLICK_SONIDO.play()

                else:
                    respuesta = obtener_respuesta_click(lista_respuestas, evento.pos)

                    if respuesta is not None:
                        if respuesta in datos_juego.get("respuestas_ocultas", []):
                            continue

                        es_correcta = verificar_respuesta(
                            datos_juego, pregunta_actual, respuesta
                        )

                        if es_correcta:
                            calcular_puntos(datos_juego, True)
                            CLICK_SONIDO.play()
                            datos_juego["doble_chance_activada"] = False
                            datos_juego["intento_extra"] = False
                            datos_juego["respuestas_ocultas"] = []
                            datos_juego["indice"] += 1
                            datos_juego["respuestas_ocultadas_bomba"] = []

                        elif datos_juego.get(
                            "doble_chance_activada", False
                        ) and not datos_juego.get("intento_extra", False):
                            datos_juego["intento_extra"] = True
                            datos_juego["respuestas_ocultas"].append(respuesta)
                            ERROR_SONIDO.play()

                        else:
                            calcular_puntos(datos_juego, False)
                            ERROR_SONIDO.play()
                            datos_juego["doble_chance_activada"] = False
                            datos_juego["intento_extra"] = False
                            datos_juego["respuestas_ocultas"] = []
                            datos_juego["indice"] += 1

                        if datos_juego["indice"] == len(lista_preguntas):
                            mezclar_lista(lista_preguntas)
                            datos_juego["indice"] = 0

                        pregunta_actual = cambiar_pregunta(
                            lista_preguntas,
                            datos_juego["indice"],
                            caja_pregunta,
                            lista_respuestas,
                        )
                        if datos_juego["indice"] == len(lista_preguntas):
                            mezclar_lista(lista_preguntas)
                            datos_juego["indice"] = 0

                        pregunta_actual = cambiar_pregunta(
                            lista_preguntas,
                            datos_juego["indice"],
                            caja_pregunta,
                            lista_respuestas,
                        )

        elif evento.type == evento_tiempo:
            datos_juego["tiempo_restante"] -= 1

    # DIBUJO
    pantalla.blit(fondo_pantalla, (0, 0))
    pantalla.blit(caja_pregunta["superficie"], caja_pregunta["rectangulo"])

    for i in range(len(lista_respuestas)):
        if (i + 1) in datos_juego.get("respuestas_ocultadas_bomba", []):
            continue
        if (i + 1) not in datos_juego.get("respuestas_ocultas", []):
            pantalla.blit(
                lista_respuestas[i]["superficie"], lista_respuestas[i]["rectangulo"]
            )
            mostrar_texto(
                lista_respuestas[i]["superficie"],
                pregunta_actual[f"respuesta_{i + 1}"],
                (20, 20),
                FUENTE_RESPUESTA,
                COLOR_BLANCO,
            )

    mostrar_texto(
        caja_pregunta["superficie"],
        pregunta_actual["pregunta"],
        (20, 20),
        FUENTE_PREGUNTA,
        COLOR_BLANCO,
    )

    if not datos_juego.get("comodin_pasar_usado", True):
        pygame.draw.rect(pantalla, (50, 150, 255), BOTON_COMODIN)
        mostrar_texto(
            pantalla,
            "Pasar pregunta",
            (BOTON_COMODIN.x + 10, BOTON_COMODIN.y + 10),
            FUENTE_CAMBIO_PREGUNTA,
            COLOR_BLANCO,
        )

    if not datos_juego.get("comodin_doble_usado", True):
        pygame.draw.rect(pantalla, (255, 165, 0), BOTON_X2)
        mostrar_texto(
            pantalla,
            "X2 puntos",
            (BOTON_X2.x + 10, BOTON_X2.y + 10),
            FUENTE_CAMBIO_PREGUNTA,
            COLOR_BLANCO,
        )

    if not datos_juego.get("comodin_doble_chance_usado", True):
        pygame.draw.rect(pantalla, (0, 200, 100), BOTON_DOBLE_CHANCE)
        mostrar_texto(
            pantalla,
            "Doble chance",
            (BOTON_DOBLE_CHANCE.x + 10, BOTON_DOBLE_CHANCE.y + 10),
            FUENTE_CAMBIO_PREGUNTA,
            COLOR_BLANCO,
        )

    if not datos_juego.get("comodin_bomba_usado", True):
        pygame.draw.rect(pantalla, (200, 0, 0), BOTON_BOMBA)
        mostrar_texto(
            pantalla,
            "Bomba",
            (BOTON_BOMBA.x + 40, BOTON_BOMBA.y + 10),
            FUENTE_CAMBIO_PREGUNTA,
            COLOR_BLANCO,
        )

    for i in range(datos_juego["vidas"]):
        pantalla.blit(corazon_img, (10 + i * 35, 10))

    mostrar_texto(
        pantalla,
        f"PUNTUACION: {datos_juego['puntuacion']}",
        (10, 40),
        FUENTE_TEXTO,
        COLOR_BLANCO,
    )
    mostrar_texto(
        pantalla,
        f"{datos_juego['tiempo_restante']}",
        (PANTALLA[0] - 100, 10),
        FUENTE_TIEMPO,
        COLOR_BLANCO,
    )
    mostrar_texto(pantalla, "COMODINES", (440, 350), FUENTE_TEXTO, COLOR_BLANCO)

    return retorno
