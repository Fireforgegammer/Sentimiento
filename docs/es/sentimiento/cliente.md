# 🔌 `sentimiento/cliente.py`

🌐 [English](../../en/sentimiento/cliente.md) · [Português](../../pt/sentimiento/cliente.md) · [← Índice](../INDEX.md)

---

## Descripción General

Módulo de inicialización del cliente de la API de Groq. Se encarga de leer la clave de API desde las variables de entorno (cargadas desde `.env`) y retornar una instancia configurada de `Groq`, lista para ser importada por otros módulos.

---

## Diagrama de Flujo

```
Carga del módulo
      │
      ▼
BASE_DIR = Path(__file__).resolve().parent.parent
      │
      ▼
load_dotenv(os.path.join(BASE_DIR, ".env"))
      │
      ▼
client = obtener_cliente()
      │
      ▼
  obtener_cliente()
      │
      ▼
api_key = os.getenv("GROQ_API_KEY")
      │
      ├── api_key es None?
      │       │ Sí ──► raise ValueError("GROQ_API_KEY no encontrada") ❌
      │       │
      │      No
      │       │
      ▼
return Groq(api_key=api_key) ✅
```

---

## Variables del Módulo

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `BASE_DIR` | `Path` | Ruta raíz del proyecto (dos niveles por encima del archivo) |
| `client` | `Groq` | Instancia global del cliente Groq lista para usar |

---

## Función: `obtener_cliente`

### Signatura

```python
def obtener_cliente() -> Groq
```

### Descripción

Fábrica del cliente Groq. Lee la variable de entorno `GROQ_API_KEY` y valida su presencia antes de construir la instancia. Al fallar, lanza un error descriptivo en lugar de silenciar el problema.

### Parámetros

Ninguno.

### Retorno

| Tipo | Descripción |
|------|-------------|
| `Groq` | Instancia del cliente configurada con la API key |

### Excepciones

| Excepción | Condición |
|-----------|-----------|
| `ValueError` | `GROQ_API_KEY` no está definida en el entorno |

### Ejemplo de uso

```python
# Nunca importar obtener_cliente directamente para instanciar:
# el módulo ya expone `client` como singleton.

from sentimiento.cliente import client

respuesta = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Hola"}]
)
```

---

## Configuración del Entorno

El archivo `.env` debe estar en la **raíz del proyecto** con el siguiente contenido:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
```

> ⚠️ **Nunca** incluir el archivo `.env` en control de versiones. Está listado en `.gitignore`.

---

## Dependencias

| Dependencia | Uso |
|-------------|-----|
| `os` | Acceso a variables de entorno |
| `pathlib.Path` | Resolución de rutas multiplataforma |
| `python-dotenv` | Carga de `.env` en el entorno |
| `groq` | SDK oficial de Groq |