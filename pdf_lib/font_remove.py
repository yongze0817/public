import fitz
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap

def remove_superscript_from_pdf(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    result_text = ""
    
    front_size = None   
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        try:
            text_blocks = page.get_text("dict")["blocks"]
            for text_block in text_blocks:
                lines = text_block.get("lines", [])
                for line in lines:
                    for span in line.get("spans", []):
                        text = span["text"]
                        current_size = span["size"] 
                        if front_size is not None and current_size < front_size: 
                            filtered_text = "".join(char for char in text if not char.isdigit())
                            result_text += filtered_text

                        elif "(" in text and any(char.isdigit() for char in text):
                            number_str = text[text.find('(')+1:text.find(')')]

                            if number_str.lstrip('-').replace(',', '').isdigit():
                                number_in_brackets = int(number_str.replace(',', ''))
                                neg_number = str(-number_in_brackets)
                                result_text += neg_number
                            else:  
                                result_text += text

                        else:  
                            result_text += text
                        front_size = current_size
        except Exception as e:
            print(f"An error occurred while processing page {page_num}: {e}")

    wrapped_string = textwrap.fill(result_text, width=100)
    
    def write_to_pdf(text, filename):
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        lines = text.split('\n')
        x = 50
        y = height - 50
        for line in lines:
            if y < 50:  # 如果已经到达页面底部，则添加新的页面
                c.showPage()
                y = height - 50
            c.drawString(x, y, line)
            y -= 14  # 每行的高度大约为14点 

        c.save()
    
    write_to_pdf(wrapped_string, output_path)
    


pdf_path = 'C:/Users/yuanma/Desktop/beke_2023Q4.pdf'
output_path = 'C:/Users/yuanma/Desktop/output.pdf'
superscript_text = remove_superscript_from_pdf(pdf_path, output_path)
