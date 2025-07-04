from collections import deque
import sys, os

current_dir  = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.extend([project_root,
    os.path.join(project_root, 'domain'),
    os.path.join(project_root, 'tda')
])
# ---------------------------  BFS con autonomía  --------------------------- #
def bfs_autonomy(graph, roles, start, goal, max_battery: int = 50):
    """
    BFS modificado que respeta un límite de batería y permite recargas.
    Devuelve dict con path, distancia, batería usada y nodos de recarga,
    o None si no existe ruta viable.
    """
    queue   = deque([(start, [start], 0, [], max_battery)])
    visited = set()

    while queue:
        cur, path, used, recs, rem = queue.popleft()

        if (cur, rem) in visited:
            continue
        visited.add((cur, rem))

        if cur == goal:
            return {
                "path":         path,
                "dist":         used,
                "battery_used": used,
                "recharges":    recs
            }

        for e in graph.incident_edges(cur):
            nxt  = e.opposite(cur)
            cost = e.element()

            if cost is None or nxt in path or rem - cost < 0:
                continue

            nrem  = rem - cost
            nrecs = list(recs)
            if roles.get(nxt) == "recharge":
                nrem  = max_battery
                nrecs.append(nxt)

            queue.append((nxt, path + [nxt], used + cost, nrecs, nrem))

    return None


# --------------------------  Resumen de vuelo  ----------------------------- #
def flight_summary(simulation, origin_v, dest_v):
    """
    Calcula la ruta (BFS con recargas).  
    Si es viable, crea Order, la vincula al cliente y registra la ruta
    en todas las estructuras de la simulación.
    Retorna (info_dict, order) o None si no hay ruta.
    """
    info = bfs_autonomy(
        simulation.graph,
        simulation.node_roles,
        origin_v,
        dest_v,
        max_battery=50
    )
    if not info:
        return None

    # ---------- Crear Order ----------
    from domain.order import Order
    from domain.route import Route
    from tda.avl import insert as avl_insert, Node as AVLNode

    order = Order(
        origin       = origin_v,
        destination  = dest_v,
        route        = info["path"],
        cost         = info["dist"],
        priority     = 1,
        battery_used = info["battery_used"],
        recharges    = info["recharges"],
        full_path    = info["path"]
    )

    # ---------- Asociar cliente ----------
    for client in simulation.clients:
        if getattr(client, "vertex", None) == dest_v:
            order.cliente     = client
            order.id_cliente  = client.client_id
            client.add_order(order)
            break

    order.entregar()
    simulation.orders.append(order)

    # ---------- Registrar ruta ----------
    route_obj = Route([v.element() for v in info["path"]], info["dist"])
    simulation.routes.append(route_obj)

    # AVL de rutas
    if simulation.route_avl is None:
        simulation.route_avl = AVLNode(str(route_obj))
    else:
        simulation.route_avl = avl_insert(simulation.route_avl, str(route_obj))

    # Frecuencia de rutas
    rstr = str(route_obj)
    prev = simulation.route_counts.get(rstr, 0)
    simulation.route_counts.set(rstr, prev + 1)

    return info, order
