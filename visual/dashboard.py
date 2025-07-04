import sys, os, random
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from streamlit_folium import st_folium

current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.extend([
    project_root,
    os.path.join(project_root, 'sim'),
    os.path.join(project_root, 'domain')
])

from sim.init_simulation import run_simulation, get_current_simulation
from sim.persistence import * 
from visual.networkx_adapter import graph_to_networkx, draw_networkx_graph, draw_mst_graph
from visual.map.map_builder    import MapBuilder
from visual.map.flight_summary import flight_summary

# ---------- Layout ----------
st.set_page_config(page_title="Drone Logistics Simulator", layout="wide")
st.markdown("# ⛑️ Simulador de logística con drones - Entrega de suministros")

st.markdown("""
**Proporción de Roles de Nodos:**
- 📦 Nodos de Almacenamiento: 20%
- 🔋 Nodos de Recarga: 20%
- 👤 Nodos de Personas: 60%
""")

tabs = st.tabs([
    "🔄 Ejecutar Simulación",
    "🔎 Explorar Red",
    "🌐 Suministros y Refugios",
    "📋 Análisis de Rutas",
    "📈 Estadísticas",
])

# ---------- Pestaña 1 ----------
with tabs[0]:
    st.markdown("# ⚙️ Inicializar Simulación")
    num_nodes  = st.slider("Cantidad de Nodos", 10, 150, 15)
    num_edges  = st.slider("Cantidad de Aristas", 10, 300, 20)
    num_orders = st.slider("Cantidad de Pedidos", 1, 500, 10)

    st.markdown(f"**Nodos Cliente Derivados:** {int(num_nodes*0.6)}")

    if st.button("🚀 Iniciar Simulación"):
        sim = run_simulation(num_nodes, num_edges, num_orders)
        # Coordenadas aleatorias alrededor de Temuco
        coords = {v: (-38.7359 + random.uniform(-0.02,0.02),
                      -72.5904 + random.uniform(-0.02,0.02))
                  for v in sim.graph.vertices()}
        st.session_state.update({
            "simulation": sim,              # simulación actual
            "coords": coords,               # coordenadas de los nodos
            "boton_presionado": True,       # indica si se presionó el botón de iniciar
            "current_path": None,           # ruta actual seleccionada
            "show_mst": False,              # mostrar árbol de expansión mínima (MST)
        })
        save_simulation(sim)
        st.success("¡Simulación inicializada correctamente!")

# ---------- Pestaña 2 ----------
with tabs[1]:
    if not st.session_state.get("boton_presionado"):
        st.warning("⚠️ Primero debes inicializar una simulación.")
    else:
        sim = st.session_state.simulation
        coords = st.session_state.coords

        col1, col2 = st.columns(2)

        with col1:

            # --- Map View ---
            st.subheader("🗺️ Mapa Interactivo")
            mb = MapBuilder(sim.graph, sim.node_roles, coords)
            mb.add_base_graph()
            if st.session_state.get("show_mst"):
                mb.add_mst(sim.get_mst_edges())
            if st.session_state.get("last_path"):
                path = st.session_state.last_path
                battery = sum(sim.graph.get_edge(path[i], path[i+1]).element() for i in range(len(path)-1))
                popup = f"🔋 Batería estimada: {battery}"
                mb.add_route(
                st.session_state.last_path,
                color="red",
                popup_text=f"Ruta actual | Batería: {battery}",
                dashed=True
                )
            st_folium(mb.finish(), width=700, height=500)

            # --- 🚁 Entregar (crear orden real) ---
            st.subheader("📦 Calcular y Entregar (crear orden real)")
            origin = st.session_state.get("origin_select")
            destination = st.session_state.get("dest_select")

            if origin and destination:
                o_v = next(v for v in sim.graph.vertices() if str(v) == origin)
                d_v = next(v for v in sim.graph.vertices() if str(v) == destination)
                if st.button("🚁 Entregar Orden"):
                    res = flight_summary(sim, o_v, d_v)
                    save_simulation(sim)
                    if res:
                        info, order = res
                        st.success(f"✅ Entregado | Cost: {info['dist']} | Battery: {info['battery_used']}")
                        st.session_state.last_path = info['path']
                    else:
                        st.error("❌ No ruta viable con la autonomía actual.")
            else:
                st.info("Selecciona origen y destino en la columna de la derecha.")
            

        with col2:
            st.markdown("## 🚀 Calculate Route")

            # --- Select origen y destino con roles ---
            all_nodes = [str(v) for v in sim.graph.vertices()]
            clients  = [str(v) for v in sim.graph.vertices() if sim.node_roles[v] == "client"]
            storages = [str(v) for v in sim.graph.vertices() if sim.node_roles[v] == "storage"]

            origin = st.selectbox("Nodo Origen (Solo almacen)", storages, key="origin_select")
            destination = st.selectbox("Nodo Destino (Solo cliente)", clients, key="dest_select")

            # --- Selector de algoritmo ---
            st.markdown("### Routing Algorithm")
            algorithm = st.radio("Algoritmo de ruta", ["Dijkstra"], index=0)

            # --- Botones ---
            if st.button("Calculate Route"):
                o_v = next(v for v in sim.graph.vertices() if str(v) == origin)
                d_v = next(v for v in sim.graph.vertices() if str(v) == destination)
                path, used_bat, recs = sim.find_route_with_recharges_bfs(o_v, d_v)

                if path:
                    cost = sum(sim.graph.get_edge(path[i], path[i+1]).element()
                            for i in range(len(path)-1))
                    st.session_state.last_path = path
                    st.success("Calcular Ruta")
                    st.write(f"*Path:* {' → '.join(str(v) for v in path)}")
                    st.write(f"*Costo:* {cost}  |  *Bateria usada:* {used_bat}")
                    st.write("🔋 *Recargas:* " + (", ".join(str(v) for v in recs) if recs else "None"))
                else:
                    st.error("No valid route found.")

            if st.button("Mostrar MST (Kruskal)"):
                st.session_state.show_mst = not st.session_state.get("show_mst", False)

            # --- Stats de tipos de nodos ---
            st.markdown("### Tipos de Nodo:")
            by_role = sim.get_visits_by_role()
            storage_count  = len([v for v in sim.graph.vertices() if sim.node_roles[v] == "storage"])
            recharge_count = len([v for v in sim.graph.vertices() if sim.node_roles[v] == "recharge"])
            client_count   = len([v for v in sim.graph.vertices() if sim.node_roles[v] == "client"])

            st.markdown(f"- 📦 *Storage Nodes:* {storage_count}")
            st.markdown(f"- 🔋 *Recharge Nodes:* {recharge_count}")
            st.markdown(f"- 👤 *Client Nodes:* {client_count}")

# ---------- Pestaña 3 (Clients & Orders) ----------
with tabs[2]:
    st.markdown("# 🌐 Clients and Orders")
    if "simulation" not in st.session_state:
        st.warning("⚠️ Initialize a simulation first.")
    else:
        sim = st.session_state.simulation
        
        st.markdown("### Clients")
        st.json([c.to_dict() for c in sim.clients])
        st.markdown("### Orders")
        st.json([o.to_dict() for o in sim.orders])

# ---------- Pestaña 4 (Route Analytics) ----------
with tabs[3]:
    if not st.session_state.get("boton_presionado"):
        st.warning("⚠️ Inicializa una simulación primero.")
    else:
        sim = st.session_state.simulation
        route_counts = sim.get_route_counts()

        st.subheader("📥 Generar Informe PDF")

        if st.button("📄 Generar y Descargar PDF"):
            import requests
            try:
                response = requests.get("http://localhost:8000/reporte/pdf")
                if response.status_code == 200:
                    st.success("Informe generado correctamente.")
                    st.download_button(
                        label="📥 Descargar Informe",
                        data=response.content,
                        file_name="informe_rutas.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("Error al generar el PDF desde el servidor.")
            except Exception as e:
                st.error(f"No se pudo conectar al backend: {e}")

        st.subheader("📈 Rutas más Frecuentes")
        if route_counts:
            for ruta, cnt in sorted(route_counts.items(), key=lambda x: -x[1]):
                st.markdown(f"- {ruta} — **{cnt}** veces")
        else:
            st.info("No hay rutas registradas.")

        st.subheader("📜 Historial de Rutas")
        for i, r in enumerate(sim.get_routes(), 1):
            st.markdown(f"**Ruta #{i}:** {r}")

        st.subheader("🌳 Árbol de Expansión Mínima (Kruskal)")
        if st.button("Mostrar Árbol de Expansión Mínima"):
            import requests
            try:
                response = requests.get("http://localhost:8000/info/mst")
                if response.status_code == 200:
                    mst = response.json()
                    for edge in mst:
                        st.markdown(f"- {edge['from']} → {edge['to']} — Peso: {edge['weight']}")
                    else:
                        st.error("No se pudo obtener el árbol mínimo del servidor.")
            except Exception as e:
                st.error(f"No se pudo conectar al backend: {e}")

# ---------- Pestaña 5 (Statistics) ----------
with tabs[4]:
    st.markdown("# 📈 General Statistics")
    if not st.session_state.get("boton_presionado"):
        st.warning("⚠️ Initialize a simulation first.")
    else:
        sim = st.session_state.simulation
        by_role = sim.get_visits_by_role()
        col1,col2,col3 = st.columns(3)
        for role,col in zip(["client","recharge","storage"],[col1,col2,col3]):
            with col:
                st.markdown(f"#### {role.capitalize()}")
                data = by_role[role]
                if data:
                    fig, ax = plt.subplots()
                    ax.bar(list(data.keys()), list(data.values()))
                    st.pyplot(fig)
                else:
                    st.write("No data")
