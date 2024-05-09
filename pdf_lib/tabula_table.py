import tabula
import fitz
import pandas as pd

def extract_table_from_pdf(pdf_path):
    tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)
    return(tables)


def create_pdf_from_dataframe(dataframes, output_path):
    doc = fitz.open()

    for df in dataframes:
        table_text = '\n'.join('\t'.join(str(cell) for cell in row) for row in df.values)
        page = doc.new_page()
        page.insert_text((100, 100), "Table Data")  # 添加表头
        page.insert_text((100, 120), table_text) 

    # 保存PDF文件
    doc.save(output_path)
    doc.close()


# 调用函数并提取表格数据
if __name__ == "__main__":
    pdf_path = "C:/Users/yuanma/Desktop/beke_2023Q4.pdf"
    table_data = extract_table_from_pdf(pdf_path)
    create_pdf_from_dataframe(table_data,"C:/Users/yuanma/Desktop/table_data.pdf")
