from abc import ABC, abstractmethod
from typing import List, Optional
import numpy as np

class ResolutionStrategy(ABC):
    @abstractmethod
    def solve(self, circuit) -> Optional[List[float]]:
        pass

class CramerStrategy(ResolutionStrategy):
    def solve(self, circuit) -> Optional[List[float]]:
        try:
            A, b = circuit.build_mesh_system()
            
            if A is None or b is None:
                return None
            
            # Convertir a numpy arrays para cálculos
            A = np.array(A, dtype=float)
            b = np.array(b, dtype=float)
            
            n = len(b)
            
            # Calcular determinante de A
            det_A = self._determinant(A)
            
            if abs(det_A) < 1e-10:  # Sistema singular
                return None
            
            # Resolver usando Regla de Cramer
            solutions = []
            for i in range(n):
                # Crear matriz Ai reemplazando columna i con b
                Ai = A.copy()
                Ai[:, i] = b
                
                # Calcular determinante de Ai
                det_Ai = self._determinant(Ai)
                
                # Solución: xi = det(Ai) / det(A)
                xi = det_Ai / det_A
                solutions.append(xi)
            
            return solutions
            
        except Exception as e:
            print(f"Error en Cramer: {e}")
            return None
    
    def _determinant(self, matrix):
        matrix = np.array(matrix, dtype=float)
        n = matrix.shape[0]
        
        # Caso base: matriz 1x1
        if n == 1:
            return matrix[0, 0]
        
        # Caso base: matriz 2x2
        if n == 2:
            return matrix[0, 0] * matrix[1, 1] - matrix[0, 1] * matrix[1, 0]
        
        # Para matrices mayores: usar numpy (más eficiente)
        return np.linalg.det(matrix)

class GaussJordanStrategy(ResolutionStrategy):
    def solve(self, circuit) -> Optional[List[float]]:
        try:
            A, b = circuit.build_mesh_system()
            
            if A is None or b is None:
                return None
            
            # Convertir a numpy arrays
            A = np.array(A, dtype=float)
            b = np.array(b, dtype=float).reshape(-1, 1)
            
            n = len(b)
            
            # Crear matriz aumentada [A|b]
            augmented = np.hstack([A, b])
            
            # FASE 1: Eliminación hacia adelante
            for i in range(n):
                # Buscar el pivote
                max_row = i
                for k in range(i + 1, n):
                    if abs(augmented[k, i]) > abs(augmented[max_row, i]):
                        max_row = k
                
                # Intercambiar filas si es necesario
                if max_row != i:
                    augmented[[i, max_row]] = augmented[[max_row, i]]
                
                # Verificar si el pivote es cero
                if abs(augmented[i, i]) < 1e-10:
                    return None  # Sistema singular o inconsistente
                
                # Hacer el pivote = 1
                augmented[i] = augmented[i] / augmented[i, i]
                
                # Hacer ceros en toda la columna (arriba y abajo del pivote)
                for k in range(n):
                    if k != i:
                        factor = augmented[k, i]
                        augmented[k] = augmented[k] - factor * augmented[i]
            
            # Las soluciones están en la última columna
            solutions = augmented[:, -1].tolist()
            
            return solutions
            
        except Exception as e:
            print(f"Error en Gauss-Jordan: {e}")
            return None

class NumericStrategy(ResolutionStrategy): 
    def solve(self, circuit) -> Optional[List[float]]:
        try:
            A, b = circuit.build_mesh_system()
            
            if A is None or b is None:
                return None
            
            # Convertir a numpy arrays
            A = np.array(A, dtype=float)
            b = np.array(b, dtype=float)
            
            # Verificar que la matriz no sea singular
            if abs(np.linalg.det(A)) < 1e-10:
                return None
            
            # Resolver usando  NumPy
            solutions = np.linalg.solve(A, b)
            
            # Verificar que las soluciones sean válidas
            if np.any(np.isnan(solutions)) or np.any(np.isinf(solutions)):
                return None
            
            return solutions.tolist()
            
        except np.linalg.LinAlgError:
            print("Error: Sistema singular o mal condicionado")
            return None
        except Exception as e:
            print(f"Error en método numérico: {e}")
            return None