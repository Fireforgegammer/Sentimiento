# 💾 `almacenamiento/guardar.py`

[Español](../../es/almacenamiento/guardar.md) · [English](../../en/almacenamiento/guardar.md) · 🇧🇷 Português · [← Índice](../INDEX.md)

---

## Visão Geral

Módulo de escrita de resultados. Persiste qualquer dicionário Python como arquivo JSON formatado dentro do diretório `resultados/`, criando-o se não existir.

---

## Diagrama de Fluxo

```
dados: dict, nome_arquivo: str
          │
          ▼
caminho = os.path.join("resultados", nome_arquivo)
          │
          ▼
os.makedirs("resultados", exist_ok=True)
          │
          ▼
open(caminho, "w", encoding="utf-8")
          │
          ▼
json.dump(dados, f, indent=4, ensure_ascii=False)
          │
          ▼
return caminho  ✅
```

---

## Função: `guardar_json`

### Assinatura

```python
def guardar_json(datos: dict, nombre_archivo: str) -> str
```

### Parâmetros

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `datos` | `dict` | Dicionário a serializar |
| `nombre_archivo` | `str` | Nome do arquivo de destino com extensão (ex: `"resultado.json"`) |

### Retorno

| Tipo | Descrição |
|------|-----------|
| `str` | Caminho completo do arquivo criado (ex: `"resultados/resultado.json"`) |

### Exceções

| Exceção | Condição |
|---------|----------|
| `TypeError` | `datos` contém tipos não serializáveis |
| `OSError` | Sem permissão de escrita no diretório |

### Exemplo

```python
from almacenamiento.guardar import guardar_json

resultado = {"sentimento": "positivo", "polaridade": 0.8}
caminho = guardar_json(resultado, "minha_analise.json")
print(caminho)  # → "resultados/minha_analise.json"
```

---

# 📖 `almacenamiento/leer.py`

[Español](../../es/almacenamiento/leer.md) · [English](../../en/almacenamiento/guardar.md) · 🇧🇷 Português · [← Índice](../INDEX.md)

---

## Visão Geral

Módulo de leitura de resultados persistidos. Carrega um arquivo JSON do diretório `resultados/` e o retorna como dicionário Python, com validação de existência prévia.

---

## Diagrama de Fluxo

```
nome_arquivo: str
      │
      ▼
caminho = os.path.join("resultados", nome_arquivo)
      │
      ▼
os.path.exists(caminho)?
      │
      ├── Não → raise FileNotFoundError ❌
      │
     Sim
      │
      ▼
open(caminho, "r", encoding="utf-8")
      │
      ▼
return json.load(f)  ✅
```

---

## Função: `leer_json`

### Assinatura

```python
def leer_json(nombre_archivo: str) -> dict
```

### Parâmetros

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `nombre_archivo` | `str` | Nome do arquivo a ler (ex: `"resultado.json"`) |

### Retorno

| Tipo | Descrição |
|------|-----------|
| `dict` | Conteúdo do arquivo JSON desserializado |

### Exceções

| Exceção | Condição |
|---------|----------|
| `FileNotFoundError` | O arquivo não existe em `resultados/` |
| `json.JSONDecodeError` | O arquivo existe mas contém JSON malformado |

---

## Relação com `guardar.py`

```
guardar_json(dados, "resultado.json")
        │
        ▼  (escreve)
  resultados/resultado.json
        │
        ▼  (lê)
leer_json("resultado.json") → dados
```