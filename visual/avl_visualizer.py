import matplotlib.pyplot as plt
import networkx as nx


def draw_avl_tree(root):
    """
    Dibuja un árbol AVL usando NetworkX y matplotlib.
    Recibe la raíz del árbol y retorna una figura de matplotlib.
    """
    if root is None:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No routes registered", ha='center', va='center', fontsize=12)
        ax.axis('off')
        return fig

    G = nx.DiGraph()

    def add_edges(node):
        if node:
            G.add_node(str(node.key))
            if node.left:
                G.add_edge(str(node.key), str(node.left.key))
                add_edges(node.left)
            if node.right:
                G.add_edge(str(node.key), str(node.right.key))
                add_edges(node.right)

    add_edges(root)

    pos = nx.spring_layout(G, seed=42)  # Usar spring_layout para AVL pequeño-mediano
    fig, ax = plt.subplots(figsize=(6, 5))
    nx.draw(G, pos, with_labels=True, node_color="lightgreen", edge_color="gray", node_size=800, font_size=10, ax=ax)
    ax.set_title("AVL Route Tracker", fontsize=14)
    ax.set_axis_off()

    return fig
