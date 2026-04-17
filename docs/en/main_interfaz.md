🚀 main_interfaz.py — GUI Entry Point
Español · 🌐 English · Português · ← Index

Overview
Graphical interface launcher. Initializes the TkinterDnD event loop (required for Drag & Drop support), manages the initial window visibility, and starts the AppSentimiento application.

Flow Diagram
python main_interfaz.py
        │
        ▼
    main()
        │
        ▼
root = TkinterDnD.Tk()          ← DnD-compatible window
        │
        ▼
root.withdraw()                 ← hide while loading
        │
        ▼
root.after(0, root.deiconify)   ← show after first cycle
        │
        ▼
app = AppSentimiento(root)      ← build UI
        │
        ▼
root.mainloop()                 ← event loop
Why withdraw + deiconify
Some operating systems render the window at its default size before Tkinter applies the geometry configured in AppSentimiento, causing a visual flash. This technique eliminates that artifact.

Dependencies
DependencyUsagetkinterdnd2.TkinterDnDRoot window with Drag & Drop supportinterface.app_sentimiento.AppSentimiento