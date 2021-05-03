from fpdf import FPDF
import datetime as dt

WIDTH = 210
HEIGHT = 297
#set height for 2 graphs per page
H1 = 70
H2 = 170
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

def create_analytics_report(path, filename = "budget_report.pdf"):
    pdf = FPDF() # A4 (210 by 297 mm)

    '''Presentation Page'''
    pdf.add_page()
    #pdf.image()
    create_presentation_page(pdf)
    
    '''First Page -- Last Month'''
    pdf.add_page()
    create_subtitle(f"Budget", 20, pdf)

    #Budget per user
    create_subtitle(f"First Analysis: money spent per user", 25, pdf)
    pdf.image(f"{path}/User.png", W1, H1, WIDTH/2-10)
    #pdf.image("", WIDTH/2, H1, WIDTH/2-10)

    #Budget per type
    create_subtitle(f"Second Analysis: money spent per type", 100, pdf)
    pdf.image(f"{path}/Type.png", W1, H2, WIDTH/2-10)
    #pdf.image("", WIDTH/2, H2, WIDTH/2-10)

    file_path = filename
    pdf.output(file_path, 'F')