import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def graph_to_networkx(custom_graph, orders=None):
    """
    Convierte un grafo personalizado en un grafo de NetworkX, incluyendo roles y prioridades.

    :param custom_graph: Instancia de la clase Graph personalizada.
    :param orders: Lista de órdenes para anotar prioridad en los nodos destino.
    :return: Grafo de NetworkX.
    """
    G = nx.Graph()
    priority_map = {}

    # Construir mapa de prioridades por nodo destino
    if orders:
        for order in orders:
            dest = str(order.destination)
            priority_map[dest] = order.priority

    for v in custom_graph.vertices():
        role = getattr(v, 'role', 'unknown')  # Asegura que Vertex tenga atributo 'role'
        label = str(v)
        G.add_node(label, role=role, priority=priority_map.get(label, None))

    for edge in custom_graph.edges():
        u, v = edge.endpoints()
        G.add_edge(str(u), str(v), weight=edge.element())

    return G


def draw_networkx_graph(G, path_nodes=None):
    """
    Dibuja el grafo con colores por rol y prioridades. Resalta rutas si se especifican.

    :param G: Grafo de NetworkX.
    :param path_nodes: Lista de nodos que forman una ruta.
    :return: Figura de Matplotlib.
    """
    pos = nx.spring_layout(G, seed=42)

    node_colors = []
    edge_colors = []

    for node, data in G.nodes(data=True):
        role = data.get("role")
        priority = data.get("priority")

        if priority == 2:
            node_colors.append("red")
        elif priority == 1:
            node_colors.append("orange")
        elif priority == 0:
            node_colors.append("white")
        else:
            # Color por rol si no tiene prioridad explícita
            if role == "client":
                node_colors.append("#1f77b4")
            elif role == "storage":
                node_colors.append("#2ca02c")
            elif role == "recharge":
                node_colors.append("#ff7f0e")
            else:
                node_colors.append("gray")

    for u, v in G.edges():
        if path_nodes and u in path_nodes and v in path_nodes:
            edge_colors.append("red")
        else:
            edge_colors.append("gray")

    fig, ax = plt.subplots(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, node_color=node_colors,
            edge_color=edge_colors, node_size=500, font_size=9, ax=ax)

    # Leyenda
    legend_elements = [
        mpatches.Patch(color="#2ca02c", label="📦 Storage"),
        mpatches.Patch(color="#ff7f0e", label="🔋 Recharge"),
        mpatches.Patch(color="#1f77b4", label="👤 Client"),
        mpatches.Patch(color="white", edgecolor="black", label="Prioridad 0"),
        mpatches.Patch(color="orange", label="Prioridad 1"),
        mpatches.Patch(color="red", label="Prioridad 2")
    ]
    ax.legend(handles=legend_elements, loc="lower left", fontsize="small")
    ax.set_title("Red de entrega con prioridad")
    plt.axis("off")

    return fig

def draw_mst_graph(G, mst_edges):

    pos = nx.spring_layout(G, seed=42)

    node_colors = []
    for node, data in G.nodes(data=True):
        role = data.get("role")
        if role == "client":
            node_colors.append("#1f77b4")
        elif role == "storage":
            node_colors.append("#2ca02c")
        elif role == "recharge":
            node_colors.append("#ff7f0e")
        else:
            node_colors.append("gray")

    edge_colors = []
    edge_widths = []
    for u, v in G.edges():
        if (u, v) in mst_edges or (v, u) in mst_edges:
            edge_colors.append("blue")
            edge_widths.append(2.5)
        else:
            edge_colors.append("gray")
            edge_widths.append(0.8)

    fig, ax = plt.subplots(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, node_color=node_colors,
            edge_color=edge_colors, width=edge_widths,
            node_size=500, font_size=9, ax=ax)

    ax.set_title("Árbol de Expansión Mínima (MST)")
    plt.axis("off")

    return fig
