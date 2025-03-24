from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import uuid
import os
from django.http import JsonResponse

def generate_pdf(request):
    if request.method == 'POST':
        link = request.POST.get('link')
        if not link:
            return JsonResponse({'error': 'Link is required'}, status=400)

        # Render the HTML template
        html_content = render_to_string('pdf_template.html', {'link': link})

        # Generate unique filename
        output_path = f"{uuid.uuid4()}.pdf"

        # Convert HTML to PDF
        pdf_file = HTML(string=html_content).write_pdf()

        # Return as a response
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="output.pdf"'
        return response

    return JsonResponse({'error': 'Invalid request'}, status=400)
