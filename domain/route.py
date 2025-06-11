class Route:
    def __init__(self, path, cost, recharge_points=None):
        self.path = path  # lista de nodos o nombres
        self.cost = cost  # suma de pesos
        self.recharge_points = recharge_points or []

    def __str__(self):
        route_str = " → ".join(str(p) for p in self.path)
        return f"Path: {route_str} | Cost: {self.cost}"

    def __repr__(self):
        return self.__str__()

    def includes_recharge(self):
        return len(self.recharge_points) > 0

    def start(self):
        return self.path[0] if self.path else None

    def end(self):
        return self.path[-1] if self.path else None