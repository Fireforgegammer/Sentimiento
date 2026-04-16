# 📖 `almacenamiento/leer.py`

🌐 [English](../../en/almacenamiento/leer.md) · [Português](../../pt/almacenamiento/leer.md) · [← Índice](../INDEX.md)

---

## Descripción General

Módulo de lectura de resultados persistidos. Carga un archivo JSON desde el directorio `resultados/` y lo devuelve como diccionario Python, con validación de existencia previa.

---

## Diagrama de Flujo

```
nombre_archivo: str
      │
      ▼
ruta = os.path.join("resultados", nombre_archivo)
      │
      ▼
¿os.path.exists(ruta)?
      │
      ├── No ──► raise FileNotFoundError(
      │              f"El archivo {nombre_archivo} no existe."
      │          ) ❌
      │
     Sí
      │
      ▼
open(ruta, "r", encoding="utf-8")
      │
      ▼
return json.load(f)  ✅
```

---

## Función: `leer_json`

### Signatura

```python
def leer_json(nombre_archivo: str) -> dict
```

### Descripción

Localiza el archivo `nombre_archivo` dentro del directorio `resultados/`, verifica su existencia y lo deserializa como diccionario Python. Falla explícitamente si el archivo no existe en lugar de devolver `None` silenciosamente.

### Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `nombre_archivo` | `str` | Nombre del archivo a leer (ej: `"resultado.json"`) |

### Retorno

| Tipo | Descripción |
|------|-------------|
| `dict` | Contenido del archivo JSON deserializado |

### Excepciones

| Excepción | Condición |
|-----------|-----------|
| `FileNotFoundError` | El archivo no existe en `resultados/` |
| `json.JSONDecodeError` | El archivo existe pero contiene JSON malformado |

### Ejemplo

```python
from almacenamiento.leer import leer_json

datos = leer_json("analisis_manual.json")
print(datos["sentimiento_global"])  # → "positivo"
```

---

## Relación con `guardar.py`

```
guardar_json(datos, "resultado.json")
        │
        ▼  (escribe)
  resultados/resultado.json
        │
        ▼  (lee)
leer_json("resultado.json") → datos
```

---

## Dependencias

| Dependencia | Uso |
|-------------|-----|
| `json` | Deserialización del archivo |
| `os` | Verificación de existencia y construcción de ruta |