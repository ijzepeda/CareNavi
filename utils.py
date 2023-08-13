from fpdf import FPDF
import os
import datetime


t = datetime.datetime.today()
D =  t.strftime('%d-%m-%y_%H%M%S')
pdf_folder="./pdfs"

def save_pdf(user): 
    pdf = FPDF() 
    pdf.add_page()
    font="Arial"
    fontstyle=True

    pdf.set_font(font,"B" if fontstyle else "", size = 20)
    pdf.cell(0, 10, txt = f"Diagnostic-{user['name']}", align = 'C')
    pdf.cell(0, 10, txt = D, align = 'C')
    pdf.ln()
    pdf.set_font(font,"I" if fontstyle else "", size = 12)
    pdf.multi_cell(0, 10, txt = "Diagnostic:\n"+user['disease'])
    pdf.ln()
    pdf.set_font(font, size = 15)
    pdf.multi_cell(0, 10, txt = "Treatment:\n"+ user['treatment'])
    pdf.ln()
    # if path doesn't exists create it
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
    pdf_path=os.path.join(pdf_folder,f"Diagnostic-{user['name']}-{D}.pdf")
    pdf.output(pdf_path,'F')#.encode('latin-1','ignore') 
    return ""
 