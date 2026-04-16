# 📘 SENTIMIENTO — English Documentation

🇪🇸 [Español](../es/INDEX.md) · 🌐 English · [Português](../pt/INDEX.md)

---

## Table of Contents

| Module | File | Description |
|--------|------|-------------|
| 🤖 AI Core | [sentimiento/niveles.md](sentimiento/niveles.md) | Basic, intermediate and advanced analyzers |
| 🔌 API Client | [sentimiento/cliente.md](sentimiento/cliente.md) | Groq API connection |
| 📦 Batch | [sentimiento/multitexto.md](sentimiento/multitexto.md) | Multi-text analysis |
| 💾 Save | [almacenamiento/guardar.md](almacenamiento/guardar.md) | JSON persistence |
| 📖 Read | [almacenamiento/leer.md](almacenamiento/leer.md) | JSON reading |
| 🖥️ GUI | [interface/app_sentimiento.md](interface/app_sentimiento.md) | Multimodal Tkinter app |
| ⌨️ CLI | [main.md](main.md) | Console entry point |
| 🚀 GUI Launcher | [main_interfaz.md](main_interfaz.md) | Graphical entry point |
| 🧪 Fixtures | [tests/tests.md](tests/tests.md) | Global pytest fixtures + all tests |
| ⚙️ CI/CD | [tests/tests.md#cicd](tests/tests.md) | GitHub Actions pipeline |

---

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                    DATA INPUT                       │
│         CLI (main.py) · GUI (main_interfaz.py)      │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────▼────────────┐
         │  sentimiento/niveles   │  ← AI Analysis Engine
         │  basic · intermediate ·│
         │       advanced         │
         └───────────┬────────────┘
                     │
         ┌───────────▼────────────┐
         │  sentimiento/cliente   │  ← Groq API (LLaMA 3.3 70B)
         └───────────┬────────────┘
                     │
         ┌───────────▼────────────┐
         │  almacenamiento/       │  ← JSON Persistence
         │  guardar · leer        │
         └────────────────────────┘
```