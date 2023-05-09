import PyPDF2
import openpyxl
import os


def pdf_to_excel(pdf_file, output_file):
    # PDFファイルを読み込み
    with open(pdf_file, 'rb') as f:
        reader = PyPDF2.PdfFileReader(f)

        # Excelファイルを作成
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # PDFの各ページを読み込んでExcelに書き込む
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text = page.extract_text()
            lines = text.split('\n')

            for row, line in enumerate(lines, start=1):
                cells = line.split()
                for col, cell in enumerate(cells, start=1):
                    sheet.cell(row=row, column=col).value = cell

        # Excelファイルを保存
        workbook.save(output_file)

        # ダウンロード用にファイルパスを返す
        return os.path.abspath(output_file)
