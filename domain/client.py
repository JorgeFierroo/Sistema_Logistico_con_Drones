import random

class Cliente:
    _contador = 0  # Variable de clase para contar instancias

    def __init__(self, total_pedidos=0):
        Cliente._contador += 1
        self.client_id = f"C{Cliente._contador:03d}"  # Formato C001, C002...
        self.nombre = f"Cliente{Cliente._contador}"
        self.total_pedidos = total_pedidos

    def __str__(self):
        return f"{self.client_id} - {self.nombre} - Pedidos: {self.total_pedidos}"
    
def crear_clientes(n):
    clientes = []
    for i in range(n):
        r = random.randint(0, 2)
        cliente = Cliente()
        clientes.append(cliente)
    return clientes


clientes =crear_clientes(10)
print([str(cliente) for cliente in clientes])
