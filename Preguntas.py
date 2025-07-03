import csv

def cargar_preguntas_csv(ruta="data/Preguntas.csv") -> list:
    preguntas = []
    with open(ruta, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            preguntas.append({
                "pregunta": fila["pregunta"],
                "respuesta_1": fila["respuesta_1"],
                "respuesta_2": fila["respuesta_2"],
                "respuesta_3": fila["respuesta_3"],
                "respuesta_correcta": int(fila["respuesta_correcta"])
            })
    return preguntas

