from fastapi import APIRouter, Response
from io import BytesIO
from collections import Counter
import tempfile, os, sys

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen       import canvas
from reportlab.lib.utils    import ImageReader

import matplotlib.pyplot as plt

current_dir  = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.extend([project_root, os.path.join(project_root, 'sim')])

from sim.init_simulation import get_current_simulation

router = APIRouter()
simulation = get_current_simulation()

# ---------- helpers ----------
def _ascii_route(path_str: str) -> str:
    return path_str.replace("→", "->")

def _save_bar_chart(counter: Counter, title: str) -> str:
    labels, values = zip(*counter.items()) if counter else ([], [])
    plt.figure(figsize=(6,3))
    plt.bar(labels, values)
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.tight_layout()
    plt.savefig(tmp.name, dpi=150)
    plt.close()
    return tmp.name

# ---------- endpoint ----------
@router.get("/pdf")
def generar_pdf():
    orders     = simulation.get_orders()
    graph      = simulation.get_graph()
    roles      = simulation.get_node_roles()
    visits     = simulation.get_visits_by_role()
    clients    = [o.destination.element() for o in orders]
    route_freq = Counter(str(o.route).replace("→", "->") for o in orders)
    client_freq= Counter(clients)
    total_bat  = sum(o.battery_used for o in orders)

    # Gráficos
    chart_clients = _save_bar_chart(client_freq, "Clientes con más pedidos")
    chart_routes  = _save_bar_chart(route_freq,  "Rutas más usadas")

    # PDF
    buf = BytesIO()
    pdf = canvas.Canvas(buf, pagesize=letter)
    W, H = letter

    # 1) Portada
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(W/2, H-60, "Informe del Sistema Logístico de Drones")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, H-100, f"Total órdenes: {len(orders)}")
    pdf.drawString(50, H-120, f"Nodos totales: {len(graph.vertices())}")
    pdf.drawString(50, H-140, f"Aristas totales: {len(graph.edges())}")
    pdf.drawString(50, H-160, f"Nodos Cliente: {sum(1 for r in roles.values() if r=='client')}")
    pdf.drawString(50, H-180, f"Nodos Recarga: {sum(1 for r in roles.values() if r=='recharge')}")
    pdf.drawString(50, H-200, f"Nodos Almacén: {sum(1 for r in roles.values() if r=='storage')}")
    pdf.drawString(50, H-220, f"Energía total utilizada (batería): {total_bat}")
    pdf.showPage()

    # 2) Tabla de órdenes
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, H-50, "📦 Tabla de Pedidos")
    pdf.setFont("Helvetica", 10)
    y = H-80
    for o in orders:
        line = (f"{o.order_id[:8]}  "
                f"{_ascii_route(str(o.origin.element()))}->{_ascii_route(str(o.destination.element()))}  "
                f"P:{o.priority}  Cost:{o.route_cost}  Bat:{o.battery_used}")
        pdf.drawString(50, y, line)
        y -= 14
        if y < 60:
            pdf.showPage()
            y = H-50; pdf.setFont("Helvetica", 10)
    pdf.showPage()

    # 3) Rankings
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, H-50, "🏆 Clientes con más pedidos")
    pdf.setFont("Helvetica", 12)
    y = H-80
    for cli, n in client_freq.most_common():
        pdf.drawString(60, y, f"{cli}: {n}")
        y -= 14

    y -= 20
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "🛤️ Rutas más usadas")
    y -= 30
    pdf.setFont("Helvetica", 10)
    for r, n in route_freq.most_common():
        pdf.drawString(60, y, f"{r}  —  {n}")
        y -= 12
        if y < 60:
            pdf.showPage()
            y = H-60; pdf.setFont("Helvetica", 10)
    pdf.showPage()

    # 4) Gráficos
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(W/2, H-40, "📊 Gráficos de distribución")
    pdf.drawImage(ImageReader(chart_clients),  40, H/2,  W-80, H/3,  preserveAspectRatio=True)
    pdf.drawImage(ImageReader(chart_routes),   40, 40,   W-80, H/3,  preserveAspectRatio=True)

    pdf.save()
    buf.seek(0)

    # cleanup
    for f in (chart_clients, chart_routes):
        try: os.remove(f)
        except OSError: pass

    return Response(content=buf.read(),
                    media_type="application/pdf",
                    headers={"Content-Disposition": "attachment; filename=informe_logistica.pdf"})