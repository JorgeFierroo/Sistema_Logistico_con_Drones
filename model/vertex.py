class Vertice:
    """Estructura ligera de un vértice para un grafo."""
    __slots__ = '_elemento'

    def __init__(self, elemento):
        """No llames directamente al constructor. Usa insertar_vertice(elemento) del Grafo."""
        self._elemento = elemento

    def elemento(self):
        """Devuelve el elemento asociado a este vértice."""
        return self._elemento

    def __hash__(self):
        return hash(id(self))

    def __str__(self):
        return str(self._elemento)

    def __repr__(self):
        return f"Vertice({self._elemento})"
