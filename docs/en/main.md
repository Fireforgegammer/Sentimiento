Copiar⌨️ main.py — CLI Entry Point
Español · 🌐 English · Português · ← Index

Overview
Command-line interface (CLI) of the system. Offers two operation modes: manual analysis of user-provided text, and batch analysis of the textos_a_analizar.txt file.

General Flow Diagram
python main.py
      │
      ▼
Options menu
  1. Analyze a text manually
  2. Analyze 'textos_a_analizar.txt' file
      │
      ├── option "1" ──► analizar_texto_manual()
      ├── option "2" ──► analizar_archivo_lote()
      └── other ──► "Invalid option."

Function: analizar_texto_manual
Signature
pythondef analizar_texto_manual() -> None
Description
Prompts the user for a text via stdin, runs advanced analysis, prints the result formatted as JSON to the console, and saves it to resultados/analisis_manual.json.
Flow Diagram
input("Write the text to analyze: ")
      │
      ├── empty text? → return
      │
      ▼
analizar_sentimiento_avanzado(text)
      │
      ▼
print(json.dumps(result, indent=2, ensure_ascii=False))
      │
      ▼
guardar_json(result, "analisis_manual.json")

Function: analizar_archivo_lote
Signature
pythondef analizar_archivo_lote() -> None
Description
Reads textos_a_analizar.txt from the project root (one line = one text), analyzes it in batch with analizar_sentimiento_multitexto, saves the result to resultados/resultado_lote.json, and prints a summary to the console.
Flow Diagram
base_dir = os.path.dirname(os.path.abspath(__file__))
path = base_dir / "textos_a_analizar.txt"
      │
      ├── Does not exist? → print(error) + return
      │
      ▼
lines = [non-empty lines from file]
      │
      ├── Empty? → print("File is empty.") + return
      │
      ▼
analizar_sentimiento_multitexto(lines)
      │
      ▼
guardar_json(result, "resultado_lote.json")
      │
      ▼
print(f"Positive: X, Negative: Y")
textos_a_analizar.txt Format
I love this product, it's fantastic.
The service was terrible and took too long.
It's not bad, meets the basics.

One text per line. Empty lines are automatically ignored.


Function: main
Signature
pythondef main() -> None
Displays the menu, reads the user's option, and 