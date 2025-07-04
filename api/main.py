import os, sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Agregar el path raíz del proyecto al sys.path
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

# Importa los routers
from .controllers import client_routes, info_routes, order_routes, report_routes, mst_routes

app = FastAPI(
    title="Sistema Logístico de Drones",
    version="2.0",
    description="API RESTful para simulación de entregas con drones autónomos."
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar los routers
app.include_router(client_routes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(order_routes.router, prefix="/ordenes", tags=["Órdenes"])
app.include_router(info_routes.router, prefix="/info", tags=["Información General"])
app.include_router(report_routes.router, prefix="/reporte", tags=["Informe PDF"])
app.include_router(mst_routes.router, prefix="/info", tags=["Árbol Mínimo"])
