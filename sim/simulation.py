import random
from model.graph import Graph
from domain.client import Client
from domain.order import Order
from domain.route import Route

class Simulation:
    def __init__(self):
        self.graph = Graph(directed=False)
        self.clients = []
        self.orders = []
        self.routes = []
        self.node_roles = {}  # maps vertex -> role ("client", "storage", "recharge")

    def initialize(self, n_nodes, n_edges, n_orders):
        self.graph = Graph(directed=False)
        self.clients = []
        self.orders = []
        self.routes = []
        self.node_roles = {}

        self._create_nodes(n_nodes)
        self._create_edges(n_edges)
        self._assign_roles()
        self._generate_orders(n_orders)

    def _create_nodes(self, n):
        for i in range(n):
            label = chr(65 + i) if i < 26 else f"N{i}"
            v = self.graph.insert_vertex(label)
            self.node_roles[v] = None  # initialize without role

    def _create_edges(self, m):
        vertices = list(self.graph.vertices())
        connected = set()
        if len(vertices) < 2:
            return

        # Create a spanning tree to ensure connectivity
        random.shuffle(vertices)
        for i in range(len(vertices) - 1):
            u = vertices[i]
            v = vertices[i + 1]
            cost = random.randint(1, 20)
            self.graph.insert_edge(u, v, cost)
            connected.add((u, v))

        # Add extra edges
        while len(list(self.graph.edges())) < m:
            u, v = random.sample(vertices, 2)
            if self.graph.get_edge(u, v) is None:
                cost = random.randint(1, 20)
                self.graph.insert_edge(u, v, cost)

    def _assign_roles(self):
        vertices = list(self.graph.vertices())
        n = len(vertices)
        num_storage = int(n * 0.2)
        num_recharge = int(n * 0.2)
        num_clients = n - num_storage - num_recharge

        random.shuffle(vertices)
        for i, v in enumerate(vertices):
            if i < num_storage:
                self.node_roles[v] = "storage"
            elif i < num_storage + num_recharge:
                self.node_roles[v] = "recharge"
            else:
                self.node_roles[v] = "client"
                self.clients.append(Client(v.element()))

    def _generate_orders(self, count):
        storages = [v for v, r in self.node_roles.items() if r == "storage"]
        clients = [v for v, r in self.node_roles.items() if r == "client"]

        for _ in range(count):
            if not storages or not clients:
                continue
            origin = random.choice(storages)
            destination = random.choice(clients)
            self.orders.append(Order(origin, destination))

    def get_node_roles(self):
        return self.node_roles

    def get_orders(self):
        return self.orders

    def get_graph(self):
        return self.graph

    def get_clients(self):
        return self.clients

    def get_routes(self):
        return self.routes

    def add_route(self, route):
        self.routes.append(route)
