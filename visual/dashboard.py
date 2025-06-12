import streamlit as st
from sim.simulation import Simulation
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

# Tabs
tabs = st.tabs(["🔄 Run Simulation", "🔎 Explore Network", "🌐 Clients & Orders", "📋 Route Analytics", "📈 Statistics"])

# Create simulation instance
if "simulation" not in st.session_state:
    st.session_state.simulation = None

# Tab 1: Run Simulation
with tabs[0]:
    st.markdown("# ⚙️ Initialize Simulation")
    num_nodes = st.slider("Number of Nodes", min_value=10, max_value=150, value=15)
    num_edges = st.slider("Number of Edges", min_value=10, max_value=300, value=20)
    num_orders = st.slider("Number of Orders", min_value=1, max_value=500, value=10)

    num_clients = int(num_nodes * 0.6)
    st.markdown(f"**Derived Client Nodes:** {num_clients} (60% of {num_nodes})")

    if st.button("🚀 Start Simulation"):
        st.session_state.simulation = Simulation(num_nodes, num_edges, num_orders)
        st.success("Simulation initialized successfully!")

# Tab 2: Explore Network
with tabs[1]:
    st.markdown("# 🌍 Network Visualization")

    sim = st.session_state.get("simulation")
    if not sim:
        st.warning("⚠️ Initialize a simulation first.")
    else:
        left_col, right_col = st.columns(2)

        with left_col:
            G_nx = graph_to_networkx(sim.graph)
            fig = draw_networkx_graph(G_nx)
            st.pyplot(fig)

        with right_col:
            st.subheader("📌 Calculate Route")
            node_ids = [str(v.element()) for v in sim.graph.vertices()]
            origin = st.selectbox("Select origin", node_ids)
            destination = st.selectbox("Select destination", node_ids)

            if st.button("✈️ Calculate Route"):
                path, cost = sim.calculate_route(origin, destination)
                if path:
                    st.success(f"Path: {' → '.join(path)} | Cost: {cost}")
                    st.session_state["last_path"] = path
                else:
                    st.error("No route available within battery limit.")

            if st.button("✅ Complete Delivery and Create Order"):
                if "last_path" in st.session_state:
                    sim.complete_order(st.session_state["last_path"])
                    st.success("Order completed and recorded.")
                else:
                    st.warning("Calculate a route first.")

# Tab 3: Clients and Orders
with tabs[2]:
    st.markdown("# 🌐 Clients and Orders")
    sim = st.session_state.get("simulation")
    if not sim:
        st.warning("⚠️ Initialize a simulation first.")
    else:
        st.write("(Client and order management coming soon)")

# Tab 4: Route Analytics
with tabs[3]:
    st.markdown("# 📋 Route Frequency & History")
    sim = st.session_state.get("simulation")
    if not sim:
        st.warning("⚠️ Simulation not initialized or AVL route tracker missing.")
    else:
        st.write("(AVL-based route history and frequency analysis coming soon)")

# Tab 5: General Statistics
with tabs[4]:
    st.markdown("# 📈 General Statistics")
    sim = st.session_state.get("simulation")
    if not sim:
        st.warning("⚠️ Initialize a simulation first.")
    else:
        st.write("(Node frequency charts coming soon)")
