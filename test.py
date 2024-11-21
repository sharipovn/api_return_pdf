import pdfkit

# Path to wkhtmltopdf if needed
path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

# Configure pdfkit to use this executable
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

# Path to the HTML file
html_file = 'test.html'

# Output PDF file path
output_pdf = 'table_output.pdf'

# Options for scaling the content and fitting it to the page
options = {
    'page-size': 'A4',              # Set page size to A4
    'no-outline': None,             # Remove outlines
    'margin-top': '10mm',           # Top margin
    'margin-right': '10mm',         # Right margin
    'margin-bottom': '10mm',        # Bottom margin
    'margin-left': '10mm',          # Left margin
    'zoom': 1.0,                    # Optional: Adjust zoom level (1.0 means no zoom)
    'disable-smart-shrinking': True ,# Disable smart shrinking, to avoid unwanted scaling
    'page-width': '210mm',  # A4 width
    'page-height': '297mm'  # A4 height
}

# Convert the HTML file to PDF with the specified options
pdfkit.from_file(html_file, output_pdf, configuration=config, options=options)

print(f"PDF saved as {output_pdf}")
