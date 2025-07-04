import folium

ROLE_COLOR = {"client": "blue", "storage": "green", "recharge": "orange"}

class MapBuilder:
    def __init__(self, graph, node_roles, coordinates):
        self.g   = graph
        self.roles = node_roles
        self.coords = coordinates
        self.m = folium.Map(location=[-38.7359, -72.59], zoom_start=13)

    # ---------- nodos + aristas ----------
    def add_base_graph(self):
        # nodos
        for v in self.g.vertices():
            lat, lon = self.coords[v]
            folium.CircleMarker(
                location=(lat, lon),
                radius=6,
                color=ROLE_COLOR.get(self.roles[v], "gray"),
                fill=True,
                popup=f"{v.element()} ({self.roles[v]})"
            ).add_to(self.m)
        # aristas
        for e in self.g.edges():
            u, v = e.endpoints()
            folium.PolyLine(
                [self.coords[u], self.coords[v]],
                weight=1, color="blue", opacity=0.8
            ).add_to(self.m)

    # ---------- dibujar MST ----------
    def add_mst(self, mst_edges):
        for e in mst_edges:
            u, v = e.endpoints()
            folium.PolyLine(
                [self.coords[u], self.coords[v]],
                weight=4, color="green", opacity=0.8, dashArray="10,10"
                 
            ).add_to(self.m)
        

    # ---------- dibujar ruta especÃ­fica ----------
    def add_route(self, path, color="red", popup_text=None, dashed=False):
        points = [self.coords[v] for v in path]
        style = {
            "color": color,
            "weight": 5
        }
    
        polyline = folium.PolyLine(points, **style)

        if popup_text:
            polyline.add_child(folium.Popup(popup_text))

        polyline.add_to(self.m)



    def finish(self):
        return self.m