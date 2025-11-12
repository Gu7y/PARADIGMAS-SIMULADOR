from typing import List, Optional

class CircuitController:
    def __init__(self, strategy):
        from models.circuit import Circuit
        self.circuit = Circuit.get_instance()
        self.strategy = strategy
    
    def set_strategy(self, strategy):
        self.strategy = strategy
    
    def calculate_currents(self) -> Optional[List[float]]:
        return self.strategy.solve(self.circuit)
    
    def add_resistor(self, resistance: float):
        self.circuit.add_resistor(resistance)
    
    def remove_resistor(self, index: int):
        self.circuit.remove_resistor(index)
    
    def set_voltage(self, voltage: float):
        self.circuit.set_voltage(voltage)
    
    def get_circuit_data(self):
        return {
            'voltage': self.circuit.voltage,
            'resistors': self.circuit.resistors.copy()
        }
