🚀 main_interfaz.py — Ponto de Entrada GUI
Español · English · 🇧🇷 Português · ← Índice

Diagrama de Fluxo
python main_interfaz.py
        │
        ▼
    main()
        │
        ▼
root = TkinterDnD.Tk()          ← janela compatível com DnD
        │
        ▼
root.withdraw()                 ← ocultar durante o carregamento
        │
        ▼
root.after(0, root.deiconify)   ← mostrar após primeiro ciclo
        │
        ▼
app = AppSentimiento(root)      ← construir a UI
        │
        ▼
root.mainloop()                 ← loop de eventos