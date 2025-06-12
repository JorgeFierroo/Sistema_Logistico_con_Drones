import random
from model.graph import Graph
from domain.client import Client
from domain.order import Order
from domain.route import Route

def initialize_simulation(num_nodes, num_edges, num_orders):
    graph = Graph(directed=False)
    vertices = []

    # Asignar roles proporcionalmente
    roles = (["client"] * int(num_nodes * 0.6) +
             ["storage"] * int(num_nodes * 0.2) +
             ["recharge"] * int(num_nodes * 0.2))
    random.shuffle(roles)

    # Crear nodos con sus roles
    for i in range(num_nodes):
        label = f"N{i}"
        v = graph.insert_vertex(label)
        v.role = roles[i]  # Asegúrate de que tu clase Vertex lo soporte
        vertices.append(v)

    # Crear grafo conexo base (n - 1 aristas mínimo)
    connected = set()
    connected.add(vertices[0])
    while len(connected) < num_nodes:
        a = random.choice(list(connected))
        b = random.choice([v for v in vertices if v not in connected])
        weight = random.randint(1, 15)
        graph.insert_edge(a, b, weight)
        connected.add(b)

    # Agregar aristas extra (si se requieren más de n - 1)
    extra_edges = num_edges - (num_nodes - 1)
    attempts = 0
    while extra_edges > 0 and attempts < num_edges * 5:
        u, v = random.sample(vertices, 2)
        if graph.get_edge(u, v) is None:
            cost = random.randint(1, 15)
            graph.insert_edge(u, v, cost)
            extra_edges -= 1
        attempts += 1

    # Crear órdenes entre almacenamiento y clientes
    storage_nodes = [v for v in vertices if v.role == "storage"]
    client_nodes = [v for v in vertices if v.role == "client"]
    orders = []
    for _ in range(num_orders):
        origin = random.choice(storage_nodes)
        destination = random.choice(client_nodes)
        orders.append(Order(origin=origin, destination=destination))

    # Retornar información útil para la interfaz
    return graph, {
        "storage": storage_nodes,
        "recharge": [v for v in vertices if v.role == "recharge"],
        "client": client_nodes
    }, orders
