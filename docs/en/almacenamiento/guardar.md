# 💾 `almacenamiento/guardar.py`

[Español](../../es/almacenamiento/guardar.md) · 🌐 English · [Português](../../pt/almacenamiento/guardar.md) · [← Index](../INDEX.md)

---

## Overview

Results writing module. Persists any Python dictionary as a formatted JSON file inside the `resultados/` directory, creating it if it doesn't exist.

---

## Flow Diagram

```
datos: dict, nombre_archivo: str
          │
          ▼
path = os.path.join("resultados", nombre_archivo)
          │
          ▼
os.makedirs("resultados", exist_ok=True)
          │
          ▼
open(path, "w", encoding="utf-8")
          │
          ▼
json.dump(datos, f, indent=4, ensure_ascii=False)
          │
          ▼
return path  ✅
```

---

## Function: `guardar_json`

### Signature

```python
def guardar_json(datos: dict, nombre_archivo: str) -> str
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `datos` | `dict` | Dictionary to serialize |
| `nombre_archivo` | `str` | Target filename with extension (e.g. `"result.json"`) |

### Return

| Type | Description |
|------|-------------|
| `str` | Full path of the created file (e.g. `"resultados/result.json"`) |

### Exceptions

| Exception | Condition |
|-----------|-----------|
| `TypeError` | `datos` contains non-serializable types |
| `OSError` | No write permissions on the directory |

---

# 📖 `almacenamiento/leer.py`

[Español](../../es/almacenamiento/leer.md) · 🌐 English · [Português](../../pt/almacenamiento/leer.md) · [← Index](../INDEX.md)

---

## Overview

Results reading module. Loads a JSON file from `resultados/` and returns it as a Python dict, with existence validation.

---

## Flow Diagram

```
nombre_archivo: str
      │
      ▼
path = os.path.join("resultados", nombre_archivo)
      │
      ▼
os.path.exists(path)?
      │
      ├── No → raise FileNotFoundError ❌
      │
     Yes
      │
      ▼
open(path, "r", encoding="utf-8")
      │
      ▼
return json.load(f)  ✅
```

---

## Function: `leer_json`

### Signature

```python
def leer_json(nombre_archivo: str) -> dict
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `nombre_archivo` | `str` | Filename to read (e.g. `"result.json"`) |

### Return

| Type | Description |
|------|-------------|
| `dict` | Deserialized JSON file content |

### Exceptions

| Exception | Condition |
|-----------|-----------|
| `FileNotFoundError` | File does not exist in `resultados/` |
| `json.JSONDecodeError` | File exists but contains malformed JSON |