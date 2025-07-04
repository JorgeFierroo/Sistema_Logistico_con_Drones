import pickle
import os

SIM_PATH = os.path.join(os.path.dirname(__file__), 'sim_state.pkl')

def save_simulation(simulation):
    with open(SIM_PATH, 'wb') as f:
        pickle.dump(simulation, f)

def load_simulation():
    if os.path.exists(SIM_PATH):
        with open(SIM_PATH, 'rb') as f:
            return pickle.load(f)
    return None
