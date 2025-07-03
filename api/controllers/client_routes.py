from fastapi import APIRouter, HTTPException
from typing import List
from sim.simulation import Simulation
from domain.client import Client

router = APIRouter()

# Instancia compartida (puede cambiarse por DI o un singleton si es necesario)
simulation = Simulation()

@router.get("/", response_model=List[str])
def get_all_clients():
    """
    Retorna una lista con los nombres/identificadores de todos los clientes.
    """
    clients = simulation.get_clients()
    return [str(client) for client in clients]

@router.get("/{client_id}")
def get_client_info(client_id: str):
    """
    Obtiene información detallada de un cliente específico.
    """
    for client in simulation.get_clients():
        if str(client) == client_id:
            return {"id": client_id, "info": "Información simulada del cliente"}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")
