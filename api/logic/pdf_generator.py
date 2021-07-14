import pathlib
from fpdf import FPDF
import datetime as dt

from api.logic.manage_files import get_pdf_path


WIDTH = 210
HEIGHT = 297

IMAGE_WIDTH = WIDTH/2-10
#set height for 2 graphs per page
H1 = 55
H2 = 140
H3 = 210
W1 = 5 #standard
W2 = WIDTH/2

TITLE_FONT_SIZE = 24
SUBTITLE_FONT_SIZE = 20
SUBSUBTITLE_FONT_SIZE = 16

class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', '', 15)
        # Title
        self.cell(30, 10, 'Budget Analytics Report')
        self.cell(130)
        self.cell(30, 10, f'{dt.date.today()}')
        # Line break
        self.ln(20)



    # pdf.write(4, )
def create_subtitle(text, y, pdf, font_size = SUBTITLE_FONT_SIZE):
    pdf.set_font('Arial', '', font_size)
    pdf.ln(y)
    pdf.cell(200, 4, text, align='C')

def create_analytics_report(path):
    '''
    Creates PDF report and retrieves the path
    '''
    pdf = PDF() # A4 (210 by 297 mm)

    '''First Page'''
    pdf.add_page()
    # create_presentation_page(pdf)
    create_subtitle(f"Monthly Budget", 0, pdf)
    create_subtitle(f"First Analysis: money spent last month", 15, pdf)
    pdf.image(f"{path}/User-barchart.png", 40, 60, 130)
    pdf.image(f"{path}/Type-barchart.png", 40, 160, 130)

    '''Second Page'''
    #Second Analysis
    for i in range(12):
        w = set_width(i)
        h = set_heigth(i)
        file_path = path / f'user{i}-barchart.png'
        if validate_filepath(file_path):
            if i == 6 or i==0:
                pdf.add_page()
                create_subtitle(f"Second Analysis: graphs per user", 15, pdf)
            pdf.image(str(file_path), w, h, IMAGE_WIDTH)
        else:
            break

    '''Third Page'''
    pdf.add_page()
    create_subtitle(f"Third Analysis: comparative between last 3 months", 15, pdf)
    pdf.image(f"{path}/User-monthsbarchart.png", 40, 60, 130)
    pdf.image(f"{path}/Type-monthsbarchart.png", 40, 160, 130)

    pdf.output(get_pdf_path(path), 'F')

def set_width(i:int)-> int:
        if (i % 2) == 0:
            return W1
        return W2

def set_heigth(i:int)-> int:
        if i <=1:
            return H1
        elif i<=3:
            return H2
        return H3

#delete
def validate_filepath(path: pathlib.PosixPath)->bool:
    if pathlib.Path.is_file(path):
        return True
