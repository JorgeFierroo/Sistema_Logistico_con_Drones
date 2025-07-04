from sim.simulation import Simulation
from sim.persistence import save_simulation, load_simulation

_simulation_instance = load_simulation() or Simulation()

def run_simulation(n_nodes: int, n_edges: int, n_orders: int) -> Simulation:
    _simulation_instance.initialize(n_nodes, n_edges, n_orders)
    save_simulation(_simulation_instance)
    return _simulation_instance

def get_current_simulation() -> Simulation:
    return _simulation_instance
