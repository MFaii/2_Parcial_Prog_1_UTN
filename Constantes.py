import pygame

pygame.init()

COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_VERDE = (0, 255, 0)
COLOR_ROJO = (255, 0, 0)
COLOR_AZUL = (0, 0, 255)
COLOR_VIOLETA = (134, 23, 219)
ANCHO = 600
ALTO = 600
PANTALLA = (ANCHO, ALTO)
FPS = 30

BOTON_JUGAR = 0
BOTON_CONFIG = 1
BOTON_PUNTUACIONES = 2
BOTON_SALIR = 3

ANCHO_PREGUNTA = 350
ALTO_PREGUNTA = 150
ANCHO_BOTON = 250
ALTO_BOTON = 60
ANCHO_CUADRO = 250
ALTO_CUADRO = 50

TAMAÑO_BOTON_VOLUMEN = (60, 60)
TAMAÑO_BOTON_VOLVER = (100, 40)
FUENTE_TIEMPO = pygame.font.SysFont("Arial", 60, bold=True)
CLICK_SONIDO = pygame.mixer.Sound("./sounds/click.mp3")
ERROR_SONIDO = pygame.mixer.Sound("./sounds/error.mp3")
FUENTE_PREGUNTA = pygame.font.SysFont("Arial", 30, True)
FUENTE_RESPUESTA = pygame.font.SysFont("Arial", 20, True)
FUENTE_TEXTO = pygame.font.SysFont("Arial", 25, True)
FUENTE_VOLUMEN = pygame.font.SysFont("Arial", 100, True)
FUENTE_CUADRO_TEXTO = pygame.font.SysFont("Arial", 40, True)
FUENTE_CAMBIO_PREGUNTA = pygame.font.SysFont("Arial", 18)
FUENTE_RANKING_TITULO = pygame.font.SysFont("Arial", 30, True)
FUENTE_RANKING_JUGADOR = pygame.font.SysFont("Arial", 15, True)

BOTON_JUGAR = 0

CANTIDAD_VIDAS = 5
PUNTUACION_ACIERTO = 100
PUNTUACION_ERROR = 25
CANTIDAD_TIEMPO = 30

BOTON_GUARDAR = pygame.Rect(300, 350, 200, 50)
BOTON_COMODIN = pygame.Rect(450, 400, 140, 40)
BOTON_DOBLE_CHANCE = pygame.Rect(450, 500, 140, 40)
BOTON_X2 = pygame.Rect(450, 450, 140, 40)
BOTON_BOMBA = pygame.Rect(450, 550, 140, 40)
FUENTE_RESPUESTA_CHICA = pygame.font.SysFont("Arial", 18)
