import streamlit as st
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np



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

    
    st.markdown("# ⚙️ Initialize Simulation")

    # Sliders
    num_nodes = st.slider("Number of Nodes", min_value=10, max_value=150, value=15)
    num_edges = st.slider("Number of Edges", min_value=10, max_value=300, value=20)
    num_orders = st.slider("Number of Orders", min_value=1, max_value=500, value=10)

    # Cálculo de clientes (60%)
    num_clients = int(num_nodes * 0.6)
    st.markdown(f"**Derived Client Nodes:** {num_clients} (60% of {num_nodes})")

    # Botón
    if st.button("🚀 Start Simulation"):
        st.session_state["boton_presionado"] = True
        st.success("Simulation initialized successfully!")

with tabs[1]:

    st.markdown("# 🌍 Network Visualization")

    if not st.session_state.get("boton_presionado", False):
        st.warning("⚠️ Initialize a simulation first.")
    else:
        # Crear dos columnas (50% y 50%)
        left_col, right_col = st.columns(2)

        with left_col:

            # Grafo simple de ejemplo
            G = nx.Graph()
            G.add_edges_from([("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")])

            if len(G.nodes) == 0:
                st.warning("No hay nodos para mostrar en el grafo.")
            else:
                pos = nx.spring_layout(G)
                fig, ax = plt.subplots(figsize=(5, 4))
                nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", ax=ax)
                st.pyplot(fig)
                
                if st.button("✅ Create Delivery and Create Order"):
                    # Aquí puedes usar las opciones seleccionadas
                    st.success("Order created and delivered for client")

        with right_col:
            st.subheader("📌 Calculate Route")

            option1 = st.selectbox("Seleccione opción 1", ["Opción A", "Opción B", "Opción C"])
            option2 = st.selectbox("Seleccione opción 2", ["Valor 1", "Valor 2", "Valor 3"])

            if st.button("✈️ Calculate Route"):
                # Aquí puedes usar las opciones seleccionadas
                st.success("Order created and delivered for client with options")
        


with tabs[2]:
    st.markdown("# 🌐 Clients and Orders")

    if not st.session_state.get("boton_presionado", False):
        st.warning("⚠️ Initialize a simulation first.")
    else:
        pass

with tabs[3]:
    st.markdown("# 📋 Route Frequency & History") 

    if not st.session_state.get("boton_presionado", False):
        st.warning("⚠️ Simulation not initialized or AVL route tracker missing.")
    else:
        pass

with tabs[4]:
    st.markdown("# 📈 General Statistics")  

    if not st.session_state.get("boton_presionado", False):
        st.warning("⚠️ Initialize a simulation first.")
    else:
        st.subheader("📊 Top Visited Nodes by Role")
        left_col, center_col, right_col = st.columns(3)

        with left_col: 

            st.markdown("##### 👤 Most Visited Clients")

            categorias = ['A', 'B', 'C', 'D']
            valores = [23, 45, 12, 36]

            # Crear figura y ejes con fondo transparente
            fig, ax = plt.subplots(facecolor='none')

            # Dibujar gráfico de barras (con zorder alto para que estén por encima del grid)
            ax.bar(categorias, valores, color='skyblue', zorder=3)

            # Fondo transparente
            ax.set_facecolor('none')
            fig.patch.set_alpha(0.0)

            # Líneas horizontales sólidas detrás de las barras
            ax.yaxis.grid(True, color='#222222', linestyle='-', linewidth=0.7, zorder=1)
            ax.xaxis.grid(False)

            ax.tick_params(axis='y', length=0, colors='white')  # Eje Y sin líneas, texto blanco
            ax.tick_params(axis='x', length=0, colors='white')  # Eje X sin líneas, texto blanco

            # Quitar el marco
            for spine in ax.spines.values():
                spine.set_visible(False)

            # Mostrar en Streamlit
            st.pyplot(fig)


        with center_col: 

            st.markdown("##### 🔋 Most Visited Recharge Stations")

            categorias = ['A', 'B', 'C', 'D']
            valores = [23, 45, 12, 36]

            # Crear figura y ejes con fondo transparente
            fig, ax = plt.subplots(facecolor='none')

            # Dibujar gráfico de barras (con zorder alto para que estén por encima del grid)
            ax.bar(categorias, valores, color='skyblue', zorder=3)

            # Fondo transparente
            ax.set_facecolor('none')
            fig.patch.set_alpha(0.0)

            # Líneas horizontales sólidas detrás de las barras
            ax.yaxis.grid(True, color='#222222', linestyle='-', linewidth=0.7, zorder=1)
            ax.xaxis.grid(False)

            ax.tick_params(axis='y', length=0, colors='white')  # Eje Y sin líneas, texto blanco
            ax.tick_params(axis='x', length=0, colors='white')  # Eje X sin líneas, texto blanco

            # Quitar el marco
            for spine in ax.spines.values():
                spine.set_visible(False)

            # Mostrar en Streamlit
            st.pyplot(fig)


        with right_col: 

            st.markdown("##### 📦 Most Visited Storage Nodes")

            categorias = ['A', 'B', 'C', 'D']
            valores = [23, 45, 12, 36]

            # Crear figura y ejes con fondo transparente
            fig, ax = plt.subplots(facecolor='none')

            # Dibujar gráfico de barras (con zorder alto para que estén por encima del grid)
            ax.bar(categorias, valores, color='skyblue', zorder=3)

            # Fondo transparente
            ax.set_facecolor('none')
            fig.patch.set_alpha(0.0)

            # Líneas horizontales sólidas detrás de las barras
            ax.yaxis.grid(True, color='#222222', linestyle='-', linewidth=0.7, zorder=1)
            ax.xaxis.grid(False)

            ax.tick_params(axis='y', length=0, colors='white')  # Eje Y sin líneas, texto blanco
            ax.tick_params(axis='x', length=0, colors='white')  # Eje X sin líneas, texto blanco

            # Quitar el marco
            for spine in ax.spines.values():
                spine.set_visible(False)

            # Mostrar en Streamlit
            st.pyplot(fig)