import random
from Constantes import *
import pygame
import json
from datetime import datetime
import os


def mostrar_texto(surface, text, pos, font, color=pygame.Color("black")):
    """
    Muestra texto en una superficie con ajuste automático de línea.

    Args:
        surface: Superficie de Pygame donde se dibuja el texto.
        text: Texto a mostrar.
        pos: Tupla con la posición (x, y) donde empieza el texto.
        font: Fuente utilizada para renderizar el texto.
        color: Color del texto (por defecto negro).
    """
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
    """
    Mezcla aleatoriamente la lista de preguntas.

    Args:
        lista_preguntas: Lista de preguntas a mezclar.
    """
    random.shuffle(lista_preguntas)


# GENERAL
def reiniciar_estadisticas(datos_juego: dict) -> None:
    """
    Reinicia las estadísticas del juego a sus valores iniciales.

    Args:
        datos_juego: Diccionario con los datos del juego.
    """
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
    """
    Verifica si la respuesta del jugador es correcta.

    Args:
        datos_juego: Diccionario con los datos del juego.
        pregunta: Diccionario con los datos de la pregunta.
        respuesta: Respuesta seleccionada por el jugador (1 a 4).

    Returns:
        True si la respuesta es correcta, False en caso contrario.
    """
    return respuesta == pregunta["respuesta_correcta"]


def crear_elemento_juego(
    textura: str, ancho: int, alto: int, pos_x: int, pos_y: int
) -> dict:
    """
    Crea un elemento gráfico del juego con su textura y posición.

    Args:
        textura: Ruta de la imagen.
        ancho: Ancho del elemento.
        alto: Alto del elemento.
        pos_x: Posición X.
        pos_y: Posición Y.

    Returns:
        Diccionario con la superficie y el rectángulo del elemento.
    """
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
    """
    Limpia y actualiza la textura del elemento gráfico.

    Args:
        elemento_juego: Elemento del juego a limpiar.
        textura: Ruta de la nueva imagen.
        ancho: Ancho de la imagen.
        alto: Alto de la imagen.
    """
    elemento_juego["superficie"] = pygame.transform.scale(
        pygame.image.load(textura), (ancho, alto)
    )


def obtener_respuesta_click(lista_respuestas: list, pos_click: tuple):
    """
    Devuelve la opción seleccionada según la posición del click.

    Args:
        lista_respuestas: Lista de botones de respuesta.
        pos_click: Tupla con la posición del click.

    Returns:
        Número de la respuesta seleccionada (1 a 4), o None.
    """
    respuesta = None

    for i in range(len(lista_respuestas)):
        if lista_respuestas[i]["rectangulo"].collidepoint(pos_click):
            respuesta = i + 1

    return respuesta


def cambiar_pregunta(
    lista_preguntas: list, indice: int, caja_pregunta: dict, lista_respuestas: list
) -> dict:
    """
    Cambia la pregunta actual limpiando las superficies y devolviendo la nueva pregunta.

    Args:
        lista_preguntas: Lista de preguntas.
        indice: Índice de la nueva pregunta.
        caja_pregunta: Diccionario con la caja donde se muestra la pregunta.
        lista_respuestas: Lista de botones de respuesta.

    Returns:
        Diccionario con los datos de la nueva pregunta.
    """
    pregunta_actual = lista_preguntas[indice]
    limpiar_superficie(
        caja_pregunta, "./imgs/neon_1.png", ANCHO_PREGUNTA, ALTO_PREGUNTA
    )
    for i in range(len(lista_respuestas)):
        limpiar_superficie(
            lista_respuestas[i], "./imgs/neon_2.png", ANCHO_BOTON, ALTO_BOTON
        )

    return pregunta_actual


def crear_botones_menu() -> list:
    """
    Crea y devuelve los botones del menú principal.

    Returns:
        Lista de diccionarios, cada uno representando un botón.
    """
    lista_botones = []
    cantidad_botones = 4
    espacio = 20
    altura_total = cantidad_botones * ALTO_BOTON + (cantidad_botones - 1) * espacio
    pos_y = (600 - altura_total) // 2
    pos_x = (600 - ANCHO_BOTON) // 2

    for i in range(cantidad_botones):
        boton = crear_elemento_juego(
            "./imgs/neon_2.png", ANCHO_BOTON, ALTO_BOTON, pos_x, pos_y
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
    """
    Crea los botones de respuesta para una pregunta.

    Args:
        textura: Ruta de la imagen de los botones.
        ancho: Ancho de los botones.
        alto: Alto de los botones.
        pos_x: Posición X inicial.
        pos_y: Posición Y inicial.
        cantidad_respuestas: Cantidad de respuestas a crear.

    Returns:
        Lista de diccionarios representando los botones de respuesta.
    """
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
    """
    Maneja la entrada de texto del jugador para escribir su nombre.

    Args:
        cuadro_texto: Cuadro de texto a limpiar si se borra.
        tecla_nombre: Nombre de la tecla presionada.
        tecla_unicode: Carácter correspondiente a la tecla.
        bloc_mayus: Estado de mayúsculas (SHIFT o CAPS).
        datos_juego: Diccionario donde se almacena el nombre.
    """
    # 1. Si se presiona la barra espaciadora
    if tecla_nombre == "space":
        CLICK_SONIDO.play()
        datos_juego["nombre"] += " "

    # 2. Si se presiona la tecla borrar (backspace) y hay texto para borrar
    elif tecla_nombre == "backspace" and len(datos_juego["nombre"]) > 0:
        datos_juego["nombre"] = datos_juego["nombre"][:-1]
        limpiar_superficie(cuadro_texto, "./imgs/neon_2.png", ANCHO_CUADRO, ALTO_CUADRO)

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
    """
    Guarda los datos del jugador actual en un archivo JSON.

    Args:
        datos_juego: Diccionario con los datos del jugador.
        archivo: Ruta del archivo JSON donde se guardarán los datos.
    """
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
    """
    Carga las 10 mejores partidas desde un archivo JSON ordenadas por puntuación.

    Args:
        archivo: Ruta del archivo JSON de donde leer los datos.

    Returns:
        Lista con los 10 mejores puntajes.
    """
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
    """
    Aplica el efecto del comodín indicado si aún no fue usado.

    Args:
        comodin: Nombre del comodín a aplicar.
        datos_juego: Diccionario con los datos del juego.
        lista_preguntas: Lista de preguntas.

    Returns:
        True si el comodín se aplicó correctamente, False si ya fue usado.
    """
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
    """
    Calcula y actualiza la puntuación del jugador dependiendo de si respondió bien o mal.

    Args:
        datos_juego: Diccionario con los datos del juego.
        es_correcta: True si la respuesta fue correcta, False si fue incorrecta.
    """
    if es_correcta:
        puntos = PUNTUACION_ACIERTO
        if datos_juego.get("x2_activado", False):
            puntos *= 2
            datos_juego["x2_activado"] = False
        datos_juego["puntuacion"] += puntos
    else:
        datos_juego["puntuacion"] = max(0, datos_juego["puntuacion"] - PUNTUACION_ERROR)
        datos_juego["vidas"] -= 1


def crear_boton_con_imagen(path_imagen: str, rect: pygame.Rect) -> pygame.Surface:
    """
    Crea un botón a partir de una imagen escalada a un rectángulo dado.

    Args:
        path_imagen (str): Ruta del archivo de imagen a usar como textura del botón.
        rect (pygame.Rect): Objeto Rect que define el tamaño deseado del botón.

    Returns:
        pygame.Surface: Superficie de Pygame con la imagen escalada al tamaño especificado.
    """
    imagen = pygame.image.load(path_imagen)
    return pygame.transform.scale(imagen, (rect.width, rect.height))
