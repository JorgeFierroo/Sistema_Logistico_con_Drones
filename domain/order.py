import datetime
import uuid
import hashlib

class Order:

    def __init__(self, origin, destination, route, cost=None, priority=0, battery_used=0, recharges=None, full_path=None):
        uid = str(uuid.uuid4())
        self.order_id = hashlib.sha256(uid.encode()).hexdigest()[:8]
        self.cliente = None
        self.id_cliente = None
        self.route = route
        self.origin = origin
        self.destination = destination
        self.status = "pendiente"
        self.priority = priority
        self.created_at = datetime.datetime.now()
        self.delivered_at = None
        self.route_cost = cost
        self.battery_used = battery_used
        self.recharges = recharges or []
        self.full_path = full_path or []

    def entregar(self):
        self.status = "entregado"
        self.delivered_at = datetime.datetime.now()

    def __str__(self):
        return f"Order #{self.order_id}: {self.origin} → {self.destination} | Cost: {self.route_cost} | Battery: {self.battery_used}"

    def to_dict(self):
        return {
            "Id_orden": self.order_id,
            "Origen": str(self.origin),
            "Destino": str(self.destination),
            "Estado": self.status,
            "Prioridad": self.priority,
            "Creado en": self.created_at,
            "Entregado en": self.delivered_at,
            "Costo de ruta": self.route_cost,
            "Batería usada": self.battery_used,
            "Recargas": [str(r) for r in self.recharges],
            "Ruta completa": [str(n) for n in self.full_path]
        }
