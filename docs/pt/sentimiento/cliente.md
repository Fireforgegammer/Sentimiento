# 🔌 `sentimiento/cliente.py`

[Español](../../es/sentimiento/cliente.md) · [English](../../en/sentimiento/cliente.md) · 🇧🇷 Português · [← Índice](../INDEX.md)

---

## Visão Geral

Módulo de inicialização do cliente da API Groq. Responsável por ler a chave de API das variáveis de ambiente (carregadas do `.env`) e retornar uma instância configurada de `Groq`, pronta para ser importada por outros módulos.

---

## Diagrama de Fluxo

```
Carregamento do módulo
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
      ├── api_key é None? → raise ValueError("GROQ_API_KEY não encontrada") ❌
      │
      ▼
return Groq(api_key=api_key) ✅
```

---

## Variáveis do Módulo

| Variável | Tipo | Descrição |
|----------|------|-----------|
| `BASE_DIR` | `Path` | Caminho raiz do projeto (dois níveis acima deste arquivo) |
| `client` | `Groq` | Instância global do cliente Groq pronta para usar |

---

## Função: `obtener_cliente`

### Assinatura

```python
def obtener_cliente() -> Groq
```

### Descrição

Fábrica do cliente Groq. Lê a variável de ambiente `GROQ_API_KEY`, valida sua presença e constrói a instância. Em caso de falha, lança um erro descritivo em vez de silenciar o problema.

### Retorno

| Tipo | Descrição |
|------|-----------|
| `Groq` | Instância do cliente configurada com a API key |

### Exceções

| Exceção | Condição |
|---------|----------|
| `ValueError` | `GROQ_API_KEY` não está definida no ambiente |

---

## Configuração do Ambiente

O arquivo `.env` deve estar na **raiz do projeto**:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
```

> ⚠️ **Nunca** incluir o arquivo `.env` no controle de versão. Está listado no `.gitignore`.

---

## Dependências

| Dependência | Uso |
|-------------|-----|
| `os` | Acesso às variáveis de ambiente |
| `pathlib.Path` | Resolução de caminhos multiplataforma |
| `python-dotenv` | Carregamento do `.env` no ambiente |
| `groq` | SDK oficial da Groq |