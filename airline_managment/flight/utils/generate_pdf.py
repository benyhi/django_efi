from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO

def generar_pdf(request, vuelos_queryset):
    vuelos_data = []
    for vuelo in vuelos_queryset:
        reservas = vuelo.reservation_set.select_related('passenger', 'seat').all()
        vuelos_data.append({
            "vuelo": vuelo,
            "reservas": reservas
        })

    context = {
        "titulo": "Reporte de Vuelos y Pasajeros",
        "vuelos_data": vuelos_data
    }

    html_string = render_to_string("flight/flight_report.html", context)

    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(pdf_file)
    pdf_file.seek(0)
    response = HttpResponse(pdf_file.read(), content_type="application/pdf")
    response['Content-Disposition'] = 'inline; filename="reporte_pasajerosXvuelo.pdf"'
    return response
