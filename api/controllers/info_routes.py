from fastapi import APIRouter
from sim.simulation import Simulation

router = APIRouter()

# Simulación compartida (debes asegurarte que sea la misma usada en otras rutas)
simulation = Simulation()

@router.get("/info/general")
def obtener_info_general():
    """
    Retorna información general sobre la simulación actual.
    """
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

@router.get("/info/visits")
def visitas_por_tipo():
    """
    Retorna el número de visitas por tipo de nodo (basado en rutas).
    """
    visitas = simulation.get_visits_by_role()
    return visitas
