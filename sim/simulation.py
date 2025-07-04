import random, heapq, sys, os
from collections import defaultdict, deque

current_dir  = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.extend([project_root,
    os.path.join(project_root, 'domain'),
    os.path.join(project_root, 'model'),
    os.path.join(project_root, 'tda')
])

from domain.client import Client
from domain.order  import Order
from domain.route  import Route          # <-- ahora se usa
from model.graph   import Graph
from tda.avl       import insert as avl_insert, Node as AVLNode
from tda.hasp_map  import HashMap

class Simulation:
    def __init__(self):
        self.graph        = Graph(directed=False)
        self.clients      = []
        self.orders       = []
        self.routes       = []          # objetos Route (historial)
        self.node_roles   = {}          # Vertex -> role
        self.route_avl    = None        # AVL para rutas
        self.route_counts = HashMap()   # HashMap ruta_str -> freq

    # ---------- inicialización ----------
    def initialize(self, n_nodes, n_edges, n_orders):
        self.__init__()                        # limpia estado
        self._create_nodes(n_nodes)
        self._create_edges(n_edges)
        self._assign_roles()
        self._generate_orders(n_orders)

    # ---------- grafo ----------
    def _create_nodes(self, n):
        for i in range(n):
            label = chr(65+i) if i < 26 else f"N{i}"
            v = self.graph.insert_vertex(label)
            self.node_roles[v] = None

    def _create_edges(self, m):
        verts=list(self.graph.vertices()); random.shuffle(verts)
        for i in range(len(verts)-1):               # spanning‑tree
            self.graph.insert_edge(verts[i], verts[i+1],
                                   random.randint(1,20))
        while len(list(self.graph.edges())) < m:    # aristas extra
            u,v=random.sample(verts,2)
            if self.graph.get_edge(u,v) is None:
                self.graph.insert_edge(u,v,random.randint(1,20))

    def _assign_roles(self):
        verts=list(self.graph.vertices()); random.shuffle(verts)
        ns,nr=int(len(verts)*.2), int(len(verts)*.2)
        for i,v in enumerate(verts):
            if i < ns:
                self.node_roles[v] = "storage"
            elif i < ns + nr:
                self.node_roles[v] = "recharge"
            else:
                self.node_roles[v] = "client"
                client = Client()
                client.vertex = v             # <-- Asociación importante
                self.clients.append(client)

    # ---------- BFS con autonomía ----------
    def find_route_with_recharges_bfs(self, start, goal, battery_max=50):
        q=deque([(start,[start],0,[],battery_max)]); visited=set()
        while q:
            cur,path,used,rechs,rem=q.popleft()
            if (cur,rem) in visited: continue
            visited.add((cur,rem))
            if cur==goal: return path,used,rechs
            for e in self.graph.incident_edges(cur):
                nxt=e.opposite(cur); cost=e.element()
                if nxt in path or rem-cost<0: continue
                nrem, nrechs = rem-cost, list(rechs)
                if self.node_roles[nxt]=="recharge":
                    nrem=battery_max; nrechs.append(nxt)
                q.append((nxt, path+[nxt], used+cost, nrechs, nrem))
        return None,None,None

    # ---------- Dijkstra ----------
    def dijkstra_shortest_path(self, start, goal):
        dist={start:0}; prev={}; pq=[(0,start)]
        while pq:
            d,u=heapq.heappop(pq)
            if u==goal: break
            if d>dist[u]: continue
            for e in self.graph.incident_edges(u):
                v=e.opposite(u); w=d+e.element()
                if v not in dist or w<dist[v]:
                    dist[v]=w; prev[v]=u; heapq.heappush(pq,(w,v))
        if goal not in dist: return None,None
        path=[]; cur=goal
        while cur!=start: path.append(cur); cur=prev[cur]
        path.append(start); path.reverse()
        return path, dist[goal]

    # ---------- Floyd‑Warshall opcional ----------
    def floyd_warshall_all_pairs(self):
        verts=list(self.graph.vertices())
        idx={v:i for i,v in enumerate(verts)}; n=len(verts); INF=10**9
        dist=[[INF]*n for _ in range(n)]
        for v in verts:
            i=idx[v]; dist[i][i]=0
            for e in self.graph.incident_edges(v):
                j=idx[e.opposite(v)]
                dist[i][j]=min(dist[i][j], e.element())
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][j]>dist[i][k]+dist[k][j]:
                        dist[i][j]=dist[i][k]+dist[k][j]
        return verts, dist

    # ---------- generación de órdenes ----------
    def _generate_orders(self, cnt):
        stor=[v for v,r in self.node_roles.items() if r=="storage"]
        cli =[v for v,r in self.node_roles.items() if r=="client"]
        for _ in range(cnt):
            if not stor or not cli: break
            o,d=random.choice(stor),random.choice(cli)
            path,used,rechs=self.find_route_with_recharges_bfs(o,d)
            if not path: continue
            cost=sum(self.graph.get_edge(path[i],path[i+1]).element()
                     for i in range(len(path)-1))
            order=Order(o,d,path,cost,random.randint(1,3),used,rechs,path)
            self.orders.append(order)

            # ----- registrar ruta -----
            route_obj = Route([v.element() for v in path], cost)
            self.routes.append(route_obj)

            if self.route_avl is None:
                self.route_avl = AVLNode(str(route_obj))
            else:
                self.route_avl = avl_insert(self.route_avl, str(route_obj))

            rstr=str(route_obj)
            self.route_counts.set(rstr,
                                  self.route_counts.get(rstr,0)+1)

    # ---------- estadísticas ----------
    def get_route_counts(self):
        return {k: self.route_counts.get(k) for k in self.route_counts.keys()}

    def get_origin_destination_frequencies(self):
        origins, dests = defaultdict(int), defaultdict(int)
        for o in self.orders:
            origins[str(o.origin)]      += 1
            dests[str(o.destination)]   += 1
        return {"origins": dict(origins), "destinations": dict(dests)}

    def get_visits_by_role(self):
        """
        Devuelve cuántas veces aparece cada vértice en las rutas,
        agrupado por rol (client / recharge / storage).
        """
        # 1) contar visitas por etiqueta
        node_visits = defaultdict(int)
        for route in self.routes:
            for label in route.path:
                node_visits[label] += 1

        # 2) agrupar por rol
        result = {"client": {}, "recharge": {}, "storage": {}}
        for v, role in self.node_roles.items():
            label = v.element()
            if role in result:
                result[role][label] = node_visits.get(label, 0)
        return result

    # ---------- getters ----------
    def get_graph(self):      return self.graph
    def get_orders(self):     return self.orders
    def get_routes(self):     return self.routes
    def get_route_avl(self):  return self.route_avl
    def get_mst_edges(self):  return self.graph.kruskal_mst()
    def get_clients(self):    return self.clients
    def get_node_roles(self): return self.node_roles