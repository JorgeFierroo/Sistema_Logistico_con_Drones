import folium
import random

class MapBuilder:
    def __init__(self, graph, node_roles):
        self.graph = graph
        self.node_roles = node_roles
        self.coordinates = {}

    def generate_coordinates(self, center=(-38.7359, -72.5904), spread=0.02):
        """
        Asigna coordenadas aleatorias a cada nodo en torno a un punto central (Temuco).
        """
        for v in self.graph.vertices():
            lat = center[0] + random.uniform(-spread, spread)
            lon = center[1] + random.uniform(-spread, spread)
            self.coordinates[v] = (lat, lon)

    def build_map(self):
        """
        Construye y retorna un mapa folium con los nodos y aristas del grafo.
        """
        if not self.coordinates:
            self.generate_coordinates()

        fmap = folium.Map(location=[-38.7359, -72.5904], zoom_start=13)

        # Agrega nodos
        for v in self.graph.vertices():
            lat, lon = self.coordinates[v]
            role = self.node_roles.get(v, "unknown")
            color = {
                "client": "blue",
                "storage": "green",
                "recharge": "orange"
            }.get(role, "gray")

            folium.CircleMarker(
                location=(lat, lon),
                radius=6,
                popup=f"{v.element()} ({role})",
                color=color,
                fill=True,
                fill_opacity=0.8
            ).add_to(fmap)

        # Agrega aristas
        for edge in self.graph.edges():
            u, v = edge.endpoints()
            lat1, lon1 = self.coordinates[u]
            lat2, lon2 = self.coordinates[v]
            folium.PolyLine(
                locations=[(lat1, lon1), (lat2, lon2)],
                color="gray",
                weight=2
            ).add_to(fmap)

        return fmap
