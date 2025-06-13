import sys
import os
import streamlit as st

ruta_sim = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sim'))
ruta_orden = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sim'))

sys.path.extend([ruta_sim, ruta_orden])

from init_simulation import run_simulation, get_current_simulation
from order import Order
from networkx_adapter import graph_to_networkx, draw_networkx_graph

st.set_page_config(page_title="Drone Logistics Simulator", layout="wide")
st.markdown("# 🚁 Drone Logistics Simulator - Correos Chile")

# Leyenda de proporciones
st.markdown("""
**Node Role Proportions:**
- 📦 Storage Nodes: 20%
- 🔋 Recharge Nodes: 20%
- 👤 Client Nodes: 60%
""")

# Pestañas
tabs = st.tabs([
    "🔄 Run Simulation",
    "🔎 Explore Network",
    "🌐 Clients & Orders",
    "📋 Route Analytics",
    "📈 Statistics"
])

# Pestaña 1: Run Simulation
with tabs[0]:
    st.markdown("# ⚙️ Initialize Simulation")
    num_nodes = st.slider("Number of Nodes", min_value=10, max_value=150, value=15)
    num_edges = st.slider("Number of Edges", min_value=10, max_value=300, value=20)
    num_orders = st.slider("Number of Orders", min_value=1, max_value=500, value=10)

    num_clients = int(num_nodes * 0.6)
    st.markdown(f"**Derived Client Nodes:** {num_clients} (60% of {num_nodes})")

    if st.button("🚀 Start Simulation"):
        simulation = run_simulation(num_nodes, num_edges, num_orders)
        st.session_state.simulation = simulation
        st.success("Simulation initialized successfully!")

# Pestaña 2: Explore Network
with tabs[1]:
    st.markdown("# 🌍 Network Visualization")

    if not st.session_state.get("boton_presionado", False):
        st.warning("⚠️ Initialize a simulation first.")
    else:
        sim = st.session_state["simulation"]
        graph = sim.get_graph()
        roles = sim.get_node_roles()

        # Visualización en red
        st.subheader("🧠 Grafo de red actual")

        fig = draw_networkx_graph(graph, roles)
        st.pyplot(fig)

        st.subheader("📌 Calculate Route")
        vertices = list(graph.vertices())

        if len(vertices) < 2:
            st.info("Not enough vertices to compute routes.")
        else:
            origin = st.selectbox("Select origin", vertices, format_func=str)
            destination = st.selectbox("Select destination", vertices, format_func=str)

            if st.button("✈️ Calculate Route"):
                # Simple BFS
                from collections import deque

                def bfs_path(g, start, goal):
                    visited = set()
                    queue = deque([(start, [start])])

                    while queue:
                        current, path = queue.popleft()
                        if current == goal:
                            return path
                        visited.add(current)
                        for neighbor in g.neighbors(current):
                            if neighbor not in visited:
                                queue.append((neighbor, path + [neighbor]))
                    return []

                path = bfs_path(graph, origin, destination)

                if path:
                    sim.add_route(path)
                    sim.orders.append(Order(origin, destination))
                    st.success(f"Route found: {' → '.join(str(v) for v in path)}")
                else:
                    st.error("No route found between selected nodes.")


# Pestaña 3: Clients & Orders
with tabs[2]:
    st.markdown("# 🌐 Clients and Orders")

    if "simulation" not in st.session_state:
        st.warning("⚠️ Initialize a simulation first.")
    else:
        sim = st.session_state.simulation
        orders = sim.get_orders()

        st.markdown("### 📦 Active Orders")
        for order in orders:
            st.write(f"From {order.origin.element()} to {order.destination.element()}")

# Pestaña 4: Route Analytics
with tabs[3]:
    st.markdown("# 📋 Route Frequency & History")
    st.warning("⚠️ Functionality not implemented yet.")

# Pestaña 5: Statistics
with tabs[4]:
    st.markdown("# 📈 General Statistics")
    st.warning("⚠️ Functionality not implemented yet.")
