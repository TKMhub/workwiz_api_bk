# pdf_conversion/services/pdf_to_excel.py

import os
import tempfile
import PyPDF2
import openpyxl


def convert_pdf_to_excel(pdf_file_path):
    # PDFファイルを読み込み、テキストデータに変換
    with open(pdf_file_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfFileReader(pdf_file)
        num_pages = reader.numPages
        text_data = ''
        for page in range(num_pages):
            text_data += reader.getPage(page).extractText()

    # テキストデータをExcelファイルに変換
    excel_file = openpyxl.Workbook()
    sheet = excel_file.active
    sheet.cell(row=1, column=1).value = text_data

    # Excelファイルを一時ディレクトリに保存
    temp_dir = tempfile.mkdtemp()
    excel_file_path = os.path.join(temp_dir, 'output.xlsx')
    excel_file.save(excel_file_path)

    return excel_file_path
