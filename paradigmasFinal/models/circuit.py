from typing import List, Tuple

class Observer:
    #"Interfaz Observer"
    def update(self, subject):
        pass

class Subject: #CLASE PARA PATRON OBSERVER
    def __init__(self):
        self._observers: List[Observer] = []
    
    def add_observer(self, observer: Observer):
        self._observers.append(observer)
    
    def notify_observers(self):
        for observer in self._observers:
            observer.update(self)

class Circuit(Subject):
    #Singleton Pattern: Garantiza una única instancia del circuito
    #SRP: Responsable solo de mantener el estado del circuito
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        super().__init__()
        self.voltage: float = 15.0
        self.resistors: List[float] = [7.0, 5.0, 2.0]
        self.circuit_type: str = 'serie'  # 'serie', 'paralelo', 'mallas'
        self._initialized = True
    
    def set_voltage(self, voltage: float):
        self.voltage = voltage
        self.notify_observers()
    
    def set_circuit_type(self, circuit_type: str):
        if circuit_type in ['serie', 'paralelo', 'mallas']:
            self.circuit_type = circuit_type
            self.notify_observers()
    
    def add_resistor(self, resistance: float):
        if resistance > 0:
            self.resistors.append(resistance)
            self.notify_observers()
    
    def remove_resistor(self, index: int):
        if 0 <= index < len(self.resistors):
            self.resistors.pop(index)
            self.notify_observers()
    
    def build_mesh_system(self) -> Tuple[List[List[float]], List[float]]:
        """
        Construye el sistema de ecuaciones para análisis de mallas
        
        Para un circuito con N resistencias, se crean N-1 mallas:
        Malla 1: R1*I1 + R2*(I1-I2) = V
        Malla 2: R2*(I2-I1) + R3*(I2-I3) = 0
        Malla 3: R3*(I3-I2) + R4*I3 = 0
        ...
        
        Returns:
            Tuple[A, b] donde A es la matriz de coeficientes y b el vector de términos independientes
        """
        n = len(self.resistors)
        
        if n < 2:
            return None, None
        
        # Crear matriz de coeficientes A y vector b
        A = []
        b = []
        
        if self.circuit_type == 'serie':
            # Sistema simple: (R1+R2+...+Rn)*I = V
            A = [[sum(self.resistors)]]
            b = [self.voltage]
            
        elif self.circuit_type == 'paralelo':
            # Sistema diagonal: Ri*Ii = V para cada rama
            A = [[0.0] * n for _ in range(n)]
            for i in range(n):
                A[i][i] = self.resistors[i]
            b = [self.voltage] * n
            
        else:  # mallas (configuración compleja)
            # Crear sistema de N ecuaciones para N corrientes de malla
            num_meshes = n
            A = [[0.0] * num_meshes for _ in range(num_meshes)]
            b = [0.0] * num_meshes
            
            # Primera malla tiene la fuente de voltaje
            b[0] = self.voltage
            
            for i in range(num_meshes):
                # Diagonal principal: suma de resistencias en la malla i
                if i == 0:
                    A[i][i] = self.resistors[i] + (self.resistors[i+1] if i+1 < n else 0)
                elif i == num_meshes - 1:
                    A[i][i] = self.resistors[i]
                else:
                    A[i][i] = self.resistors[i] + (self.resistors[i+1] if i+1 < n else 0)
                
                # Elementos fuera de la diagonal: resistencias compartidas
                if i > 0:
                    A[i][i-1] = -self.resistors[i]
                if i < num_meshes - 1:
                    A[i][i+1] = -(self.resistors[i+1] if i+1 < n else 0)
        
        return A, b
    
    @classmethod
    def get_instance(cls):
        """Obtiene la instancia única del circuito"""
        if cls._instance is None:
            cls._instance = Circuit()
        return cls._instance