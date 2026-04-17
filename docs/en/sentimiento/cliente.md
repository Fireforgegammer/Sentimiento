# 🔌 `sentimiento/cliente.py`

[Español](../../es/sentimiento/cliente.md) · 🌐 English · [Português](../../pt/sentimiento/cliente.md) · [← Index](../INDEX.md)

---

## Overview

Groq API client initialization module. Reads the API key from environment variables (loaded from `.env`) and returns a configured `Groq` instance, ready to be imported by other modules.

---

## Flow Diagram

```
Module load
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
      ├── api_key is None? → raise ValueError("GROQ_API_KEY not found") ❌
      │
      ▼
return Groq(api_key=api_key) ✅
```

---

## Module Variables

| Variable | Type | Description |
|----------|------|-------------|
| `BASE_DIR` | `Path` | Project root path (two levels above this file) |
| `client` | `Groq` | Global Groq client instance, ready to use |

---

## Function: `obtener_cliente`

### Signature

```python
def obtener_cliente() -> Groq
```

### Description

Groq client factory. Reads the `GROQ_API_KEY` environment variable, validates its presence, and constructs the instance. Raises a descriptive error on failure rather than silencing the problem.

### Return

| Type | Description |
|------|-------------|
| `Groq` | Client instance configured with the API key |

### Exceptions

| Exception | Condition |
|-----------|-----------|
| `ValueError` | `GROQ_API_KEY` is not defined in the environment |

---

## Environment Setup

The `.env` file must be at the **project root**:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
```

> ⚠️ **Never** include `.env` in version control. It is listed in `.gitignore`.

---

## Dependencies

| Dependency | Usage |
|------------|-------|
| `os` | Environment variable access |
| `pathlib.Path` | Cross-platform path resolution |
| `python-dotenv` | Load `.env` into the environment |
| `groq` | Official Groq SDK |