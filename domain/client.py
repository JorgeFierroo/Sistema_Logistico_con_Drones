class Client:
    def __init__(self, id_vertex):
        self.id_vertex = id_vertex  # puede ser string o Vertex
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def total_orders(self):
        return len(self.orders)

    def __str__(self):
        return f"Client({self.id_vertex}) - {len(self.orders)} order(s)"

    def __repr__(self):
        return self.__str__()
