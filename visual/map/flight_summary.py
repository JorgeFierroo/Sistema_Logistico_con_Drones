from collections import deque

def bfs_autonomy(graph, roles, start, goal, max_battery=50):
    queue = deque([(start, [start], 0, [], max_battery)])
    visited = set()
    while queue:
        cur, path, used, recs, rem = queue.popleft()
        if (cur, rem) in visited: 
            continue
        visited.add((cur, rem))
        if cur == goal:
            dist = used
            return {"path": path, "dist": dist,
                    "battery_used": used, "recharges": recs}
        for e in graph.incident_edges(cur):
            nxt = e.opposite(cur); cost = e.element()
            if nxt in path or rem - cost < 0: 
                continue
            nrem, nrecs = rem - cost, list(recs)
            if roles[nxt] == "recharge":
                nrem = max_battery
                nrecs.append(nxt)
            queue.append((nxt, path + [nxt], used + cost, nrecs, nrem))
    return None

def flight_summary(simulation, origin_v, dest_v):
    info = bfs_autonomy(simulation.graph, simulation.node_roles,
                        origin_v, dest_v, 50)
    if not info:
        return None
    # crear orden y marcar entregada
    from domain.order import Order
    order = Order(origin_v, dest_v,
                  route=info["path"],
                  cost=info["dist"],
                  priority=1,
                  battery_used=info["battery_used"],
                  recharges=info["recharges"],
                  full_path=info["path"])
    order.entregar()
    simulation.orders.append(order)
    return info, order
