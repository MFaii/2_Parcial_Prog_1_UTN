import pygame
from Constantes import *
from Menu import *
from Juego import *
from Configuracion import *
from Rankings import *
from Terminado import *

pygame.init()
pygame.display.set_caption("PREGUNTADOS")
icono = pygame.image.load("./imgs/icono.png")
pygame.display.set_icon(icono)
pantalla = pygame.display.set_mode(PANTALLA)
datos_juego = {
    "puntuacion": 0,
    "vidas": CANTIDAD_VIDAS,
    "aciertos_consecutivos": 0,
    "nombre": "",
    "tiempo_restante": CANTIDAD_TIEMPO,
    "indice": 0,
    "volumen_musica": 5,
    "volumen_anterior": 50,
    # Comodines
    # Pasar
    "comodin_pasar_usado": False,
    # x2 puntos
    "comodin_doble_usado": False,
    "x2_activado": False,
    # Doble chance
    "comodin_doble_chance": False,
    "doble_chance_activada": False,
    "intento_extra": False,
    "respuestas_ocultas": [],
    # Bomba
    "comodin_bomba_usado": False,
    "respuestas_ocultadas_bomba": [],
}
corriendo = True
reloj = pygame.time.Clock()
bandera_musica = False
ventana_actual = "menu"

# Ustedes la van a cargar del json
lista_rankings = []
ya_guardado = {"guardado": False}

while corriendo:
    reloj.tick(FPS)
    cola_eventos = pygame.event.get()

    if ventana_actual == "menu":
        if bandera_musica == True:
            pygame.mixer.music.stop()
            bandera_musica = False
        reiniciar_estadisticas(datos_juego)
        # SOLO SI HACEMOS QUE SE REINICIE SOLO
        # ya_guardado["guardado"] = False
        ventana_actual = mostrar_menu(pantalla, cola_eventos)
    elif ventana_actual == "juego":
        porcentaje_volumen = datos_juego["volumen_musica"] / 100

        if bandera_musica == False:
            pygame.mixer.music.load("./sounds/musica.mp3")
            pygame.mixer.music.set_volume(porcentaje_volumen)
            pygame.mixer.music.play(-1)
            bandera_musica = True

        ventana_actual = mostrar_juego(pantalla, cola_eventos, datos_juego)
    elif ventana_actual == "salir":
        corriendo = False
    elif ventana_actual == "ajustes":
        ventana_actual = mostrar_ajustes(pantalla, cola_eventos, datos_juego)
    elif ventana_actual == "rankings":
        lista_rankings = cargar_top_jugadores()
        ventana_actual = mostrar_rankings(pantalla, cola_eventos, lista_rankings)
    elif ventana_actual == "terminado":
        ventana_actual = mostrar_fin_juego(
            pantalla, cola_eventos, datos_juego, lista_rankings, ya_guardado
        )

    # print(ventana_actual)
    pygame.display.flip()

pygame.quit()
