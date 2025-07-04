from fastapi import APIRouter, HTTPException
from typing import List
from sim.persistence import load_simulation

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/clients")
def get_all_clients():
    sim = load_simulation()
    if sim is None:
        raise HTTPException(status_code=404, detail="Simulación no inicializada")
    return [c.to_dict() for c in sim.get_clients()]

@router.get("/cliente/{cliente_id}")
def get_cliente(cliente_id: str):
    sim = load_simulation()   # <-- obtener siempre la instancia actual
    for cliente in sim.get_clients():
        if cliente.client_id == cliente_id:
            return cliente.to_dict()
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@router.get("/test_clients")
def test_clients():
    sim = load_simulation()
    clients = sim.get_clients()
    print("Clientes en API:", clients)  
    return {"num_clients": len(clients), "clients": [c.to_dict() for c in clients]}
