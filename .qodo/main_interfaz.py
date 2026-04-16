import os
import sys
from tkinterdnd2 import TkinterDnD
from interface.app_sentimiento import AppSentimiento

def main():
    root = TkinterDnD.Tk()
    
    root.withdraw()
    root.after(0, root.deiconify)
    
    app = AppSentimiento(root)
    root.mainloop()

if __name__ == "__main__":
    main()