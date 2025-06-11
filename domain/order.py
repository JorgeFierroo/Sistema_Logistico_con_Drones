class Order:
    _id_counter = 0

    def __init__(self, origin, destination, path, cost):
        Order._id_counter += 1
        self.id = f"ORD-{Order._id_counter:04d}"
        self.origin = origin
        self.destination = destination
        self.path = path  # lista de nodos o strings
        self.cost = cost
        self.status = "completed"  # por ahora asumimos entregada tras simular

    def __str__(self):
        return f"{self.id} | From {self.origin} to {self.destination} | Cost: {self.cost}"

    def __repr__(self):
        return self.__str__()