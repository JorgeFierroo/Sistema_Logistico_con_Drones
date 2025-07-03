from fastapi import APIRouter, HTTPException
from typing import List, Dict
from sim.simulation import Simulation
from domain.order import Order

router = APIRouter()

# Instancia global compartida
simulation = Simulation()

@router.get("/", response_model=List[Dict])
def get_all_orders():
    """
    Retorna todas las órdenes generadas en la simulación.
    """
    return [order.to_dict() for order in simulation.get_orders()]

@router.get("/{order_id}", response_model=Dict)
def get_order_by_id(order_id: str):
    """
    Retorna una orden específica dado su ID.
    """
    for order in simulation.get_orders():
        if order.order_id == order_id:
            return order.to_dict()
    raise HTTPException(status_code=404, detail="Orden no encontrada")

@router.post("/generar/{cantidad}")
def generar_ordenes(cantidad: int):
    """
    Genera nuevas órdenes aleatorias para testing o simulación.
    """
    simulation._generate_orders(cantidad)
    return {"mensaje": f"{cantidad} órdenes generadas exitosamente."}
