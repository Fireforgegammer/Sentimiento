import os
import json
from almacenamiento.guardar import guardar_json

def test_guardar_json_crea_archivo(tmp_path):
    datos = {"test": "ok"}
    nombre_archivo = tmp_path / "test_output.json"
    guardar_json(datos, str(nombre_archivo))
    
    assert os.path.exists(nombre_archivo)
    with open(nombre_archivo, "r") as f:
        contenido = json.load(f)
    assert contenido["test"] == "ok"