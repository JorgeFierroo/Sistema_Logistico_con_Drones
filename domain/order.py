from datetime import datetime

class Pedido:
    def __init__(self, id_pedido: str, cliente: object, id_cliente: str,
                 origen: str, destino: str, costo_ruta: float,
                 prioridad: int = 0, estado: str = "pendiente"):
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.id_cliente = id_cliente
        self.origen = origen
        self.destino = destino
        self.estado = estado  
        self.prioridad = prioridad
        self.creado_en = datetime.now()
        self.entregado_en = None
        self.costo_ruta = costo_ruta

    def marcar_como_entregado(self):
        self.estado = "entregado"
        self.entregado_en = datetime.now()

    def __repr__(self):
        return (f"Pedido(ID: {self.id_pedido}, Cliente: {self.cliente.name}, "
                f"Estado: {self.estado}, Prioridad: {self.prioridad}, "
                f"Creado: {self.creado_en}, Entregado: {self.entregado_en}, "
                f"Costo: {self.costo_ruta})")
