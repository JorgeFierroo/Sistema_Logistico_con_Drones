class Order:
    _id_counter = 1

    def __init__(self, origin, destination, route=None, cost=None):
        self.id = Order._id_counter
        Order._id_counter += 1
        self.origin = origin
        self.destination = destination
        self.route = route or []
        self.cost = cost

    def __str__(self):
        return f"Order #{self.id}: {self.origin} → {self.destination} | Cost: {self.cost} | Route: {self.route}"

    def to_dict(self):
        return {
            "id": self.id,
            "origin": str(self.origin),
            "destination": str(self.destination),
            "cost": self.cost,
            "route": [str(v) for v in self.route]
        }
