import asyncio
import os
import uuid
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.template.loader import render_to_string
from weasyprint import HTML

async def html_to_pdf(html_content, output_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # ✅ Ensure headless mode
        page = await browser.new_page()
        await page.set_content(html_content)
        await page.pdf(path=output_path)
        await browser.close()

@csrf_exempt
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
        pdf_file = HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf()

        # Return as a response
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="output.pdf"'
        return response

    return JsonResponse({'error': 'Invalid request'}, status=400)

def index(request):
    return render(request, 'index.html')
