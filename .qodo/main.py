import json
from sentimiento.niveles import (
    analizar_sentimiento_basico, 
    analizar_sentimiento_intermedio, 
    analizar_sentimiento_avanzado
)
from sentimiento.multitexto import analizar_sentimiento_multitexto
from almacenamiento.guardar import guardar_json

def ejecutar_proyecto():
    texto_prueba = "El producto llegó rápido, pero la calidad no es lo que esperaba. La verdad, estoy un poco decepcionado."
    
    print("Ejecutando análisis individual...")
    res_basico = analizar_sentimiento_basico(texto_prueba)
    res_intermedio = analizar_sentimiento_intermedio(texto_prueba)
    res_avanzado = analizar_sentimiento_avanzado(texto_prueba)

    reseñas = [
        "Me encantó este producto, súper recomendado",
        "Regular, cumple pero no es nada del otro mundo",
        "Horrible, no compren esto, es una estafa"
    ]
    
    print("Ejecutando análisis de lote...")
    res_multiple = analizar_sentimiento_multitexto(reseñas)

    print("Guardando resultados...")
    guardar_json(res_avanzado, "analisis_individual.json")
    guardar_json(res_multiple, "analisis_lote.json")
    
    print("Proceso finalizado. Archivos generados en la carpeta 'resultados/'.")

if __name__ == "__main__":
    ejecutar_proyecto()