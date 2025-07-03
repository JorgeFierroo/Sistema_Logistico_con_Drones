from fastapi import APIRouter, Response
from sim.simulation import Simulation
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

router = APIRouter()

# Instancia global compartida (o podrías recibirla vía dependencia)
simulation = Simulation()

@router.get("/pdf")
def generar_pdf():
    """
    Genera un PDF con el resumen de órdenes.
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Informe de Órdenes - Sistema de Drones")

    p.setFont("Helvetica", 12)
    y = height - 80

    orders = simulation.get_orders()
    if not orders:
        p.drawString(50, y, "No hay órdenes registradas.")
    else:
        for order in orders:
            text = f"Orden #{order.order_id} | {order.origin.element()} → {order.destination.element()} | Prioridad: {order.priority} | Costo: {order.route_cost}"
            p.drawString(50, y, text)
            y -= 20
            if y < 60:
                p.showPage()
                y = height - 60
                p.setFont("Helvetica", 12)

    p.save()
    buffer.seek(0)

    return Response(content=buffer.read(), media_type="application/pdf")
