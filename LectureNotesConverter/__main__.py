"""
lecturenotes2pdf: Convert LectureNotes notebooks to PDF format
"""

from __future__ import absolute_import, print_function

import argparse
import logging
import sys

from .notebook import Notebook
from .pdf import notebook2pdf

def main():
    notebook_pdf_filename = "sandbox_conversion.pdf"
    notebook_location = ""
    notebook_at_location = Notebook(notebook_location)
    notebook2pdf(notebook_at_location,notebook_pdf_filename)


if __name__ == '__main__':
    main()
