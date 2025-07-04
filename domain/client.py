import random

class Client:
    _contador = 0

    def __init__(self):
        Client._contador += 1
        self.client_id = f"C{Client._contador:03d}"
        self.name = f"Client{Client._contador}"
        self.vertex = None  
        self.type = random.choice(["alta", "media", "baja"])
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def to_dict(self):
        return {
            "cliente_id": self.client_id,
            "Nombre": self.name,
            "Tipo": self.type,
            "Ordenes": len(self.orders)
        }

    def __str__(self):
        return f"[{self.client_id}] {self.name} ({self.type}) - {len(self.orders)} orden(es)"

    def __repr__(self):
        return self.__str__()

    def get_orders(self):
        """Devuelve la lista de órdenes asociadas a este cliente."""
        return self.orders