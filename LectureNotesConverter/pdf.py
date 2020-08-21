"""
lecturenotes2pdf.pdf

PDF generation
"""
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch

class PDFGenerator(object):
    def __init__(self, notebook, pdf_filename):
        self.notebook = notebook
        self.pdf_filename = pdf_filename

        self.dpi = 300.0
        self.pixel = inch / self.dpi

        self.width = notebook.paper_width * self.pixel
        self.height = notebook.paper_height * self.pixel

    def run(self):
        canvas = Canvas(self.pdf_filename, pagesize=(self.width, self.height))
        canvas.setTitle(self.notebook.name)

        for page in self.notebook.pages:
            self.draw_page(canvas, page)
            canvas.showPage()

        canvas.save()

    def draw_page(self, canvas, page):
        # Draw the background
        canvas.setFillColorRGB(*self.notebook.paper_color)
        canvas.rect(0, 0, self.width, self.height, stroke=0, fill=1)

        # Draw the layers
        layer = 1
        while layer <= self.notebook.displayed_layers:
            self.draw_image_layer(canvas, page, layer)
            layer += 1

    def draw_image_layer(self, canvas, page, layer):
        # Note the layers are 1-indexed
        canvas.drawImage(page.image_layers[layer-1],
                         0, 0, self.width, self.height,
                         mask='auto')

def notebook2pdf(notebook, pdf_filename):
    PDFGenerator(notebook, pdf_filename).run()
