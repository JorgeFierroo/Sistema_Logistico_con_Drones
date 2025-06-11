import random
from model.graph import Graph
from model.vertex import Vertex

def generate_connected_graph(n_nodes, m_edges):
    if m_edges < n_nodes - 1:
        raise ValueError("El número de aristas debe ser al menos n_nodes - 1 para garantizar conectividad.")

    graph = Graph()
    nodes = []

    # Crear vértices y agregarlos al grafo
    for i in range(n_nodes):
        node_id = chr(65 + i)  # A, B, C, D...
        v = Vertex(node_id)
        v.role = None  # Añadir atributo dinámicamente si no está en __init__
        nodes.append(graph.insert_vertex(v))

    # Conectividad mínima (árbol generador)
    available = list(nodes)
    connected = [available.pop()]
    while available:
        a = random.choice(connected)
        b = available.pop(random.randint(0, len(available) - 1))
        weight = random.randint(1, 20)
        graph.insert_edge(a, b, weight)
        connected.append(b)

    # Aristas adicionales aleatorias
    edges_added = n_nodes - 1
    while edges_added < m_edges:
        u, v = random.sample(nodes, 2)
        if not graph.has_edge(u, v):
            weight = random.randint(1, 20)
            graph.insert_edge(u, v, weight)
            edges_added += 1

    # Asignar roles
    random.shuffle(nodes)
    n_storage = int(n_nodes * 0.2)
    n_recharge = int(n_nodes * 0.2)

    for i, v in enumerate(nodes):
        if i < n_storage:
            v.role = "storage"
        elif i < n_storage + n_recharge:
            v.role = "recharge"
        else:
            v.role = "client"

    return graph, nodes
