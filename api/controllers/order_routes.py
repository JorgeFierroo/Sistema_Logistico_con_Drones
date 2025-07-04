# api/controllers/order_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import sys, os

current_dir  = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.extend([
    project_root,
    os.path.join(project_root, 'sim'),
    os.path.join(project_root, 'domain')
])

from sim.init_simulation import get_current_simulation
from domain.order        import Order

router      = APIRouter()
simulation  = get_current_simulation()          # instancia compartida


# ---------------------------------------------------------------------- #
# ---------------------------  MODELO Pydantic  ------------------------- #
# ---------------------------------------------------------------------- #
class OrderPayload(BaseModel):
    Id_orden:        str
    Origen:          str
    Destino:         str
    Prioridad:       int
    Costo_de_ruta:   int
    Bateria_usada:   int
    Recargas:        list[str] | None = []
    Ruta_completa:   list[str]


# ---------------------------------------------------------------------- #
# --------------------------  ENDPOINTS GET ---------------------------- #
# ---------------------------------------------------------------------- #
@router.get("/", response_model=List[Dict])
def get_all_orders():
    return [o.to_dict() for o in simulation.get_orders()]


@router.get("/{order_id}", response_model=Dict)
def get_order_by_id(order_id: str):
    for o in simulation.get_orders():
        if o.order_id == order_id:
            return o.to_dict()
    raise HTTPException(status_code=404, detail="Orden no encontrada")


# ---------------------------------------------------------------------- #
# --------------------------  ENDPOINTS POST --------------------------- #
# ---------------------------------------------------------------------- #
@router.post("/crear", status_code=201)
def crear_orden(payload: OrderPayload):
    """
    Recibe un JSON desde el frontend y lo registra
    tanto en la simulación en memoria como en la lista
    expuesta por este controlador.
    """
    # 1) Mapear labels de nodos a vértices reales
    origin_v = next((v for v in simulation.graph.vertices()
                     if str(v) == payload.Origen), None)
    dest_v   = next((v for v in simulation.graph.vertices()
                     if str(v) == payload.Destino), None)

    if origin_v is None or dest_v is None:
        raise HTTPException(status_code=400,
                            detail="Origen o destino no existen en el grafo")

    # 2) Crear objeto Order coherente
    order = Order(
        origin        = origin_v,
        destination   = dest_v,
        route         = payload.Ruta_completa,
        cost          = payload.Costo_de_ruta,
        priority      = payload.Prioridad,
        battery_used  = payload.Bateria_usada,
        recharges     = payload.Recargas,
        full_path     = payload.Ruta_completa
    )
    order.order_id  = payload.Id_orden        # conservar mismo id
    order.status    = "entregado"             # viene como ya entregada

    # 3) Asociar cliente a la orden
    for cli in simulation.clients:
        if cli.vertex == dest_v:
            order.cliente     = cli
            order.id_cliente  = cli.client_id
            cli.add_order(order)
            break

    simulation.orders.append(order)
    return {"mensaje": "Orden registrada en backend", "orden": order.to_dict()}


@router.post("/generar/{cantidad}")
def generar_ordenes(cantidad: int):
    simulation._generate_orders(cantidad)
    return {"mensaje": f"{cantidad} órdenes generadas exitosamente."}


@router.post("/{order_id}/cancel")
def cancelar_orden(order_id: str):
    for o in simulation.get_orders():
        if o.order_id == order_id:
            if o.status == "pendiente":
                o.status = "cancelada"
                return {"mensaje": f"Orden {order_id} cancelada."}
            return {"error": f"No se puede cancelar: estado {o.status}"}
    raise HTTPException(status_code=404, detail="Orden no encontrada")


@router.post("/{order_id}/complete")
def completar_orden(order_id: str):
    for o in simulation.get_orders():
        if o.order_id == order_id:
            if o.status == "pendiente":
                o.status = "entregado"
                return {"mensaje": f"Orden {order_id} completada."}
            return {"error": f"No se puede completar: estado {o.status}"}
    raise HTTPException(status_code=404, detail="Orden no encontrada")
