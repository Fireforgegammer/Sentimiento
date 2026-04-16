import json
import os

def leer_json(nombre_archivo: str) -> dict:
    ruta = os.path.join("resultados", nombre_archivo)
    
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"El archivo {nombre_archivo} no existe.")
        
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)