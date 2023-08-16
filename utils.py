from fpdf import FPDF
import os
import datetime


t = datetime.datetime.today()
D =  t.strftime('%d/%m/%y')
D_file =  t.strftime('%d-%m-%y_%H%M%S')
pdf_folder="./pdfs"
# if folder doesn't exist create it
if not os.path.exists(pdf_folder):
    os.makedirs(pdf_folder)


def all_values_empty_or_none(dictionary):
    for value in dictionary.values():
        if value is not None and value:
            return False
    return True

def save_pdf(user): 
    if(not all_values_empty_or_none(user)):
        return None
    pdf = FPDF() 
    pdf.add_page()
    font="Arial" 

    pdf.set_font(font,"B", size = 20)
    pdf.cell(0, 10, txt = f"Diagnostic {user['name']}", align = 'C') #Title
    pdf.ln()
    pdf.cell(0, 10, txt = D, align = 'C') # Date
    pdf.ln()
#     pdf.set_font(font,"I", size = 12)
#     pdf.multi_cell(0, 10, txt = f"Name: {user['name'].capitalize()} \t\tAge: {user['age']} ") #User details
#     pdf.multi_cell(0, 10, txt = f"Height: {user['height']} \t\tWeight: {user['weight']} \t\tBMI: {user['bmi']}") #User details
#     pdf.ln()
    
    # User details with underlines
    pdf.set_font(font, "I", size=12)
    pdf.cell(20, 10, txt="Name:", ln=False)
    pdf.set_font(font, "IU", size=12)
    pdf.cell(40, 10, txt=f"{user['name'].capitalize()}", ln=False)
    pdf.set_font(font, "I", size=12)
    pdf.cell(20, 10, txt="Age:", ln=False)
    pdf.set_font(font, "IU", size=12)
    pdf.cell(20, 10, txt=f"{user['age']} years", ln=True)

    pdf.set_font(font, "I", size=12)
    pdf.cell(20, 10, txt="Weight:", ln=False)
    pdf.set_font(font, "IU", size=12)
    pdf.cell(20, 10, txt=f"{round(user['weight'],2)} kg", ln=False)

    pdf.set_font(font, "I", size=12)
    pdf.cell(20, 10, txt="Height:", ln=False)
    pdf.set_font(font, "IU", size=12)
    pdf.cell(20, 10, txt=f"{round(user['height'],2)} cm", ln=False)

    pdf.set_font(font, "I", size=12)
    pdf.cell(20, 10, txt="BMI:", ln=False)
    pdf.set_font(font, "IU", size=12)
    pdf.cell(20, 10, txt=f"{round(user['bmi'],2)}", ln=True)
    
    
    
    pdf.set_font(font,"B", size = 15)
    pdf.multi_cell(0, 10, txt = "Diagnostic:\n")
    pdf.set_font(font, size=12)
    pdf.multi_cell(0, 10, txt =user['disease'].capitalize())
    pdf.ln()
    
    pdf.set_font(font,"B", size = 15)
    pdf.multi_cell(0, 10, txt = "Definition:\n")
    pdf.set_font(font, size=12)
    pdf.multi_cell(0, 10, txt =user['description'].capitalize())
    pdf.ln()
    
    pdf.set_font(font,"B", size = 15)
    pdf.multi_cell(0, 10, txt = "Treatment:\n")
    pdf.set_font(font, size=12)
    pdf.multi_cell(0, 10, txt =user['treatment'].capitalize())
    pdf.ln()
    pdf.set_font(font,"B", size = 15)
    pdf.multi_cell(0, 10, txt = "Treatment (Secondary):\n")
    pdf.set_font(font, size=12)
    pdf.multi_cell(0, 10, txt =user['treatments'].capitalize())
    pdf.ln()
    pdf.ln()
    # if path doesn't exists create it
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
    pdf_path=os.path.join(pdf_folder,f"Diagnostic-{user['name']}-{D_file}.pdf")
    pdf.output(pdf_path,'F')#.encode('latin-1','ignore') 
    print("PDF SAVED AT", pdf_path)
    return pdf_path
 