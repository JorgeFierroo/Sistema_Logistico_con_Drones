class Route:
    def __init__(self, path, cost):
        """
        Representa una ruta en el sistema.

        :param path: Lista de nodos (Vertex) por los que pasa la ruta.
        :param cost: Costo total de la ruta (suma de pesos de aristas).
        """
        self.path = path
        self.cost = cost

    def __str__(self):
        path_str = " → ".join(str(v) for v in self.path)
        return f"Path: {path_str} | Cost: {self.cost}"

    def to_dict(self):
        return {
            "path": [str(v) for v in self.path],
            "cost": self.cost
        }
