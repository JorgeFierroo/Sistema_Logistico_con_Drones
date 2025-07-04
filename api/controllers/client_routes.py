from fastapi import APIRouter, HTTPException
from typing import List
import sys, os

current_dir  = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.extend([project_root,os.path.join(project_root, 'domain'), os.path.join(project_root, 'sim'),])

from domain.client import Client
from sim.init_simulation import get_current_simulation

router = APIRouter(prefix="/clients", tags=["Clients"])

simulation = get_current_simulation()

@router.get("/", response_model=List[dict])
def get_all_clients():
    """
    Retorna una lista con los datos de todos los clientes.
    """
    clients = simulation.get_clients()
    return [client.to_dict() for client in clients]

@router.get("/{client_id}")
def get_client_info(client_id: str):
    """
    Obtiene información detallada de un cliente específico.
    """
    for client in simulation.get_clients():
        if str(client) == client_id:
            return client.to_dict()
    raise HTTPException(status_code=404, detail="Cliente no encontrado")