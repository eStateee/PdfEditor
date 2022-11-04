from typing import AnyStr
from pdf2docx import parse
import docx
from docx2pdf import convert
from docx.shared import Pt
from constants import *


def convert_pdf_to_docx() -> AnyStr:
    _doc_file_name = 'd.docx'
    pdf_path = os.path.join(TEMPLATES_PATH, 'before.pdf')
    docx_path = os.path.join(TEMP_PATH, _doc_file_name)
    parse(pdf_path, docx_path)
    return docx_path





def redact_docx_file(doc, D):
    _pdf_path = os.path.join(TEMP_PATH, 'doc.pdf')
    # SET STYLES
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'

    # REDACT
    for i in D.keys():
        for j in doc.paragraphs:
            if j.text.find(i) >= 0:
                j.text = j.text.replace(i, '')
                runner = j.add_run(D[i])
                runner.font.size = docx.shared.Pt(36)
                runner.bold = True
                if i == 'qwe':
                    runner.underline = True
                elif i == 'asd':
                    runner.font.size = docx.shared.Pt(14)
                elif i == 'zxc':
                    runner.italic = True
    try:
        _redacted_docx_file_path = os.path.join(TEMP_PATH, 'doc.docx')
        doc.save(_redacted_docx_file_path)
        convert(_redacted_docx_file_path)  # convert docx to pdf(doc.pdf)
        return _pdf_path
    except Exception:
        return None
