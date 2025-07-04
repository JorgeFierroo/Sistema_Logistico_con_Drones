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
    os.path.join(project_root, 'domain'),
])

from sim.init_simulation import run_simulation, get_current_simulation
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
            # --- NetworkX Grafo ---
            G_nx = graph_to_networkx(sim.get_graph(), sim.get_orders())
            fig  = draw_networkx_graph(G_nx, st.session_state.get("current_path"))
            st.pyplot(fig)

            if st.button("🌳 Mostrar MST"):
                mst_edges  = sim.graph.kruskal_mst()
                edge_tuples = [(str(e.endpoints()[0]), str(e.endpoints()[1])) for e in mst_edges]
                fig_mst = draw_mst_graph(G_nx, edge_tuples)
                st.pyplot(fig_mst)

            # --- Map View ---
            st.subheader("🗺️ Mapa Interactivo")
            mb = MapBuilder(sim.graph, sim.node_roles, coords)
            mb.add_base_graph()
            if st.session_state.get("show_mst"):
                mb.add_mst(sim.get_mst_edges())
            if st.session_state.get("last_path"):
                mb.add_route(st.session_state.last_path, color="red")
            st_folium(mb.finish(), width=700, height=500)

        with col2:
            # --- Calcular ruta normal ---
            st.subheader("📌 Calcular Ruta (solo visualizar)")
            all_nodes = [str(v) for v in sim.graph.vertices()]
            origin = st.selectbox("Origen", all_nodes, key="o_net")
            destination = st.selectbox("Destino", all_nodes, key="d_net")

            if st.button("✈️ Calcular Ruta"):
                o_v = next(v for v in sim.graph.vertices() if str(v) == origin)
                d_v = next(v for v in sim.graph.vertices() if str(v) == destination)
                path, used_bat, recs = sim.find_route_with_recharges_bfs(o_v, d_v)
                if path:
                    cost = sum(sim.graph.get_edge(path[i], path[i+1]).element()
                            for i in range(len(path)-1))
                    st.session_state.current_path = [str(v) for v in path]
                    st.success("Ruta calculada")
                    st.write(f"Path: {' → '.join(str(v) for v in path)}")
                    st.write(f"Cost: {cost}  |  Battery: {used_bat}")
                    st.write("Recargas: " + (", ".join(str(v) for v in recs) if recs else "None"))
                else:
                    st.error("No se encontró una ruta válida.")

            # --- Entregar (crear orden real) ---
            st.subheader("📦 Calcular y Entregar (crear orden real)")
            o = st.selectbox("Origen Entrega", all_nodes, key="o_map")
            d = st.selectbox("Destino Entrega", all_nodes, key="d_map")
            if st.button("🚁 Entregar"):
                o_v = next(v for v in sim.graph.vertices() if str(v)==o)
                d_v = next(v for v in sim.graph.vertices() if str(v)==d)
                res = flight_summary(sim, o_v, d_v)
                if res:
                    info, order = res
                    st.success(f"Entregado | Cost {info['dist']} | Bat {info['battery_used']}")
                    st.session_state.last_path = info['path']
                else:
                    st.error("No ruta viable con la autonomía actual.")

            if st.button("🌲 Toggle MST en Mapa"):
                st.session_state.show_mst = not st.session_state.get("show_mst", False)

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
