from fastapi import APIRouter, HTTPException
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
from domain.order import Order

router = APIRouter()
simulation = get_current_simulation()

@router.get("/", response_model=List[Dict])
def get_all_orders():
    return [order.to_dict() for order in simulation.get_orders()]

@router.get("/orders/{order_id}", response_model=Dict)
def get_order_by_id(order_id: str):
    for order in simulation.get_orders():
        if order.order_id == order_id:
            return order.to_dict()
    raise HTTPException(status_code=404, detail="Orden no encontrada")

@router.post("/generar/{cantidad}")
def generar_ordenes(cantidad: int):
    simulation._generate_orders(cantidad)
    return {"mensaje": f"{cantidad} órdenes generadas exitosamente."}

@router.post("/orders/{order_id}/cancel")
def cancelar_orden(order_id: str):
    for order in simulation.get_orders():
        if order.order_id == order_id:
            if order.status == "pendiente":
                order.status = "cancelada"
                return {"mensaje": f"Orden {order_id} cancelada exitosamente."}
            else:
                return {"error": f"La orden {order_id} no puede ser cancelada (estado actual: {order.status})."}
    raise HTTPException(status_code=404, detail="Orden no encontrada")

@router.post("/orders/{order_id}/complete")
def completar_orden(order_id: str):
    for order in simulation.get_orders():
        if order.order_id == order_id:
            if order.status == "pendiente":
                order.status = "entregado"
                return {"mensaje": f"Orden {order_id} marcada como entregada."}
            else:
                return {"error": f"La orden {order_id} no puede completarse (estado actual: {order.status})."}
    raise HTTPException(status_code=404, detail="Orden no encontrada")
