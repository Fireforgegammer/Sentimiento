# 🤖 `sentimiento/niveles.py`

[Español](../../es/sentimiento/niveles.md) · 🌐 English · [Português](../../pt/sentimiento/niveles.md) · [← Index](../INDEX.md)

---

## Overview

Central sentiment analysis engine. Exposes **three levels of analytical depth** that invoke the LLaMA 3.3 70B model via the Groq API. Each level returns a structured dictionary with progressively richer information.

---

## General Flow Diagram

```
                        text: str
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
        [BASIC]      [INTERMEDIATE]     [ADVANCED]
      1 sentiment       JSON with        JSON with
         field        4 fields + level  6 fields + level
            │               │               │
            └───────────────┼───────────────┘
                            │
                    clean_json_response()
                            │
                     json.loads() / fallback
                            │
                        dict result
```

---

## Function: `limpiar_respuesta_json`

### Signature

```python
def limpiar_respuesta_json(texto_raw: str) -> str
```

### Description

Sanitizes the raw model response by removing markdown code blocks (` ```json ... ``` `) that the LLM may unintentionally wrap around the JSON output.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `texto_raw` | `str` | Raw response as received from the model |

### Return

| Type | Description |
|------|-------------|
| `str` | Clean JSON string without backticks or block prefixes |

### Flow Diagram

```
texto_raw
    │
    ▼
Does it start with ```?
    │
   Yes ──► Split into lines
    │         │
    │         ▼
    │    Does first line start with ```? → Remove it
    │         ▼
    │    Does last line start with ```? → Remove it
    │         ▼
    │    Rejoin remaining lines
    │
   No ──► strip()
    │
    ▼
Clean str
```

---

## Function: `analizar_sentimiento_basico`

### Signature

```python
def analizar_sentimiento_basico(texto: str) -> dict
```

### Description

Performs a **shallow** sentiment analysis. The model responds with a single word: `positivo`, `negativo`, or `neutral`. Ideal for quick classifications or high-volume pipelines.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `texto` | `str` | Text to analyze (arbitrary length) |

### Return

```python
{
    "nivel": "básico",
    "sentimiento": "positivo" | "negativo" | "neutral",
    "texto_original": str  # first 100 characters
}
```

### Model configuration

| Parameter | Value |
|-----------|-------|
| Model | `llama-3.3-70b-versatile` |
| Temperature | `0.0` (deterministic) |
| System prompt | Return one word only |

---

## Function: `analizar_sentimiento_intermedio`

### Signature

```python
def analizar_sentimiento_intermedio(texto: str) -> dict
```

### Description

**Mid-depth** analysis. The model returns a structured JSON with sentiment, numeric polarity, detected emotions list, and intensity. Includes parse error handling with a fallback.

### Return (success)

```python
{
    "nivel": "intermedio",
    "sentimiento": str,
    "polaridad": float,      # typical range [-1.0, 1.0]
    "emociones": list[str],
    "intensidad": float,     # typical range [0.0, 1.0]
    "texto_original": str
}
```

### Return (parse error)

```python
{
    "nivel": "intermedio",
    "error": "Error de parseo",
    "respuesta_raw": str
}
```

---

## Function: `analizar_sentimiento_avanzado`

### Signature

```python
def analizar_sentimiento_avanzado(texto: str) -> dict
```

### Description

**Full deep** analysis. Extracts global sentiment, polarity, key text fragments, reasoned justification, communicative tone, and improvement recommendation. This is the level used by the GUI and E2E tests.

### Return (success)

```python
{
    "nivel": "avanzado",
    "sentimiento_global": str,
    "polaridad": float,
    "fragmentos": list[str],     # key text fragments
    "justificacion": str,        # model reasoning
    "tonalidad": str,            # communicative tone
    "recomendacion": str,        # improvement suggestion
    "texto_original": str
}
```

### Flow Diagram

```
texto: str
    │
    ▼
client.chat.completions.create()
    │  system: "Respond ONLY with JSON:
    │           sentimiento_global, polaridad,
    │           fragmentos, justificacion,
    │           tonalidad, recomendacion"
    │  user: text
    │  temp: 0.0
    │
    ▼
contenido_raw
    │
    ▼
limpiar_respuesta_json()
    │
    ├── try: json.loads() → inject level + original_text → return ✅
    └── except: return fallback with raw ⚠️
```

---

## Level Comparison

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| Fields returned | 3 | ~6 | ~8 |
| Numeric polarity | ❌ | ✅ | ✅ |
| Emotions list | ❌ | ✅ | ❌ (replaced by fragments) |
| Justification | ❌ | ❌ | ✅ |
| Recommendation | ❌ | ❌ | ✅ |
| Key fragments | ❌ | ❌ | ✅ |
| Token cost | Low | Medium | High |
| Used in GUI | Yes | Yes | Yes (main tab) |

---

## Dependencies

| Dependency | Usage |
|------------|-------|
| `json` | Parse model responses |
| `.cliente` | Groq client instance |