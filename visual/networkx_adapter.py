import networkx as nx
import matplotlib.pyplot as plt

def graph_to_networkx(custom_graph):
    """
    Convierte un grafo personalizado (estructura Graph) en un grafo de NetworkX para visualización.

    :param custom_graph: Instancia de la clase Graph personalizada.
    :return: Grafo de NetworkX con nodos y aristas.
    """
    G = nx.Graph()

    for v in custom_graph.vertices():
        role = getattr(v, 'role', 'unknown')  # Asegúrate de que Vertex tenga atributo 'role'
        G.add_node(str(v), role=role)

    for edge in custom_graph.edges():
        u, v = edge.endpoints()
        G.add_edge(str(u), str(v), weight=edge.element())

    return G

def draw_networkx_graph(G, path_nodes=None):
    """
    Dibuja el grafo de NetworkX, coloreando los nodos según su rol y resaltando una ruta opcional.

    :param G: Grafo de NetworkX.
    :param path_nodes: Lista de nombres de nodos que conforman una ruta a resaltar (opcional).
    :return: Figura de Matplotlib.
    """
    pos = nx.spring_layout(G, seed=42)

    # Colores de nodos por rol
    node_colors = []
    for node in G.nodes(data=True):
        role = node[1].get('role')
        if role == "client":
            node_colors.append("#1f77b4")  # Azul
        elif role == "storage":
            node_colors.append("#2ca02c")  # Verde
        elif role == "recharge":
            node_colors.append("#ff7f0e")  # Naranjo
        else:
            node_colors.append("gray")  # Desconocido

    # Estilos de aristas
    edge_colors = []
    for u, v in G.edges():
        if path_nodes and u in path_nodes and v in path_nodes:
            edge_colors.append("red")
        else:
            edge_colors.append("gray")

    fig, ax = plt.subplots(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, node_color=node_colors,
            edge_color=edge_colors, node_size=500, font_size=9, ax=ax)
    return fig
