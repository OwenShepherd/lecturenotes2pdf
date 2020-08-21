"""
lecturenotes2pdf.pdf

PDF generation
"""

from __future__ import print_function, absolute_import

# import logging

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch

from .notebook import TextingMachine

_log = logging.getLogger(__name__)

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
            _log.info('{}: drawing page {}'.format(self.notebook.name, page.number))
            self.draw_page(canvas, page)
            canvas.showPage()

        canvas.save()

    def draw_page(self, canvas, page):
        # Draw the background
        canvas.setFillColorRGB(*self.notebook.paper_color)
        canvas.rect(0, 0, self.width, self.height, stroke=0, fill=1)

        # Draw the layers
        layer = 1
        img_layer = 1
        while layer <= self.notebook.displayed_layers:
            if self.notebook.have_text_layer and self.notebook.text_layer == layer:
                self.draw_text_layer(canvas, page)
            else:
                self.draw_image_layer(canvas, page, img_layer)
                # note the image layer counter does not increment when
                # we draw a text layer
                img_layer += 1
            layer += 1

    def draw_image_layer(self, canvas, page, layer):
        _log.debug('{}: page {}: drawing image layer {}'.format(
            self.notebook.name, page.number, layer))
        # Note the layers are 1-indexed
        canvas.drawImage(page.image_layers[layer-1],
                         0, 0, self.width, self.height,
                         mask='auto')

def notebook2pdf(notebook, pdf_filename):
    PDFGenerator(notebook, pdf_filename).run()
