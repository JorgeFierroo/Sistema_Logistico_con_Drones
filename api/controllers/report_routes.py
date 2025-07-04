from fastapi import APIRouter, Response
from io import BytesIO
from collections import Counter
import tempfile, os, sys

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

import matplotlib.pyplot as plt

current_dir = os.path.dirname(__file__)
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
    plt.figure(figsize=(6, 3))
    plt.bar(labels, values)
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.tight_layout()
    plt.savefig(tmp.name, dpi=150)
    plt.close()
    return tmp.name

def _save_pie_chart(roles: dict, title: str) -> str:
    role_counts = Counter(roles.values())
    labels = {
        "storage": "Almacenamiento",
        "recharge": "Recarga",
        "client": "Personas"
    }

    sizes = [
        role_counts.get("storage", 0),
        role_counts.get("recharge", 0),
        role_counts.get("client", 0)
    ]

    label_list = [
        labels["storage"],
        labels["recharge"],
        labels["client"]
    ]

    colors = ["#4CAF50", "#2196F3", "#FFC107"]

    plt.figure(figsize=(5, 5))
    plt.pie(sizes, labels=label_list, autopct="%1.1f%%", startangle=90, colors=colors)
    plt.title(title)
    plt.axis("equal")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.tight_layout()
    plt.savefig(tmp.name, dpi=150)
    plt.close()
    return tmp.name


# ---------- endpoint ----------
@router.get("/pdf")
def generar_pdf():
    orders = simulation.get_orders()
    graph = simulation.get_graph()
    roles = simulation.get_node_roles()
    clients_data = simulation.get_clients()
    clients = [o.destination.element() for o in orders]
    route_freq = Counter(str(o.route).replace("→", "->") for o in orders)
    client_freq = Counter(clients)
    total_bat = sum(o.battery_used for o in orders)

    # Gráficos
    chart_clients = _save_bar_chart(client_freq, "Clientes con más pedidos")
    chart_routes = _save_bar_chart(route_freq, "Rutas más usadas")
    chart_roles = _save_pie_chart(roles, "Proporción de Roles de Nodos")

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
    pdf.drawString(50, H-160, f"Nodos Cliente: {sum(1 for r in roles.values() if r == 'client')}")
    pdf.drawString(50, H-180, f"Nodos Recarga: {sum(1 for r in roles.values() if r == 'recharge')}")
    pdf.drawString(50, H-200, f"Nodos Almacén: {sum(1 for r in roles.values() if r == 'storage')}")
    pdf.drawString(50, H-220, f"Energía total utilizada (batería): {total_bat}")
    pdf.showPage()

    # 2) Tabla de Clientes
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, H - 50, "Clientes Registrados")
    pdf.setFont("Helvetica-Bold", 10)
    y = H - 80
    pdf.drawString(50, y, "Cliente id")
    pdf.drawString(130, y, "Nombre")
    pdf.drawString(230, y, "Tipo")
    pdf.drawString(300, y, "Total ordenes")
    pdf.setFont("Helvetica", 10)
    y -= 20

    for c in clients_data:
        pdf.drawString(50, y, str(c.client_id))
        pdf.drawString(130, y, str(c.name))
        pdf.drawString(230, y, str(c.type))
        pdf.drawString(300, y, str(len(c.orders)))
        y -= 14
        if y < 60:
            pdf.showPage()
            y = H - 50
    pdf.showPage()

    # 3) Tabla de Pedidos
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, H-50, "Tabla de Pedidos")
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
            y = H-50
            pdf.setFont("Helvetica", 10)
    pdf.showPage()

    # 4) Ranking: Clientes con más pedidos
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, H - 50, "Clientes con más pedidos")
    pdf.setFont("Helvetica", 12)
    y = H - 80
    for cli, n in client_freq.most_common():
        pdf.drawString(60, y, f"{cli}: {n}")
        y -= 14
        if y < 60:
            pdf.showPage()
            y = H - 60
    pdf.showPage()

    # 5) Ranking: Rutas más usadas
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, H - 50, "Rutas más usadas")
    pdf.setFont("Helvetica", 10)
    y = H - 80
    for r, n in route_freq.most_common():
        pdf.drawString(60, y, f"{r}  —  {n}")
        y -= 12
        if y < 60:
            pdf.showPage()
            y = H - 60
    pdf.drawImage(ImageReader(chart_routes), 40, 40, W - 80, H / 3, preserveAspectRatio=True)
    pdf.showPage()

    # 6) Gráfico: Clientes con más pedidos
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(W / 2, H - 40, "Clientes con más pedidos")
    pdf.drawImage(ImageReader(chart_clients), 40, H / 2 - 40, W - 80, H / 2, preserveAspectRatio=True)
    pdf.showPage()

    # 7) Gráfico: Proporción de Roles
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(W / 2, H - 40, "Proporción de Roles de Nodos")
    pdf.drawImage(ImageReader(chart_roles), 100, H / 2 - 100, W - 200, W - 200, preserveAspectRatio=True)

    pdf.save()
    buf.seek(0)

    # cleanup
    for f in (chart_clients, chart_routes, chart_roles):
        try:
            os.remove(f)
        except OSError:
            pass

    return Response(content=buf.read(),
                    media_type="application/pdf",
                    headers={"Content-Disposition": "attachment; filename=informe_logistica.pdf"})
