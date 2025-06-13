class Client:
    def __init__(self, node_id):
        self.node_id = node_id
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def __str__(self):
        return f"Client({self.node_id}, Orders: {len(self.orders)})"
