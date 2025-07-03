from collections import deque

def bfs_con_autonomia(graph, roles, origin, destination, autonomy_max):
    """
    Realiza una búsqueda BFS considerando la autonomía y estaciones de recarga.

    :param graph: instancia de Graph
    :param roles: dict con roles de nodos (vertex -> role)
    :param origin: vértice de inicio
    :param destination: vértice de destino
    :param autonomy_max: autonomía máxima del dron
    :return: (ruta, batería_usada, estaciones_recharge, distancia_total)
    """
    queue = deque()
    visited = set()

    queue.append((origin, [origin], autonomy_max, [], 0))  # nodo, ruta, batería, recargas, distancia acumulada

    while queue:
        current, path, battery, recharges, dist = queue.popleft()

        if (current, battery) in visited:
            continue
        visited.add((current, battery))

        if current == destination:
            return path, autonomy_max - battery, recharges, dist

        for edge in graph.incident_edges(current):
            neighbor = edge.opposite(current)
            if neighbor in path:
                continue

            cost = edge.element()
            new_battery = battery - cost
            new_recharges = list(recharges)
            new_dist = dist + cost

            if new_battery < 0:
                continue

            if roles.get(neighbor) == "recharge":
                new_battery = autonomy_max
                new_recharges.append(neighbor)

            queue.append((neighbor, path + [neighbor], new_battery, new_recharges, new_dist))

    return None, None, None, None


def generar_resumen_de_entrega(origin, destination, graph, roles, autonomy):
    """
    Calcula y resume la ruta entre dos nodos considerando batería y recargas.

    :param origin: vértice de inicio
    :param destination: vértice de fin
    :param graph: instancia de Graph
    :param roles: dict de roles por vértice
    :param autonomy: batería máxima
    :return: dict resumen
    """
    ruta, bateria_usada, recargas, distancia = bfs_con_autonomia(graph, roles, origin, destination, autonomy)

    if ruta is None:
        return {
            "viable": False,
            "motivo": "No se encontró ruta con autonomía suficiente",
            "ruta": [],
            "distancia": 0,
            "bateria_usada": 0,
            "recargas": []
        }

    return {
        "viable": True,
        "ruta": [v.element() for v in ruta],
        "distancia": distancia,
        "bateria_usada": bateria_usada,
        "recargas": [v.element() for v in recargas],
        "nodos_visitados": len(ruta)
    }
