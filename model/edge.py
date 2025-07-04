class Arista:
    """Estructura liviana de una arista para un grafo."""
    __slots__ = '_origen', '_destino', '_elemento'

    def __init__(self, u, v, x):
        """No llamar directamente al constructor. Usar insertar_arista(u, v, x) del Grafo."""
        self._origen = u
        self._destino = v
        self._elemento = x

    def extremos(self):
        """Devuelve una tupla (u, v) con los vértices origen y destino."""
        return (self._origen, self._destino)

    def opuesto(self, v):
        """Devuelve el vértice opuesto a v en esta arista."""
        return self._destino if v is self._origen else self._origen

    def elemento(self):
        """Devuelve el elemento asociado a esta arista."""
        return self._elemento

    def __hash__(self):
        """Permite que la arista sea usada como clave en un diccionario o conjunto."""
        return hash((self._origen, self._destino))

    def __str__(self):
        """Representación en cadena de la arista."""
        return f"({self._origen}->{self._destino}):{self._elemento}"

    def __repr__(self):
        """Representación oficial de la arista."""
        return f"Arista({self._origen}, {self._destino}, {self._elemento})"
