class MapHash:
    def __init__(self, capacidad=100):
        self.capacidad = capacidad
        self.tabla = [[] for _ in range(capacidad)]

    def _hash(self, clave):
        return hash(clave) % self.capacidad

    def insertar(self, clave, valor):
        indice = self._hash(clave)
        # Verificar si ya existe y actualizar
        for i, (k, _) in enumerate(self.tabla[indice]):
            if k == clave:
                self.tabla[indice][i] = (clave, valor)
                return
        self.tabla[indice].append((clave, valor))

    def obtener(self, clave):
        indice = self._hash(clave)
        for k, v in self.tabla[indice]:
            if k == clave:
                return v
        return None

    def eliminar(self, clave):
        indice = self._hash(clave)
        self.tabla[indice] = [(k, v) for (k, v) in self.tabla[indice] if k != clave]

    def contiene(self, clave):
        indice = self._hash(clave)
        return any(k == clave for (k, _) in self.tabla[indice])

    def claves(self):
        for cubeta in self.tabla:
            for k, _ in cubeta:
                yield k

    def valores(self):
        for cubeta in self.tabla:
            for _, v in cubeta:
                yield v

    def elementos(self):
        for cubeta in self.tabla:
            for elemento in cubeta:
                yield elemento
