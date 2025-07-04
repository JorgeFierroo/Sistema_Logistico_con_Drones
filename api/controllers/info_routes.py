from fastapi import APIRouter
import sys, os

current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.extend([project_root, os.path.join(project_root, 'sim')])

from sim.init_simulation import get_current_simulation

router = APIRouter()
simulation = get_current_simulation()

@router.get("/info/reports/summary")
def obtener_info_general():
    graph = simulation.get_graph()
    orders = simulation.get_orders()
    roles = simulation.get_node_roles()
    total_nodos = len(list(graph.vertices()))
    total_aristas = len(list(graph.edges()))
    total_ordenes = len(orders)

    conteo_roles = {"client": 0, "storage": 0, "recharge": 0}
    for rol in roles.values():
        if rol in conteo_roles:
            conteo_roles[rol] += 1

    return {
        "nodos": total_nodos,
        "aristas": total_aristas,
        "ordenes": total_ordenes,
        "clientes": conteo_roles["client"],
        "almacenes": conteo_roles["storage"],
        "recargas": conteo_roles["recharge"]
    }

@router.get("/info/reports/visits")
def visitas_por_tipo():
    return simulation.get_visits_by_role()

@router.get("/info/reports/visits/clients")
def visitas_clientes():
    return simulation.get_visits_by_role().get("client", {})

@router.get("/info/reports/visits/recharges")
def visitas_recargas():
    return simulation.get_visits_by_role().get("recharge", {})

@router.get("/info/reports/visits/storages")
def visitas_almacenes():
    return simulation.get_visits_by_role().get("storage", {})