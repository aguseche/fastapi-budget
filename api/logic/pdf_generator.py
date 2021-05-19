import pathlib
from fpdf import FPDF
import datetime as dt

from api.logic.manage_files import get_pdf_path


WIDTH = 210
HEIGHT = 297

IMAGE_WIDTH = WIDTH/2-10
#set height for 2 graphs per page
H1 = 60
H2 = 145
H3 = 210
W1 = 5 #standard

TITLE_FONT_SIZE = 24
SUBTITLE_FONT_SIZE = 20
SUBSUBTITLE_FONT_SIZE = 16

def create_presentation_page(pdf):
    pdf.set_font('Arial', '', TITLE_FONT_SIZE)  
    pdf.ln(30)
    pdf.write(5, "Budget Analytics Report")
    pdf.ln(10)
    pdf.set_font('Arial', '', SUBSUBTITLE_FONT_SIZE)
    pdf.write(4, f'{dt.date.today()}')
    pdf.ln(5)

def create_subtitle(text, y, pdf, font_size = SUBTITLE_FONT_SIZE):
    pdf.set_font('Arial', '', font_size)
    pdf.ln(y)
    pdf.cell(200, 4, text, align='C')

def create_analytics_report(path):
    '''
    Creates PDF report and retrieves the path
    '''
    pdf = FPDF() # A4 (210 by 297 mm)

    '''Presentation Page'''
    pdf.add_page()
    #pdf.image()
    create_presentation_page(pdf)
    
    '''First Page -- Last Month'''
    pdf.add_page()
    create_subtitle(f"Monthly Budget", 20, pdf)

    #First Analysis
    create_subtitle(f"First Analysis: money spent last month", 20, pdf)
    pdf.image(f"{path}/User-barchart.png", W1, H1, IMAGE_WIDTH)
    pdf.image(f"{path}/Type-barchart.png", WIDTH/2, H1, IMAGE_WIDTH)

    #Second Analysis
    create_subtitle(f"Second Analysis: graphs per user", 85, pdf)
    add_image(pdf, path / 'user0-barchart.png', W1, H2)
    add_image(pdf, path / 'user1-barchart.png', WIDTH/2, H2)
    add_image(pdf, path / 'user2-barchart.png', W1, H3)
    add_image(pdf, path / 'user3-barchart.png', WIDTH/2, H3)

    pdf.output(get_pdf_path(path), 'F')


def add_image(pdf, path, x, y):
    if pathlib.Path.is_file(path):
        pdf.image(str(path), x, y, IMAGE_WIDTH)

    