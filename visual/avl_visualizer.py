class HashMap:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]

    def _hash(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):
        idx = self._hash(key)
        # Verificar si ya existe y actualizar
        for i, (k, _) in enumerate(self.table[idx]):
            if k == key:
                self.table[idx][i] = (key, value)
                return
        self.table[idx].append((key, value))

    def get(self, key):
        idx = self._hash(key)
        for k, v in self.table[idx]:
            if k == key:
                return v
        return None

    def remove(self, key):
        idx = self._hash(key)
        self.table[idx] = [(k, v) for (k, v) in self.table[idx] if k != key]

    def contains(self, key):
        idx = self._hash(key)
        return any(k == key for (k, _) in self.table[idx])

    def keys(self):
        for bucket in self.table:
            for k, _ in bucket:
                yield k

    def values(self):
        for bucket in self.table:
            for _, v in bucket:
                yield v

    def items(self):
        for bucket in self.table:
            for item in bucket:
                yield item