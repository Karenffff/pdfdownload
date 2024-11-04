import asyncio
import os
import uuid
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from playwright.async_api import async_playwright

async def html_to_pdf(html_content, output_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html_content)
        await page.pdf(path=output_path)
        await browser.close()

@csrf_exempt
def generate_pdf(request):
    if request.method == 'POST':
        link = request.POST.get('link')
        print(link)

        if not link:
            return JsonResponse({'error': 'link is required'}, status=400)

        # Render the HTML template with the user-provided number
        html_content = render_to_string('pdf_template.html', {'link': link})

        # Generate a unique filename for the PDF
        output_path = f"{uuid.uuid4()}.pdf"

        # Generate PDF asynchronously
        asyncio.run(html_to_pdf(html_content, output_path))

        # Serve the PDF file as a response
        with open(output_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="output.pdf"'

        # Clean up the file after sending the response
        os.remove(output_path)

        return response
    return JsonResponse({'error': 'Invalid request'}, status=400)

def index(request):
    return render(request, 'index.html')
