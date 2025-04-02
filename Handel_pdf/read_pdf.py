import PyPDF2
import os
def read_pdf_to_text(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    
    return text

def extract_text_from_pdf(pdf_file):
    try:
        if isinstance(pdf_file, str):
            with open(pdf_file, 'rb') as file:
                return read_pdf_to_text(file), os.path.basename(pdf_file)
        else:
            return read_pdf_to_text(pdf_file), pdf_file.name
    except Exception as e:
        print(f"extract_text_from_pdf 函数出错: {e}")