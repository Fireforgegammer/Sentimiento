import tkinter as tk
from interface.app_sentimiento import AppSentimiento

def main():
    root = tk.Tk()
    app = AppSentimiento(root)
    root.mainloop()

if __name__ == "__main__":
    main()