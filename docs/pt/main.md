⌨️ main.py — Ponto de Entrada CLI
Español · English · 🇧🇷 Português · ← Índice

Visão Geral
Interface de linha de comando (CLI) do sistema. Oferece dois modos de operação: análise manual de um texto fornecido pelo usuário, e análise em lote do arquivo textos_a_analizar.txt.

Diagrama de Fluxo Geral
python main.py
      │
      ▼
Menu de opções
  1. Analisar um texto manualmente
  2. Analisar arquivo 'textos_a_analizar.txt'
      │
      ├── opção "1" ──► analizar_texto_manual()
      ├── opção "2" ──► analizar_archivo_lote()
      └── outro ──► "Opção inválida."

Função: analizar_texto_manual
Assinatura
pythondef analizar_texto_manual() -> None
Diagrama de Fluxo
input("Escreva o texto a analisar: ")
      │
      ├── texto vazio? → return
      │
      ▼
analizar_sentimiento_avanzado(texto)
      │
      ▼
print(json.dumps(resultado, indent=2, ensure_ascii=False))
      │
      ▼
guardar_json(resultado, "analisis_manual.json")

Função: analizar_archivo_lote
Assinatura
pythondef analizar_archivo_lote() -> None
Formato do textos_a_analizar.txt
Adoro este produto, é fantástico.
O serviço foi terrível e demorou muito.
Não está mau, cumpre o básico.

Uma linha por texto. Linhas vazias são ignoradas automaticamente.