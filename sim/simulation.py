#############################################################
#A ESTE LE DALTA UN CUESTION
#############################################################

from domain.order import Order
from domain.route import Route
import random

MAX_BATTERY = 50

def simulate_orders(graph, nodes, n_orders, avl_root=None, clients_dict=None):
    storage_nodes = [v for v, d in nodes.items() if d["role"] == "📦"]
    client_nodes = [v for v, d in nodes.items() if d["role"] == "👤"]
    recharge_nodes = [v for v, d in nodes.items() if d["role"] == "🔋"]

    orders = []

    for _ in range(n_orders):
        origin = random.choice(storage_nodes)
        destination = random.choice(client_nodes)

        # Buscar ruta válida (batería limitada)
        path, cost = find_valid_path(graph, origin, destination, recharge_nodes)

        if path:
            # Crear orden y ruta
            route = Route(path, cost, recharge_points=[n for n in path if n in recharge_nodes])
            order = Order(origin, destination, path, cost)
            orders.append(order)

            # Guardar en cliente
            if clients_dict is not None:
                clients_dict[destination].add_order(order)

            # Insertar ruta al AVL
            if avl_root is not None:
                from tda.avl import stat_insert
                route_key = " → ".join(str(n) for n in path)
                avl_root = stat_insert(avl_root, route_key)

    return orders, avl_root

def find_valid_path(graph, start, end, recharge_nodes):
    from collections import deque

    queue = deque([(start, [start], 0)])
    visited = set()

    while queue:
        current, path, cost = queue.popleft()
        if cost > MAX_BATTERY:
            continue
        if current == end:
            return path, cost
        visited.add(current)
        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                edge = graph.get_edge(current, neighbor)
                next_cost = cost + edge.element()
                queue.append((neighbor, path + [neighbor], next_cost))

    return None, None  # No ruta válida sin recarga

# Mejorable luego para forzar recarga si no hay ruta directa