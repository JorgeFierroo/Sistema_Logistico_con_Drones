import datetime
import uuid
import hashlib

class Order:

    def __init__(self, origin, destination, route=None, cost=None):
        

        uid = str(uuid.uuid4())

        # Crear hash (puedes elegir SHA256, SHA1, etc.)
        self.order_id = hashlib.sha256(uid.encode()).hexdigest()[:8]  # Ej: 'a3f5e9d1'
        self.cliente = None
        self.id_cliente = None
        self.origin = origin
        self.destination = destination
        self.status = "pendiente"
        self.priority = 0
        self.created_at = datetime.datetime.now()
        self.delivered_at = None
        self.route_cost = cost

    def entregar(self):
        self.delivered_at = datetime.datetime.now()

    def __str__(self):
        return f"Order #{self.order_id}: {self.origin} → {self.destination} {self.created_at} | Cost: {self.route_cost}"

    def to_dict(self):
        return {
            "Id_orden": self.order_id,
            "Origen": str(self.origin),
            "Destino": str(self.destination),
            "Estado": self.status,
            "Prioriedad": self.priority,
            "Creado en": self.created_at,
            "Entregado en": self.delivered_at,
            "Costo de ruta": self.route_cost
        }
    