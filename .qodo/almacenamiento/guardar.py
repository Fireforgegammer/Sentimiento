import json
import os

def guardar_json(datos: dict, nombre_archivo: str):
    ruta = os.path.join("resultados", nombre_archivo)
    
    os.makedirs("resultados", exist_ok=True)
    
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    
    return ruta