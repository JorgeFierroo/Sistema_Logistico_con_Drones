import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt



st.set_page_config(page_title="Simulador de Logística con Drones", layout="wide")

st.markdown("# 🚁 Simulador de Logística con Drones - Correos Chile")

# Leyenda de proporciones
st.markdown("""
**Proporciones de roles de nodos:**
- 📦 Nodos de Almacenamiento: 20%
- 🔋 Nodos de Recarga: 20%
- 👤 Nodos de Clientes: 60%
""")

# Pestañas
tabs = st.tabs(["🔄 Ejecutar Simulación", "🔎 Explorar Red", "🌐 Clientes y Pedidos", "📋 Análisis de ruta", "📈 Estadísticas"])

# Contenido de la primera pestaña
with tabs[0]:

    
    st.markdown("# ⚙️ Inicializar Simulación")

    # Sliders
    num_nodes = st.slider("Número de Nodos", min_value=10, max_value=150, value=15)
    num_edges = st.slider("Número de Conexiones", min_value=10, max_value=300, value=20)
    num_orders = st.slider("Número de Pedidos", min_value=1, max_value=500, value=10)

    # Cálculo de clientes (60%)
    num_clients = int(num_nodes * 0.6)
    st.markdown(f"**Nodos de Cliente Derivados:** {num_clients} (60% of {num_nodes})")

    # Botón
    if st.button("🚀 Iniciar Simulación"):
        st.session_state["boton_presionado"] = True
        st.success("¡Simulación iniciada correctamente!")

with tabs[1]:

    st.markdown("# 🌍 Visualización de la Red")

    if not st.session_state.get("boton_presionado", False):
        st.warning("⚠️ Primero debes iniciar una simulación.")
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
                
                if st.button("✅ Crear Entrega y Pedido"):
                    st.success("Pedido creado y entregado al cliente.")

        with right_col:
            st.subheader("📌 Calcular Ruta")

            option1 = st.selectbox("Seleccione opción 1", ["Opción A", "Opción B", "Opción C"])
            option2 = st.selectbox("Seleccione opción 2", ["Valor 1", "Valor 2", "Valor 3"])

            if st.button("✈️ Calcular Ruta"):
                # Aquí puedes usar las opciones seleccionadas
                st.success("Pedido creado y entregado al cliente con opciones.")
        


with tabs[2]:
    st.markdown("# 🌐 Clientes y Pedidos")

    if not st.session_state.get("boton_presionado", False):
        st.warning("⚠️ Primero debes iniciar una simulación.")
    else:
        pass

with tabs[3]:
    st.markdown("# 📋 Frecuencia de Rutas e Historial") 

    if not st.session_state.get("boton_presionado", False):
        st.warning("⚠️ Simulación no iniciada o faltan rutas registradas.")
    else:
        pass

with tabs[4]:
    st.markdown("# 📈 Estadísticas Generales")  

    if not st.session_state.get("boton_presionado", False):
        st.warning("⚠️ Primero debes iniciar una simulación.")
    else:
        st.subheader("📊 Nodos Más Visitados por Rol")
        left_col, center_col, right_col = st.columns(3)

        with left_col: 

            st.markdown("##### 👤 Clientes más visitados")

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

            st.markdown("##### 🔋 Estaciones de recarga más visitadas")

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

            st.markdown("##### 📦 Nodos de almacenamiento más visitados")

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