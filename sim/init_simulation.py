import sys
import os

# Agregar rutas a sys.path para facilitar importaciones
ruta_model = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model'))
ruta_domain = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'domain'))
ruta_tda = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tda'))

sys.path.append(ruta_model)
sys.path.append(ruta_domain)
sys.path.append(ruta_tda)

from simulation import Simulation

# Instancia global (puede ser reinicializada)
_simulation_instance = Simulation()

def run_simulation(n_nodes: int, n_edges: int, n_orders: int) -> Simulation:
    """
    Inicializa una nueva simulación con los parámetros dados.

    Parámetros:
        - n_nodes: cantidad de nodos del grafo
        - n_edges: cantidad de aristas
        - n_orders: cantidad de órdenes

    Retorna:
        - Instancia de Simulation con grafo, roles, pedidos y rutas.
    """
    _simulation_instance.initialize(n_nodes, n_edges, n_orders)
    return _simulation_instance

def get_current_simulation() -> Simulation:
    """
    Devuelve la instancia actual de simulación.
    Útil para acceder a datos desde otras pestañas.
    """
    return _simulation_instance
