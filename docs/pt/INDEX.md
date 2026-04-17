# 📘 SENTIMIENTO — Documentação em Português

[Español](../es/INDEX.md) · [English](../en/INDEX.md) · 🇧🇷 Português

---

## Índice Geral

| Módulo | Arquivo | Descrição |
|--------|---------|-----------|
| 🤖 Core IA | [sentimiento/niveles.md](sentimiento/niveles.md) | Analisadores básico, intermediário e avançado |
| 🔌 Cliente API | [sentimiento/cliente.md](sentimiento/cliente.md) | Conexão com a API Groq |
| 📦 Lotes | [sentimiento/multitexto.md](sentimiento/multitexto.md) | Análise de múltiplos textos |
| 💾 Salvar | [almacenamiento/guardar.md](almacenamiento/guardar.md) | Persistência JSON |
| 📖 Ler | [almacenamiento/leer.md](almacenamiento/leer.md) | Leitura JSON |
| 🖥️ Interface GUI | [interface/app_sentimiento.md](interface/app_sentimiento.md) | App Tkinter multimodal |
| ⌨️ CLI | [main.md](main.md) | Ponto de entrada por console |
| 🚀 Launcher GUI | [main_interfaz.md](main_interfaz.md) | Ponto de entrada gráfico |
| 🧪 Fixtures | [tests/tests.md](tests/tests.md) | Fixtures globais pytest + todos os testes |
| ⚙️ CI/CD | [tests/tests.md#cicd](tests/tests.md) | Pipeline GitHub Actions |

---

## Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────┐
│                   ENTRADA DE DADOS                  │
│         CLI (main.py) · GUI (main_interfaz.py)      │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────▼────────────┐
         │  sentimiento/niveles   │  ← Motor de análise IA
         │  básico · intermediário│
         │       · avançado       │
         └───────────┬────────────┘
                     │
         ┌───────────▼────────────┐
         │  sentimiento/cliente   │  ← API Groq (LLaMA 3.3 70B)
         └───────────┬────────────┘
                     │
         ┌───────────▼────────────┐
         │  almacenamiento/       │  ← Persistência JSON
         │  guardar · leer        │
         └────────────────────────┘
```