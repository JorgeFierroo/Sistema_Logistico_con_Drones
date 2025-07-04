class Route:
    def __init__(self, path, cost):
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
    
    def get_cost(self):
        return self.cost
