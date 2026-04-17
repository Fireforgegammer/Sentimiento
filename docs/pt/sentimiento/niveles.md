# 🤖 `sentimiento/niveles.py`

[Español](../../es/sentimiento/niveles.md) · [English](../../en/sentimiento/niveles.md) · 🇧🇷 Português · [← Índice](../INDEX.md)

---

## Visão Geral

Motor central de análise de sentimento. Expõe **três níveis de profundidade analítica** que invocam o modelo LLaMA 3.3 70B via API Groq. Cada nível retorna um dicionário estruturado com informações progressivamente mais ricas.

---

## Diagrama de Fluxo Geral

```
                        texto: str
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
        [BÁSICO]     [INTERMEDIÁRIO]    [AVANÇADO]
      1 campo de        JSON com         JSON com
      sentimento      4 campos + nível  6 campos + nível
            │               │               │
            └───────────────┼───────────────┘
                            │
                    limpar_resposta_json()
                            │
                     json.loads() / fallback
                            │
                        dict resultado
```

---

## Função: `limpiar_respuesta_json`

### Assinatura

```python
def limpiar_respuesta_json(texto_raw: str) -> str
```

### Descrição

Sanitiza a resposta bruta do modelo removendo blocos de código markdown (` ```json ... ``` `) que o LLM pode inserir involuntariamente em torno do JSON.

### Parâmetros

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `texto_raw` | `str` | Resposta bruta recebida do modelo |

### Retorno

| Tipo | Descrição |
|------|-----------|
| `str` | String JSON limpa, sem backticks ou prefixos de bloco |

### Diagrama de Fluxo

```
texto_raw
    │
    ▼
Começa com ```?
    │
   Sim ──► Dividir em linhas
    │         ├── Primeira linha começa com ``` → Remover
    │         └── Última linha começa com ``` → Remover
    │         └── Reunir linhas restantes
    │
   Não ──► strip()
    │
    ▼
str limpa
```

---

## Função: `analizar_sentimiento_basico`

### Assinatura

```python
def analizar_sentimiento_basico(texto: str) -> dict
```

### Descrição

Realiza uma análise **superficial** do sentimento. O modelo responde com uma única palavra: `positivo`, `negativo` ou `neutral`. Ideal para classificações rápidas ou pipelines de alto volume.

### Parâmetros

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `texto` | `str` | Texto a analisar (comprimento arbitrário) |

### Retorno

```python
{
    "nivel": "básico",
    "sentimiento": "positivo" | "negativo" | "neutral",
    "texto_original": str  # primeiros 100 caracteres
}
```

### Configuração do modelo

| Parâmetro | Valor |
|-----------|-------|
| Modelo | `llama-3.3-70b-versatile` |
| Temperatura | `0.0` (determinístico) |
| System prompt | Retorna apenas uma palavra |

---

## Função: `analizar_sentimiento_intermedio`

### Assinatura

```python
def analizar_sentimiento_intermedio(texto: str) -> dict
```

### Descrição

Análise de **profundidade média**. O modelo retorna um JSON estruturado com sentimento, polaridade numérica, lista de emoções detectadas e intensidade. Inclui tratamento de erros de parsing com fallback.

### Retorno (sucesso)

```python
{
    "nivel": "intermedio",
    "sentimiento": str,
    "polaridad": float,      # intervalo típico [-1.0, 1.0]
    "emociones": list[str],
    "intensidad": float,     # intervalo típico [0.0, 1.0]
    "texto_original": str
}
```

### Retorno (erro de parsing)

```python
{
    "nivel": "intermedio",
    "error": "Error de parseo",
    "respuesta_raw": str
}
```

---

## Função: `analizar_sentimiento_avanzado`

### Assinatura

```python
def analizar_sentimiento_avanzado(texto: str) -> dict
```

### Descrição

Análise **completa e profunda**. Extrai sentimento global, polaridade, fragmentos relevantes do texto, justificativa fundamentada, tonalidade comunicativa e recomendação de melhoria. É o nível usado pela interface gráfica e pelos testes E2E.

### Retorno (sucesso)

```python
{
    "nivel": "avanzado",
    "sentimiento_global": str,
    "polaridad": float,
    "fragmentos": list[str],     # fragmentos-chave do texto
    "justificacion": str,        # raciocínio do modelo
    "tonalidad": str,            # tom comunicativo
    "recomendacion": str,        # sugestão de melhoria
    "texto_original": str
}
```

### Diagrama de Fluxo

```
texto: str
    │
    ▼
client.chat.completions.create()
    │  system: "Responda SOMENTE com JSON:
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
    ├── try: json.loads() → injetar nível + texto_original → return ✅
    └── except: return fallback com raw ⚠️
```

---

## Comparativo de Níveis

| Característica | Básico | Intermediário | Avançado |
|----------------|--------|---------------|----------|
| Campos retornados | 3 | ~6 | ~8 |
| Polaridade numérica | ❌ | ✅ | ✅ |
| Lista de emoções | ❌ | ✅ | ❌ (substituído por fragmentos) |
| Justificativa | ❌ | ❌ | ✅ |
| Recomendação | ❌ | ❌ | ✅ |
| Fragmentos-chave | ❌ | ❌ | ✅ |
| Custo de tokens | Baixo | Médio | Alto |
| Usado na GUI | Sim | Sim | Sim (aba principal) |

---

## Dependências

| Dependência | Uso |
|-------------|-----|
| `json` | Parsing das respostas do modelo |
| `.cliente` | Instância do cliente Groq |