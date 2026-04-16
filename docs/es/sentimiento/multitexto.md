# 📦 `sentimiento/multitexto.py`

🌐 [English](../../en/sentimiento/multitexto.md) · [Português](../../pt/sentimiento/multitexto.md) · [← Índice](../INDEX.md)

---

## Descripción General

Módulo de análisis por lotes. Recibe una lista de textos, los analiza individualmente usando el nivel intermedio, y devuelve tanto los resultados individuales como un resumen estadístico agregado.

---

## Diagrama de Flujo

```
textos: list[str]
      │
      ▼
resultados = []
      │
      ▼
┌─────────────────────────────┐
│  for texto in textos:       │
│    resultado =              │
│      analizar_sentimiento_  │
│      intermedio(texto)      │
│    resultados.append(...)   │
└─────────────┬───────────────┘
              │
              ▼
polaridades = [r["polaridad"] for r in resultados
               if isinstance(r["polaridad"], (int, float))]
              │
              ▼
estadisticas = {
  "total": len(resultados),
  "positivos": count(sentimiento == "positivo"),
  "negativos": count(sentimiento == "negativo"),
  "neutrales": count(sentimiento == "neutral"),
  "polaridad_promedio": sum(polaridades)/len(polaridades)
              │          si hay polaridades válidas
              ▼
return {
  "resultados_individuales": resultados,
  "estadisticas": estadisticas
}
```

---

## Función: `analizar_sentimiento_multitexto`

### Signatura

```python
def analizar_sentimiento_multitexto(textos: list) -> dict
```

### Descripción

Itera sobre una lista de textos, ejecuta `analizar_sentimiento_intermedio` en cada uno, y construye un informe consolidado con estadísticas de distribución de sentimiento y polaridad promedio.

### Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `textos` | `list[str]` | Lista de textos a analizar. Pueden ser de cualquier longitud. |

### Retorno

```python
{
    "resultados_individuales": [
        {
            "nivel": "intermedio",
            "sentimiento": str,
            "polaridad": float,
            "emociones": list[str],
            "intensidad": float,
            "texto_original": str
        },
        # ... uno por cada texto de entrada
    ],
    "estadisticas": {
        "total": int,
        "positivos": int,
        "negativos": int,
        "neutrales": int,
        "polaridad_promedio": float  # 0 si no hay polaridades numéricas
    }
}
```

### Comportamiento ante errores

Si `analizar_sentimiento_intermedio` devuelve un dict con `"error"` (fallo de parseo), ese resultado se incluye en `resultados_individuales` pero **no contribuye** a `polaridad_promedio` (el filtro `isinstance` lo excluye).

### Ejemplo

```python
textos = [
    "Me encanta este producto",
    "Es horrible, no lo recomiendo",
    "No está mal, pero podría mejorar"
]

resultado = analizar_sentimiento_multitexto(textos)

# resultado["estadisticas"] →
# {
#   "total": 3,
#   "positivos": 1,
#   "negativos": 1,
#   "neutrales": 1,
#   "polaridad_promedio": 0.05
# }
```

---

## Dependencias

| Dependencia | Uso |
|-------------|-----|
| `.niveles` | `analizar_sentimiento_intermedio` para análisis individual |

---

## Notas de Rendimiento

> ⚠️ Las llamadas a la API son **secuenciales**. Para lotes grandes (>50 textos), el tiempo de respuesta puede ser elevado. Considerar implementar concurrencia con `asyncio` o `ThreadPoolExecutor` si el volumen lo requiere.