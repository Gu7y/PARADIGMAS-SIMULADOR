import customtkinter as ctk
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from views.gui import CircuitAnalyzerGUI

def main():
    root = ctk.CTk()
    app = CircuitAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()