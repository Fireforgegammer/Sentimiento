# 🤖 `sentimiento/niveles.py`

🌐 [English](../../en/sentimiento/niveles.md) · [Português](../../pt/sentimiento/niveles.md) · [← Índice](../INDEX.md)

---

## Descripción General

Motor central de análisis de sentimiento. Expone **tres niveles de profundidad analítica** que invocan el modelo LLaMA 3.3 70B mediante la API de Groq. Cada nivel devuelve un diccionario estructurado con información progresivamente más rica.

---

## Diagrama de Flujo General

```
                        texto: str
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
     [BÁSICO]        [INTERMEDIO]      [AVANZADO]
   1 campo de          JSON con         JSON con
   sentimiento      4 campos + nivel   6 campos + nivel
            │               │               │
            └───────────────┼───────────────┘
                            │
                    limpiar_respuesta_json()
                            │
                     json.loads() / fallback
                            │
                        dict resultado
```

---

## Función: `limpiar_respuesta_json`

### Signatura

```python
def limpiar_respuesta_json(texto_raw: str) -> str
```

### Descripción

Sanitiza la respuesta cruda del modelo eliminando bloques de código markdown (` ```json ... ``` `) que el LLM puede insertar involuntariamente alrededor del JSON.

### Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `texto_raw` | `str` | Respuesta cruda tal como llega del modelo |

### Retorno

| Tipo | Descripción |
|------|-------------|
| `str` | Cadena JSON limpia, sin backticks ni prefijos de bloque |

### Diagrama de Flujo

```
texto_raw
    │
    ▼
¿Empieza con ```?
    │
   Sí ──► Partir por líneas
    │         │
    │         ▼
    │    ¿Primera línea empieza con ```?
    │         │ Sí ──► Eliminar primera línea
    │         ▼
    │    ¿Última línea empieza con ```?
    │         │ Sí ──► Eliminar última línea
    │         ▼
    │    Unir líneas restantes
    │
   No ──► strip()
    │
    ▼
str limpio
```

### Ejemplo

```python
entrada = '```json\n{"sentimiento": "positivo"}\n```'
salida = limpiar_respuesta_json(entrada)
# → '{"sentimiento": "positivo"}'
```

---

## Función: `analizar_sentimiento_basico`

### Signatura

```python
def analizar_sentimiento_basico(texto: str) -> dict
```

### Descripción

Realiza un análisis **superficial** del sentimiento. El modelo responde con una única palabra: `positivo`, `negativo` o `neutral`. Ideal para clasificaciones rápidas o pipelines de alto volumen.

### Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `texto` | `str` | Texto a analizar (longitud arbitraria) |

### Retorno

```python
{
    "nivel": "básico",
    "sentimiento": "positivo" | "negativo" | "neutral",
    "texto_original": str  # primeros 100 caracteres
}
```

### Configuración del modelo

| Parámetro | Valor |
|-----------|-------|
| Modelo | `llama-3.3-70b-versatile` |
| Temperature | `0.0` (determinista) |
| System prompt | Solo devuelve una palabra |

### Diagrama de Flujo

```
texto: str
    │
    ▼
client.chat.completions.create()
    │  model: llama-3.3-70b-versatile
    │  temp: 0.0
    │  system: "Responde SOLO: positivo/negativo/neutral"
    │
    ▼
response.choices[0].message.content.strip()
    │
    ▼
{
  "nivel": "básico",
  "sentimiento": <respuesta>,
  "texto_original": texto[:100]
}
```

### Ejemplo

```python
res = analizar_sentimiento_basico("Me encanta este producto")
# → {"nivel": "básico", "sentimiento": "positivo", "texto_original": "Me encanta este producto"}
```

---

## Función: `analizar_sentimiento_intermedio`

### Signatura

```python
def analizar_sentimiento_intermedio(texto: str) -> dict
```

### Descripción

Análisis de **profundidad media**. El modelo devuelve un JSON estructurado con sentimiento, polaridad numérica, lista de emociones detectadas e intensidad. Incluye manejo de errores de parseo con fallback.

### Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `texto` | `str` | Texto a analizar |

### Retorno (éxito)

```python
{
    "nivel": "intermedio",
    "sentimiento": str,
    "polaridad": float,      # rango típico [-1.0, 1.0]
    "emociones": list[str],
    "intensidad": float,     # rango típico [0.0, 1.0]
    "texto_original": str
}
```

### Retorno (error de parseo)

```python
{
    "nivel": "intermedio",
    "error": "Error de parseo",
    "respuesta_raw": str
}
```

### Diagrama de Flujo

```
texto: str
    │
    ▼
client.chat.completions.create()
    │  system: "Responde ÚNICAMENTE JSON: sentimiento,
    │           polaridad, emociones, intensidad"
    │
    ▼
contenido_raw = response.choices[0].message.content
    │
    ▼
limpiar_respuesta_json(contenido_raw)
    │
    ├── try: json.loads()
    │       │
    │       ▼
    │   resultado["nivel"] = "intermedio"
    │   resultado["texto_original"] = texto[:100]
    │       │
    │       ▼
    │   return resultado ✅
    │
    └── except: return {"error": "Error de parseo", ...} ⚠️
```

---

## Función: `analizar_sentimiento_avanzado`

### Signatura

```python
def analizar_sentimiento_avanzado(texto: str) -> dict
```

### Descripción

Análisis **completo y profundo**. Extrae sentimiento global, polaridad, fragmentos relevantes del texto, justificación razonada, tonalidad comunicativa y recomendación de mejora. Es el nivel usado por la interfaz gráfica y los tests E2E.

### Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `texto` | `str` | Texto a analizar |

### Retorno (éxito)

```python
{
    "nivel": "avanzado",
    "sentimiento_global": str,
    "polaridad": float,
    "fragmentos": list[str],     # fragmentos clave del texto
    "justificacion": str,        # razonamiento del modelo
    "tonalidad": str,            # tono comunicativo
    "recomendacion": str,        # sugerencia de mejora
    "texto_original": str
}
```

### Retorno (error de parseo)

```python
{
    "nivel": "avanzado",
    "error": "Error de parseo",
    "respuesta_raw": str
}
```

### Diagrama de Flujo

```
texto: str
    │
    ▼
client.chat.completions.create()
    │  system: "Responde ÚNICAMENTE JSON:
    │           sentimiento_global, polaridad,
    │           fragmentos, justificacion,
    │           tonalidad, recomendacion"
    │  user: texto
    │  temp: 0.0
    │
    ▼
contenido_raw
    │
    ▼
limpiar_respuesta_json()
    │
    ├── try: json.loads()
    │       │
    │       ▼
    │   Inyectar nivel + texto_original
    │       │
    │       ▼
    │   return dict completo ✅
    │
    └── except: return fallback con raw ⚠️
```

### Ejemplo

```python
res = analizar_sentimiento_avanzado("El servicio es terrible y nunca responden")
# → {
#     "nivel": "avanzado",
#     "sentimiento_global": "negativo",
#     "polaridad": -0.85,
#     "fragmentos": ["servicio es terrible", "nunca responden"],
#     "justificacion": "Lenguaje marcadamente negativo con crítica directa...",
#     "tonalidad": "crítico-agresivo",
#     "recomendacion": "Evitar generalizaciones y proponer soluciones concretas",
#     "texto_original": "El servicio es terrible..."
# }
```

---

## Comparativa de Niveles

| Característica | Básico | Intermedio | Avanzado |
|----------------|--------|------------|----------|
| Campos devueltos | 3 | ~6 | ~8 |
| Polaridad numérica | ❌ | ✅ | ✅ |
| Lista de emociones | ❌ | ✅ | ❌ (reemplazado por fragmentos) |
| Justificación | ❌ | ❌ | ✅ |
| Recomendación | ❌ | ❌ | ✅ |
| Fragmentos clave | ❌ | ❌ | ✅ |
| Coste de tokens | Bajo | Medio | Alto |
| Usado en GUI | Sí | Sí | Sí (pestaña principal) |

---

## Dependencias

| Dependencia | Uso |
|-------------|-----|
| `json` | Parseo de respuestas del modelo |
| `.cliente` | Instancia del cliente Groq |