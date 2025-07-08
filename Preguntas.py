import csv

def cargar_preguntas_csv(ruta="data/Preguntas.csv") -> list:
    """
    Carga las preguntas desde un archivo CSV y las devuelve como una lista de diccionarios.

    Args:
        ruta (str): Ruta al archivo CSV con las preguntas. Por defecto: "data/Preguntas.csv".

    Returns:
        list: Lista de diccionarios con claves "pregunta", "respuesta_1", ..., "respuesta_4", "respuesta_correcta".
    """
    preguntas = []
    with open(ruta, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            preguntas.append({
                "pregunta": fila["pregunta"],
                "respuesta_1": fila["respuesta_1"],
                "respuesta_2": fila["respuesta_2"],
                "respuesta_3": fila["respuesta_3"],
                "respuesta_4": fila["respuesta_4"],
                "respuesta_correcta": int(fila["respuesta_correcta"])
            })
    return preguntas

