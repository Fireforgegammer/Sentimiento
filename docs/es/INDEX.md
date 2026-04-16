# 📘 SENTIMIENTO — Documentación en Español

🌐 [English](../en/INDEX.md) · [Português](../pt/INDEX.md) · 🇪🇸 Español

---

## Índice General

| Módulo | Archivo | Descripción |
|--------|---------|-------------|
| 🤖 Core IA | [sentimiento/niveles.md](sentimiento/niveles.md) | Analizadores básico, intermedio y avanzado |
| 🔌 Cliente API | [sentimiento/cliente.md](sentimiento/cliente.md) | Conexión con Groq API |
| 📦 Lotes | [sentimiento/multitexto.md](sentimiento/multitexto.md) | Análisis de múltiples textos |
| 💾 Guardar | [almacenamiento/guardar.md](almacenamiento/guardar.md) | Persistencia JSON |
| 📖 Leer | [almacenamiento/leer.md](almacenamiento/leer.md) | Lectura JSON |
| 🖥️ Interfaz GUI | [interface/app_sentimiento.md](interface/app_sentimiento.md) | Aplicación Tkinter multimodal |
| ⌨️ CLI | [main.md](main.md) | Punto de entrada por consola |
| 🚀 Lanzador GUI | [main_interfaz.md](main_interfaz.md) | Punto de entrada gráfico |
| 🧪 Fixtures | [tests/conftest.md](tests/conftest.md) | Fixtures globales de pytest |
| 🔬 Tests E2E | [tests/e2e.md](tests/e2e.md) | Pruebas end-to-end de flujo |
| 🔗 Tests Integración | [tests/integration.md](tests/integration.md) | Pruebas de integración |
| 🧩 Tests Unitarios | [tests/unit.md](tests/unit.md) | Pruebas unitarias |
| ⚙️ CI/CD | [cicd.md](cicd.md) | Pipeline GitHub Actions |

---

## Arquitectura General

```
┌─────────────────────────────────────────────────────┐
│                   ENTRADA DE DATOS                  │
│         CLI (main.py) · GUI (main_interfaz.py)      │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────▼────────────┐
         │   sentimiento/niveles  │  ← Motor de análisis IA
         │  básico · intermedio · │
         │       avanzado         │
         └───────────┬────────────┘
                     │
         ┌───────────▼────────────┐
         │   sentimiento/cliente  │  ← Groq API (LLaMA 3.3 70B)
         └───────────┬────────────┘
                     │
         ┌───────────▼────────────┐
         │  almacenamiento/       │  ← Persistencia JSON
         │  guardar · leer        │
         └────────────────────────┘
```