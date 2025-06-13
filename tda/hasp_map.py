class HashMap:
    def __init__(self, size=100):
        self.size = size
        self.map = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def set(self, key, value):
        index = self._hash(key)
        for pair in self.map[index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.map[index].append([key, value])

    def get(self, key, default=None):  # <-- CAMBIO AQUÍ
        index = self._hash(key)
        for pair in self.map[index]:
            if pair[0] == key:
                return pair[1]
        return default  # <-- DEVUELVE el valor por defecto si no lo encuentra

    def remove(self, key):
        index = self._hash(key)
        for i, pair in enumerate(self.map[index]):
            if pair[0] == key:
                del self.map[index][i]
                return True
        return False

    def keys(self):
        return [pair[0] for bucket in self.map for pair in bucket]

    def values(self):
        return [pair[1] for bucket in self.map for pair in bucket]

    def items(self):
        return [(pair[0], pair[1]) for bucket in self.map for pair in bucket]
