from sim.simulation import Simulation

# Instancia global (puede ser reinicializada)
_simulation_instance = Simulation()

def run_simulation(n_nodes: int, n_edges: int, n_orders: int) -> Simulation:
    _simulation_instance.initialize(n_nodes, n_edges, n_orders)
    return _simulation_instance

def get_current_simulation() -> Simulation:
    return _simulation_instance
