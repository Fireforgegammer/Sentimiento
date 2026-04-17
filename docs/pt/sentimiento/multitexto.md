# 📦 `sentimiento/multitexto.py`

[Español](../../es/sentimiento/multitexto.md) · [English](../../en/sentimiento/multitexto.md) · 🇧🇷 Português · [← Índice](../INDEX.md)

---

## Visão Geral

Módulo de análise em lote. Recebe uma lista de textos, analisa cada um individualmente usando o nível intermediário e retorna tanto os resultados individuais quanto um resumo estatístico agregado.

---

## Diagrama de Fluxo

```
textos: list[str]
      │
      ▼
resultados = []
      │
      ▼
┌──────────────────────────────────┐
│  for texto in textos:            │
│    resultado =                   │
│      analizar_sentimiento_       │
│      intermedio(texto)           │
│    resultados.append(resultado)  │
└─────────────┬────────────────────┘
              │
              ▼
polaridades = [r["polaridad"] for r in resultados
               if isinstance(r["polaridad"], (int, float))]
              │
              ▼
estatísticas = {
  "total", "positivos", "negativos",
  "neutrales", "polaridad_promedio"
              │
              ▼
return {
  "resultados_individuales": resultados,
  "estadisticas": estatísticas
}
```

---

## Função: `analizar_sentimiento_multitexto`

### Assinatura

```python
def analizar_sentimiento_multitexto(textos: list) -> dict
```

### Parâmetros

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `textos` | `list[str]` | Lista de textos a analisar |

### Retorno

```python
{
    "resultados_individuales": [ ...um dict por texto de entrada... ],
    "estadisticas": {
        "total": int,
        "positivos": int,
        "negativos": int,
        "neutrales": int,
        "polaridad_promedio": float
    }
}
```

### Tratamento de Erros

Se `analizar_sentimiento_intermedio` retornar um dict com `"error"` (falha de parsing), esse resultado é incluído em `resultados_individuales` mas **não contribui** para `polaridad_promedio` (o filtro `isinstance` o exclui).

---

## Dependências

| Dependência | Uso |
|-------------|-----|
| `.niveles` | `analizar_sentimiento_intermedio` para análise individual |

> ⚠️ As chamadas à API são **sequenciais**. Para lotes grandes (>50 textos), considere `asyncio` ou `ThreadPoolExecutor`.