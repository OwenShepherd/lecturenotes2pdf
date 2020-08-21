"""
lecturenotes2pdf.notebook

Interface to LectureNotes notebooks
"""

from collections import namedtuple
import logging
import os
import os.path
import xml.etree.ElementTree as ET

# Notebooks must point to an xml
class Notebook(object):
    def __init__(self, path_to_xml):
        if os.path.exists(path) and path.endswith('notebook.xml'):
            self.root_dir = os.path.dirname(path)
            self.name = os.path.basename(self.root_dir)
        else:
            raise ValueError("Invalid notebook location used.")

        # Create Page objects next
        i = 1
        self.pages = []
        while True:
            try:
                self.pages.append(Page(self, i))
                i += 1
            except ValueError:
                break

        self._notebook_xml = ET.parse(os.path.join(self.root, 'notebook.xml'))
        root = self._notebook_xml.getroot()

        self.paper_width = float(root.find('paperwidth').text)
        self.paper_height = float(root.find('paperheight').text)
        self.paper_color = parse_color(root.find('papercolor').text)
        # ignore pattern

        # ignore textlayersettings
        self.text_font_family = int(root.find('textlayerfontfamily').text) # ??
        self.text_font_style = int(root.find('textlayerfontstyle').text)
        self.text_font_size = float(root.find('textlayerfontsize').text)
        self.text_font_color = parse_color(root.find('textlayerfontcolor').text)
        self.text_margin_left = float(root.find('textlayerleftmargin').text)
        self.text_margin_top = float(root.find('textlayertopmargin').text)
        self.text_margin_right = float(root.find('textlayerrightmargin').text)
        self.text_margin_bottom = float(root.find('textlayerbottommargin').text)

        self.layers = int(root.find('layers').text)
        self.displayed_layers = int(root.find('displayedlayers').text)
        self.text_layer = int(root.find('textlayer').text)
        self.display_text = bool(int(root.find('displaytextlayer').text))

        # ignore paper scale and fit

        # Check if there is a text layer!
        self.have_text_layer = any(p.text is not None or p.text_boxes
                                   for p in self.pages)


class Page(object):
    def __init__(self, notebook, number):
        self.notebook = notebook
        self.root = notebook.root
        self.number = number

        # Collect image layers
        bg_1 = os.path.join(self.root, 'page{}.png'.format(number))
        if not os.path.exists(bg_1):
            raise ValueError("No such page: {}".format(number))

        self.image_layers = [bg_1]
        i = 2
        while True:
            path = os.path.join(self.root, 'page{}_{}.png'.format(number, i))
            if os.path.exists(path):
                self.image_layers.append(path)
                i += 1
            else:
                break