import random
import sys
import os

current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))

# Agregar las rutas necesarias
sys.path.insert(0, project_root)  # RaÃz del proyecto
sys.path.append(os.path.join(project_root, 'domain'))
sys.path.append(os.path.join(project_root, 'model'))
sys.path.append(os.path.join(project_root, 'sim'))
sys.path.append(os.path.join(project_root, 'tda'))



from domain.client import Client
from domain.order import Order
from domain.route import Route
from model.graph import Graph

from tda.avl import insert as avl_insert, delete_node as avl_delete, Node as AVLNode
from tda.hasp_map import HashMap

class Simulation:
    def __init__(self):
        self.graph = Graph(directed=False)
        self.clients = []
        self.orders = []
        self.routes = []
        self.node_roles = {}  # maps vertex -> role ("client", "storage", "recharge")
        self.route_avl = None
        self.route_counts = HashMap()

    def initialize(self, n_nodes, n_edges, n_orders):
        self.graph = Graph(directed=False)
        self.clients = []
        self.orders = []
        self.routes = []
        self.node_roles = {}
        self.route_avl = None
        self.route_counts = HashMap()

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
        if len(vertices) < 2:
            return

        # Create a spanning tree to ensure connectivity
        random.shuffle(vertices)
        for i in range(len(vertices) - 1):
            u = vertices[i]
            v = vertices[i + 1]
            cost = random.randint(1, 20)
            self.graph.insert_edge(u, v, cost)

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
                self.clients.append(Client())

    def _generate_orders(self, count):
        storages = [v for v, r in self.node_roles.items() if r == "storage"]
        clients = [v for v, r in self.node_roles.items() if r == "client"]

        for _ in range(count):
            if not storages or not clients:
                continue
            origin = random.choice(storages)
            destination = random.choice(clients)
            order = Order(origin, destination)
            self.orders.append(order)

            route = Route([origin.element(), destination.element()], cost=0)
            self.routes.append(route)
            order.route_cost = route.get_cost()


            if self.route_avl is None:
                self.route_avl = AVLNode(str(route))
            else:
                self.route_avl = avl_insert(self.route_avl, str(route))

            clave = str(route)
            valor_actual = self.route_counts.get(clave, 0)
            self.route_counts.set(clave, valor_actual + 1)


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

    def get_route_avl(self):
        return self.route_avl

    def get_route_counts(self):
        return self.route_counts

    def add_route(self, route):
        self.routes.append(route)
        if self.route_avl is None:
            self.route_avl = AVLNode(str(route))
        else:
            self.route_avl = avl_insert(self.route_avl, str(route))

        self.route_counts[str(route)] = self.route_counts.get(str(route), 0) + 1

    def get_visits_by_role(self):
        counts = {}  # vertex.element() -> cantidad

        for route in self.routes:
            for node_label in route.path:
                counts[node_label] = counts.get(node_label, 0) + 1

        result = {
            "client": {},
            "recharge": {},
            "storage": {}
        }

        for vertex, role in self.node_roles.items():
            label = vertex.element()
            if role in result:
                result[role][label] = counts.get(label, 0)

        return result
