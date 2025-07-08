
# 🎮 Preguntados - Juego con Pygame

> Proyecto académico desarrollado como entrega del segundo parcial de **Programación I (UTN)**.  
> El objetivo fue crear un juego interactivo con interfaz gráfica, simulando el clásico juego *Preguntados*, aplicando lógica, estructuras de datos, manejo de archivos y eventos.



## 📌 Requisitos
- Python 3.10 o superior
- Pygame (`pip install pygame`)
## 🧠 Objetivos del Proyecto
- Aplicar la programación estructurada y modular en Python.
- Manejar archivos externos como CSV (preguntas) y JSON (partidas).
- Desarrollar una interfaz gráfica con eventos utilizando **Pygame**.
- Implementar lógica de juego, rankings, validaciones y comodines.
## 🕹️ Características principales
✅ Interfaz gráfica funcional con botones y animaciones  
✅ Carga dinámica de preguntas desde un archivo `.csv`  
✅ Guardado de partidas en un archivo `.json`  
✅ Ranking de los 10 mejores jugadores  
✅ Tiempo límite para responder  
✅ Sistema de puntuación y vidas  
✅ Validaciones del nombre del jugador  
✅ Ingreso de nombre personalizado con input interactivo  
✅ Sistema de **comodines**:
- 🎯 *Pasar pregunta*: Salta la pregunta actual.
- ✌️ *Doble chance*: Permite dos intentos si se falla la primera.
- ✖️ *Bomba*: Elimina dos respuestas incorrectas aleatoriamente.
- 🔥 *X2 puntos*: Duplica los puntos de la próxima respuesta correcta.
## 📂 Estructura del Proyecto
```bash
Preguntados/
├── data/
│   ├── Preguntas.csv         # Preguntas cargadas
│   └── Partidas.json         # Partidas y ranking
├── imgs/                     # Iconos, fondos, botones
│   ├── icono.png
│   ├── fondo.png
│   ├── neon_1.png
│   └── ...
├── Constantes.py             # Variables globales y colores
├── Funciones.py              # Funciones auxiliares y lógicas
├── Validaciones.py           # Validación de datos (nombre)
├── main.py                   # Entrada principal del juego
├── sonidos/                  # Efectos de sonido
│   └── click.wav, error.wav
└── README.md                 # Este archivo
```
## ▶️ Cómo ejecutar
### 1. Cloná el repositorio:
```
git clone https://github.com/MFaii/Preguntados-Pygame.git
```
### 2. Instalá las dependencias:
```
pip install pygame
```
### 3.  Ejecutá el juego:
```
python main.py
```
## 💻 Autores

- [@Maximiliano Failla](https://github.com/MFaii)
- [@Agustin Escalante](https://github.com/AgustinEscalante)


## 📚 Créditos
>Este juego fue realizado en el marco de la materia Programación I - UTN.
Las imágenes y sonidos utilizados tienen fines exclusivamente educativos.
