from fastapi import APIRouter
import sys, os

current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.extend([project_root, os.path.join(project_root, 'sim')])

from sim.init_simulation import get_current_simulation

router = APIRouter()
simulation = get_current_simulation()

@router.get("/mst")
def obtener_mst():
    mst_edges = simulation.get_mst_edges()
    return [{"from": e.endpoints()[0].element(),
             "to": e.endpoints()[1].element(),
             "weight": e.element()} for e in mst_edges]