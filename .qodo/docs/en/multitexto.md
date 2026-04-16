# 📦 `sentimiento/multitexto.py`

[Español](../../es/sentimiento/multitexto.md) · 🌐 English · [Português](../../pt/sentimiento/multitexto.md) · [← Index](../INDEX.md)

---

## Overview

Batch analysis module. Receives a list of texts, analyzes each individually using the intermediate level, and returns both individual results and an aggregated statistical summary.

---

## Flow Diagram

```
textos: list[str]
      │
      ▼
resultados = []
      │
      ▼
┌──────────────────────────────────┐
│  for text in textos:             │
│    result =                      │
│      analizar_sentimiento_       │
│      intermedio(text)            │
│    resultados.append(result)     │
└─────────────┬────────────────────┘
              │
              ▼
polarities = [r["polaridad"] for r in resultados
              if isinstance(r["polaridad"], (int, float))]
              │
              ▼
estadisticas = {
  "total": len(resultados),
  "positivos": count(sentimiento == "positivo"),
  "negativos": count(sentimiento == "negativo"),
  "neutrales": count(sentimiento == "neutral"),
  "polaridad_promedio": sum / len  (if any valid polarity)
              │
              ▼
return {
  "resultados_individuales": resultados,
  "estadisticas": estadisticas
}
```

---

## Function: `analizar_sentimiento_multitexto`

### Signature

```python
def analizar_sentimiento_multitexto(textos: list) -> dict
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `textos` | `list[str]` | List of texts to analyze |

### Return

```python
{
    "resultados_individuales": [ ...one dict per input text... ],
    "estadisticas": {
        "total": int,
        "positivos": int,
        "negativos": int,
        "neutrales": int,
        "polaridad_promedio": float
    }
}
```

### Error handling

If `analizar_sentimiento_intermedio` returns an error dict (parse failure), it is included in `resultados_individuales` but **does not contribute** to `polaridad_promedio` (the `isinstance` filter excludes it).

---

## Dependencies

| Dependency | Usage |
|------------|-------|
| `.niveles` | `analizar_sentimiento_intermedio` for individual analysis |

> ⚠️ API calls are **sequential**. For large batches (>50 texts), consider `asyncio` or `ThreadPoolExecutor`.