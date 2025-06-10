import streamlit as st

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
tabs = st.tabs(["🔄 Run Simulation", "🔎 Explore Network", "🌐 Clients & Orders", "📋 Route Analytics", "📈 Statistics"])

# Contenido de la primera pestaña
with tabs[0]:
    st.subheader("⚙️ Initialize Simulation")

    # Sliders
    num_nodes = st.slider("Number of Nodes", min_value=10, max_value=150, value=15)
    num_edges = st.slider("Number of Edges", min_value=10, max_value=300, value=20)
    num_orders = st.slider("Number of Orders", min_value=1, max_value=500, value=10)

    # Cálculo de clientes (60%)
    num_clients = int(num_nodes * 0.6)
    st.markdown(f"**Derived Client Nodes:** {num_clients} (60% of {num_nodes})")

    # Botón
    if st.button("🚀 Start Simulation"):
        st.success("Simulation initialized!")

# Puedes añadir contenido a las demás pestañas así:
with tabs[1]:
    st.info("🌍 Network exploration tools go here.")

with tabs[2]:
    st.info("🌐 Client and order data goes here.")

with tabs[3]:
    st.info("📋 Route analytics interface goes here.")

with tabs[4]:
    st.info("📈 General statistics and performance metrics go here.")
