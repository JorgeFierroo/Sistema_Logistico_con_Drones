from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import client_routes, order_routes, info_routes

app = FastAPI(
    title="Sistema Logístico de Drones",
    version="2.0",
    description="API RESTful para simulación de entregas con drones autónomos."
)

# Configurar CORS para permitir acceso desde frontend (Streamlit u otro)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers definidos en otros archivos
app.include_router(client_routes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(order_routes.router, prefix="/ordenes", tags=["Órdenes"])
app.include_router(info_routes.router, prefix="/info", tags=["Información General"])
