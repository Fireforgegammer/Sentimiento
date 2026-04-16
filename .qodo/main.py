import os
import json
from sentimiento.niveles import analizar_sentimiento_avanzado
from sentimiento.multitexto import analizar_sentimiento_multitexto
from almacenamiento.guardar import guardar_json

def analizar_texto_manual():
    texto = input("\nEscribe el texto a analizar: ")
    if not texto.strip():
        return
    
    print("Procesando...")
    resultado = analizar_sentimiento_avanzado(texto)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    guardar_json(resultado, "analisis_manual.json")

def analizar_archivo_lote():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(base_dir, "textos_a_analizar.txt")
    
    if not os.path.exists(ruta):
        print(f"Error: No existe el archivo {ruta}")
        return

    with open(ruta, "r", encoding="utf-8") as f:
        lineas = [l.strip() for l in f if l.strip()]

    if not lineas:
        print("El archivo está vacío.")
        return

    print(f"Analizando {len(lineas)} textos...")
    resultado = analizar_sentimiento_multitexto(lineas)
    guardar_json(resultado, "resultado_lote.json")
    
    stats = resultado["estadisticas"]
    print(f"\nResumen: {stats['positivos']} Positivos, {stats['negativos']} Negativos")

def main():
    print("--- SISTEMA DE ANÁLISIS DE SENTIMIENTO ---")
    print("1. Analizar un texto manualmente")
    print("2. Analizar archivo 'textos_a_analizar.txt'")
    
    opcion = input("\nSelecciona una opción (1 o 2): ")
    
    if opcion == "1":
        analizar_texto_manual()
    elif opcion == "2":
        analizar_archivo_lote()
    else:
        print("Opción no válida.")

if __name__ == "__main__":
    main()