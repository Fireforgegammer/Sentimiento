---

# 🔗 `tests/integration/test_storage.py` — Tests de Integración

---

## Descripción General

Pruebas de integración del módulo de almacenamiento. Verifican que `guardar_json` crea el archivo correctamente y que el contenido escrito es el esperado.

---

## Test: `test_guardar_json_crea_archivo`

### Signatura

```python
def test_guardar_json_crea_archivo(tmp_path) -> None
```

### Descripción

Llama a `guardar_json` con un diccionario simple y una ruta en el directorio temporal, y verifica que el archivo existe y contiene el valor correcto.

### Flujo

```
datos = {"test": "ok"}
nombre_archivo = tmp_path / "test_output.json"
guardar_json(datos, str(nombre_archivo))
    │
    ▼
assert os.path.exists(nombre_archivo)
    │
    ▼
contenido = json.load(f)
assert contenido["test"] == "ok"
```

