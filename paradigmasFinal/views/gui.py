import customtkinter as ctk
from tkinter import messagebox



class CircuitAnalyzerGUI:
    def __init__(self, root: ctk.CTk):
        from models.circuit import Circuit
        from strategies.resolution_strategies import (
            CramerStrategy, GaussJordanStrategy, NumericStrategy
        )
        from controllers.circuit_controller import CircuitController
        from utils.translations import TRANSLATIONS
        
        self.root = root
        self.circuit = Circuit.get_instance()
        self.circuit.add_observer(self)
        
        self.language = 'es'
        self.TRANSLATIONS = TRANSLATIONS
        self.t = self.TRANSLATIONS[self.language]
        
        # Estrategias disponibles
        self.strategies = {
            'cramer': CramerStrategy(),
            'gauss': GaussJordanStrategy(),
            'numeric': NumericStrategy()
        }
        
        self.controller = CircuitController(self.strategies['cramer'])
        
        # Variables para mantener estado
        self.voltage_var = None
        self.resistor_var = None
        self.method_var = None
        self.circuit_type_var = None
        
        self.setup_ui()
        self.update_resistor_list()
    
    def update(self, subject):
        """Observer: Actualiza la vista cuando el modelo cambia"""
        self.update_resistor_list()
    
    def toggle_language(self):
        """Alterna entre español y portugués"""
        voltage_val = self.voltage_var.get() if self.voltage_var else '15.0'
        resistor_val = self.resistor_var.get() if self.resistor_var else '3.0'
        method_val = self.method_var.get() if self.method_var else 'cramer'
        circuit_type_val = self.circuit_type_var.get() if self.circuit_type_var else 'serie'
        
        self.language = 'pt' if self.language == 'es' else 'es'
        self.t = self.TRANSLATIONS[self.language]
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.setup_ui()
        
        self.voltage_var.set(voltage_val)
        self.resistor_var.set(resistor_val)
        self.method_var.set(method_val)
        self.circuit_type_var.set(circuit_type_val)
        
        self.update_resistor_list()
    
    def setup_ui(self):
        "interfaz gráfica "
        self.root.title(self.t['title'])
        self.root.geometry('1400x900')
        self.root.minsize(1200, 800)
        self.root.resizable(True, True)
        
        
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        
        header_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=self.t['title'],
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 5))
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text=self.t['subtitle'],
            font=ctk.CTkFont(size=14),
            text_color="gray70"
        )
        subtitle_label.pack(pady=(0, 15))
        
        lang_button = ctk.CTkButton(
            header_frame,
            text=self.t['language'],
            command=self.toggle_language,
            width=150,
            height=35,
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=8
        )
        lang_button.pack(pady=(0, 20))
        
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        
        left_frame = ctk.CTkFrame(content_frame, corner_radius=15)
        left_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        
        ctk.CTkLabel(
            left_frame,
            text=self.t['circuit'],
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 10))
        
        
        type_container = ctk.CTkFrame(
            left_frame,
            fg_color="#5b21b6",
            corner_radius=12
        )
        type_container.pack(pady=(10, 10), padx=20, fill="x")
        
        ctk.CTkLabel(
            type_container,
            text=" TIPO DE CIRCUITO ",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="black"
        ).pack(pady=(15, 5))
        
        self.circuit_type_var = ctk.StringVar(value='serie')
        
        circuit_type_menu = ctk.CTkOptionMenu(
            type_container,
            variable=self.circuit_type_var,
            values=['serie', 'paralelo', 'mallas'],
            command=self.change_circuit_type,
            width=200,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            dropdown_font=ctk.CTkFont(size=13),
            corner_radius=10,
            fg_color="white",
            button_color="#6d28d9",
            button_hover_color="#5b21b6",
            text_color="black"
        )
        circuit_type_menu.pack(pady=(5, 15))
        
        # Separador
        separator = ctk.CTkFrame(left_frame, height=2, fg_color="gray30")
        separator.pack(fill="x", padx=30, pady=15)
        
        # Voltaje
        ctk.CTkLabel(
            left_frame,
            text=self.t['voltage'],
            font=ctk.CTkFont(size=13)
        ).pack(pady=(10, 5))
        
        self.voltage_var = ctk.StringVar(value='15.0')
        ctk.CTkEntry(
            left_frame,
            textvariable=self.voltage_var,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14),
            justify="center"
        ).pack(pady=(0, 15))
        
        # Resistencia
        ctk.CTkLabel(
            left_frame,
            text=self.t['resistance'],
            font=ctk.CTkFont(size=13)
        ).pack(pady=(10, 5))
        
        self.resistor_var = ctk.StringVar(value='3.0')
        ctk.CTkEntry(
            left_frame,
            textvariable=self.resistor_var,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14),
            justify="center"
        ).pack(pady=(0, 10))
        
        # Botón agregar
        ctk.CTkButton(
            left_frame,
            text=self.t['add_resistor'],
            command=self.add_resistor,
            width=200,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669",
            corner_radius=10
        ).pack(pady=15)
        
        # Lista resistencias
        ctk.CTkLabel(
            left_frame,
            text=self.t['resistors'],
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(pady=(20, 10))
        
        self.resistor_frame = ctk.CTkScrollableFrame(
            left_frame,
            width=300,
            height=150,
            corner_radius=10
        )
        self.resistor_frame.pack(pady=(0, 20), padx=20, fill="both", expand=True)
        
        
        right_frame = ctk.CTkFrame(content_frame, corner_radius=15)
        right_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        
        ctk.CTkLabel(
            right_frame,
            text=self.t['calculator'],
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 20))
        
        # Método
        ctk.CTkLabel(
            right_frame,
            text=self.t['method'],
            font=ctk.CTkFont(size=13)
        ).pack(pady=(10, 5))
        
        self.method_var = ctk.StringVar(value='cramer')
        method_menu = ctk.CTkOptionMenu(
            right_frame,
            variable=self.method_var,
            values=['cramer', 'gauss', 'numerico'],
            width=250,
            height=40,
            font=ctk.CTkFont(size=13),
            dropdown_font=ctk.CTkFont(size=12),
            corner_radius=10
        )
        method_menu.pack(pady=(0, 20))
        
        # Botón calcular
        ctk.CTkButton(
            right_frame,
            text=self.t['calculate'],
            command=self.calculate,
            width=250,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            corner_radius=12
        ).pack(pady=20)
        
        # Resultados
        results_label = ctk.CTkLabel(
            right_frame,
            text=self.t['results'],
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#10b981"
        )
        results_label.pack(pady=(20, 10))
        
        self.results_frame = ctk.CTkScrollableFrame(
            right_frame,
            width=300,
            height=350,
            corner_radius=10,
            fg_color=("#f0f9ff", "#1a1a2e")
        )
        self.results_frame.pack(pady=(0, 20), padx=20, fill="both", expand=True)
    
    def change_circuit_type(self, value):
        "Cambia el tipo de circuito"
        self.circuit.set_circuit_type(value)
        print(f"Tipo de circuito cambiado a: {value.upper()} ✓✓✓")
    
    def update_resistor_list(self):
        "Actualiza la lista visual de resistencias"
        for widget in self.resistor_frame.winfo_children():
            widget.destroy()
        
        for i, r in enumerate(self.circuit.resistors):
            res_frame = ctk.CTkFrame(
                self.resistor_frame,
                corner_radius=8,
                fg_color=("#e0f2fe", "#1e293b")
            )
            res_frame.pack(fill="x", pady=5, padx=5)
            
            ctk.CTkLabel(
                res_frame,
                text=f"R{i+1} = {r:.1f} Ω",
                font=ctk.CTkFont(size=14, weight="bold", family="Courier")
            ).pack(side="left", padx=15, pady=10)
            
            ctk.CTkButton(
                res_frame,
                text=self.t['remove'],
                command=lambda idx=i: self.remove_resistor(idx),
                width=80,
                height=30,
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color="#ef4444",
                hover_color="#dc2626",
                corner_radius=6
            ).pack(side="right", padx=10, pady=5)
    
    def add_resistor(self):
        "Agrega una nueva resistencia"
        try:
            resistance = float(self.resistor_var.get())
            if resistance > 0:
                self.controller.add_resistor(resistance)
                self.resistor_var.set('3.0')
            else:
                messagebox.showwarning(
                    self.t['error'],
                    "La resistencia debe ser mayor a 0Ω"
                )
        except ValueError:
            messagebox.showerror(self.t['error'], "Valor inválido")
    
    def remove_resistor(self, index):
        "Elimina una resistencia"
        self.controller.remove_resistor(index)
    
    def calculate(self):
        "Calcula las corrientes del circuito"
        try:
            voltage = float(self.voltage_var.get())
            if voltage <= 0:
                messagebox.showwarning(
                    self.t['error'],
                    self.t['invalid_circuit']
                )
                return
            
            if len(self.circuit.resistors) < 2:
                messagebox.showwarning(
                    self.t['error'],
                    self.t['invalid_circuit']
                )
                return
            
            self.controller.set_voltage(voltage)
            
            method = self.method_var.get()
            self.controller.set_strategy(self.strategies[method])
            
            currents = self.controller.calculate_currents()
            
            if currents:
                self.display_results(currents)
            else:
                messagebox.showerror(
                    self.t['error'],
                    "Error en el cálculo"
                )
        
        except ValueError:
            messagebox.showerror(self.t['error'], "Valores inválidos")
    
    def display_results(self, currents):
        "Muestra los resultados del cálculo"
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        circuit_type_display = self.circuit_type_var.get().upper()
        circuit_type_label = ctk.CTkLabel(
            self.results_frame,
            text=f" Circuito: {circuit_type_display}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#8b5cf6"
        )
        circuit_type_label.pack(pady=(5, 15))
        
        for i, current in enumerate(currents):
            result_frame = ctk.CTkFrame(
                self.results_frame,
                corner_radius=8,
                fg_color=("#ecfdf5", "#0f5132")
            )
            result_frame.pack(fill="x", pady=5, padx=5)
            
            content_frame = ctk.CTkFrame(result_frame, fg_color="transparent")
            content_frame.pack(fill="x", padx=15, pady=10)
            
            ctk.CTkLabel(
                content_frame,
                text=f"{self.t['current']} I{i+1}:",
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(side="left")
            
            ctk.CTkLabel(
                content_frame,
                text=f"{current:.4f} A",
                font=ctk.CTkFont(size=14, weight="bold", family="Courier"),
                text_color="#10b981"
            ).pack(side="right", padx=(10, 0))
            
            direction = self.t['clockwise'] if current >= 0 else self.t['counterclockwise']
            ctk.CTkLabel(
                result_frame,
                text=f"{self.t['direction']}: {direction}",
                font=ctk.CTkFont(size=11),
                text_color="gray60"
            ).pack(pady=(0, 10))