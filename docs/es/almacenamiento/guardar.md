# 💾 `almacenamiento/guardar.py`

🌐 [English](../../en/almacenamiento/guardar.md) · [Português](../../pt/almacenamiento/guardar.md) · [← Índice](../INDEX.md)

---

## Descripción General

Módulo de escritura de resultados. Persiste cualquier diccionario Python como archivo JSON formateado dentro del directorio `resultados/`, creándolo si no existe.

---

## Diagrama de Flujo

```
datos: dict, nombre_archivo: str
          │
          ▼
ruta = os.path.join("resultados", nombre_archivo)
          │
          ▼
os.makedirs("resultados", exist_ok=True)
    ┌─────┴──────┐
    │             │
¿Ya existe?   No existe
    │             │
    └──── Continúa sin error ──┘
          │
          ▼
open(ruta, "w", encoding="utf-8")
          │
          ▼
json.dump(datos, f, indent=4, ensure_ascii=False)
          │
          ▼
return ruta  ✅
```

---

## Función: `guardar_json`

### Signatura

```python
def guardar_json(datos: dict, nombre_archivo: str) -> str
```

### Descripción

Serializa `datos` como JSON indentado (4 espacios) y lo escribe en `resultados/<nombre_archivo>`. Garantiza que el directorio `resultados/` existe antes de escribir. Preserva caracteres Unicode (español, emojis, etc.) gracias a `ensure_ascii=False`.

### Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `datos` | `dict` | Diccionario a serializar. Debe ser serializable por `json.dump`. |
| `nombre_archivo` | `str` | Nombre del archivo destino, incluyendo extensión (ej: `"resultado.json"`). |

### Retorno

| Tipo | Descripción |
|------|-------------|
| `str` | Ruta completa del archivo creado (ej: `"resultados/resultado.json"`) |

### Excepciones posibles

| Excepción | Condición |
|-----------|-----------|
| `TypeError` | `datos` contiene tipos no serializables (ej: objetos personalizados sin `__dict__`) |
| `OSError` | Sin permisos de escritura en el directorio |

### Ejemplo

```python
from almacenamiento.guardar import guardar_json

resultado = {"sentimiento": "positivo", "polaridad": 0.8}
ruta = guardar_json(resultado, "mi_analisis.json")
print(ruta)  # → "resultados/mi_analisis.json"
```

**Contenido del archivo generado:**
```json
{
    "sentimiento": "positivo",
    "polaridad": 0.8
}
```

---

## Dependencias

| Dependencia | Uso |
|-------------|-----|
| `json` | Serialización del diccionario |
| `os` | Creación de directorio y construcción de rutas |