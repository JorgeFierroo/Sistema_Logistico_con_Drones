from vertex import Vertex
from edge import Edge

class Grafo:
    def __init__(self, dirigido=False):
        self._adyacentes_salida = {}
        self._adyacentes_entrada = {} if dirigido else self._adyacentes_salida
        self._dirigido = dirigido

    def es_dirigido(self):
        return self._dirigido

    def insertar_vertice(self, elemento):
        v = Vertex(elemento)
        self._adyacentes_salida[v] = {}
        if self._dirigido:
            self._adyacentes_entrada[v] = {}
        return v

    def insertar_arista(self, u, v, elemento):
        e = Edge(u, v, elemento)
        self._adyacentes_salida[u][v] = e
        self._adyacentes_entrada[v][u] = e
        return e

    def eliminar_arista(self, u, v):
        if u in self._adyacentes_salida and v in self._adyacentes_salida[u]:
            del self._adyacentes_salida[u][v]
            del self._adyacentes_entrada[v][u]

    def eliminar_vertice(self, v):
        for u in list(self._adyacentes_salida.get(v, {})):
            self.eliminar_arista(v, u)
        for u in list(self._adyacentes_entrada.get(v, {})):
            self.eliminar_arista(u, v)
        self._adyacentes_salida.pop(v, None)
        if self._dirigido:
            self._adyacentes_entrada.pop(v, None)

    def obtener_arista(self, u, v):
        return self._adyacentes_salida.get(u, {}).get(v)

    def vertices(self):
        return self._adyacentes_salida.keys()

    def aristas(self):
        vistas = set()
        for mapa in self._adyacentes_salida.values():
            vistas.update(mapa.values())
        return vistas

    def vecinos(self, v):
        return self._adyacentes_salida[v].keys()

    def grado(self, v, salida=True):
        ady = self._adyacentes_salida if salida else self._adyacentes_entrada
        return len(ady[v])

    def aristas_incidentes(self, v, salida=True):
        ady = self._adyacentes_salida if salida else self._adyacentes_entrada
        return ady[v].values()
