import PySimpleGUI as sg
from typing import List, AnyStr
import os
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import csv
###
from pdf2docx import parse
import docx
from docx2pdf import convert
from docx.shared import Pt

# CONSTANTS
COMMON_META = 'MAIN_PROD_NAME || COMPANY-NAME_ENG. DESCR_TYPE на PROD-TYPE SUB1_PROD_NAME. TECH-TYPE на PROD2TYPE' \
              'SUB2_PROD_NAME. Продажа оборудования производства завод-изготовитель COMPANY-NAME_RUS, производитель ' \
              'COUNTRY. Дилер ГКНТ. Поставка Россия и СНГ. '

READY_PATH = os.path.join(os.path.abspath(os.curdir), 'res')
TEMP_PATH = os.path.join(os.path.abspath(os.curdir), 'temp')
START_PATH = os.path.join(os.path.abspath(os.curdir), 'start')
TEMPLATES_PATH = os.path.join(os.path.abspath(os.curdir), 'templates')


def get_company_info() -> List:
    res = []
    with open(os.path.join(TEMPLATES_PATH, 'company_info.csv'), encoding='utf-8') as file_obj:
        reader_obj = csv.reader(file_obj)

        for row in reader_obj:
            res.append(' '.join(row))
    return res


def get_common_meta(company_name_eng, company_name_rus, company_country, prod_name, sub_name1, sub_name2__optional,
                    descr_type,
                    global_prod_name, global_prod_name2, tech) -> AnyStr:
    _temp = COMMON_META.replace('MAIN_PROD_NAME', prod_name).replace('COMPANY-NAME_ENG', company_name_eng).replace(
        'DESCR_TYPE',
        descr_type).replace(
        'PROD-TYPE', global_prod_name).replace('SUB1_PROD_NAME', sub_name1).replace('TECH-TYPE', tech).replace(
        'PROD2TYPE',
        global_prod_name2).replace(
        'SUB2_PROD_NAME', sub_name2__optional).replace('COMPANY-NAME_RUS', company_name_rus).replace('COUNTRY',
                                                                                                     company_country)
    return _temp


def convert_pdf_to_docx() -> AnyStr:
    _doc_file_name = 'd.docx'
    pdf_file = os.path.join(TEMPLATES_PATH, 'before.pdf')
    docx_file = os.path.join(TEMP_PATH, _doc_file_name)
    parse(pdf_file, docx_file)
    return docx_file


def redact_docx_file(doc, D):
    _pdf_file_name = os.path.join(TEMP_PATH, 't_before.pdf')
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
        _new_d = os.path.join(TEMP_PATH, 'new_d.docx')
        doc.save(_new_d)
        convert(_new_d, _pdf_file_name)
        return _pdf_file_name
    except Exception:
        return None


def change_before_pdf_file(values, descr_type) -> AnyStr:
    name = values['-PROD_NAME-']
    global_prod_name = values['-GLOBAL_NAME1-']
    _D = {
        'qwe': name,
        'asd': global_prod_name.upper(),
        'zxc': descr_type.upper(),
    }
    _doc_file_name = convert_pdf_to_docx()
    _doc = docx.Document(_doc_file_name)
    try:
        _pdf_file = redact_docx_file(_doc, _D)
        return _pdf_file
    except Exception:
        print('Oooops... Some exception:(')


def add_contacts(file_path, descr_type, values) -> None:
    merger = PdfMerger()
    main = open(os.path.join(file_path), 'rb')
    _b = change_before_pdf_file(values=values, descr_type=descr_type)
    before = open(os.path.join(_b['output']), 'rb')
    # TODO Change before.pdf
    after = open(os.path.join(TEMPLATES_PATH, 'after.pdf'), 'rb')
    merger.append(main)
    merger.merge(position=0, fileobj=before, pages=(0, 1))
    merger.append(after)
    output = open(os.path.join(file_path), "wb")
    merger.write(output)
    merger.close()
    output.close()


def get_meta(values, company_info) -> (AnyStr, AnyStr):
    _types = {
        'Т': ('Технические характеристики', 'Описание'),
        'О': ('Описание', 'Характеристики'),
        'П': ('Паспорт', 'Описание'),
        'СИ': ('Описание типа средства измерений', 'Характеристики'),
        'РП': ('Руководство по эксплуатации', 'Описание'),
        'ИП': ('Инструкция по эксплуатации', 'Описание'),
    }

    descr_type = values['-DESCR-'].upper()
    prod_name = values['-PROD_NAME-']
    sub_name1 = values['-PROD_NAME1-']
    sub_name2 = ' ' + values['-PROD_NAME2-'].lower()
    global_prod_name = values['-GLOBAL_NAME1-'].lower()
    global_prod_name2 = values['-GLOBAL_NAME2-'].lower()
    if descr_type in _types.keys():
        tech = _types[descr_type]
    else:
        tech = (descr_type, 'Описание')
    _meta = get_common_meta(company_name_eng=company_name[0], company_name_rus=company_name[1],
                            company_country=company_info[2], prod_name=prod_name, sub_name1=sub_name1,
                            sub_name2__optional=sub_name2, descr_type=tech[0], global_prod_name=global_prod_name,
                            global_prod_name2=global_prod_name2, tech=tech[1])

    return _meta, tech[0]


def add_meta(reader, writer, author, meta) -> PdfWriter:
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata(
        {
            "/Author": author,
            "/Producer": "",
            '/Subject': meta,
            '/Title': meta
        }
    )
    return writer


layout = [
    [sg.Text('Файл:', font='Verdano'), sg.InputText(key='-FILE-', do_not_clear=False),
     sg.FileBrowse(file_types=(("Pdf Files", "*.pdf"),), s=13, button_color='green', button_text='Выбрать файл',
                   auto_size_button=True)],
    [sg.Text('')],
    [sg.Text(
        'Т-Тех. характеристики | О-Описание | П-Паспорт\nСИ-Описание типа средства измерений\nРП-Руководство | ИП-Инструкция',
        font='Verdano', text_color='yellow')],
    [sg.Text('Тип описания: ', font='Verdano'), sg.InputText(key='-DESCR-', do_not_clear=False)],
    [sg.Text('Название продукта: ', font='Verdano'), sg.InputText(key='-PROD_NAME-', do_not_clear=False)],
    [sg.Text('1-е доп название продукта: ', font='Verdano'), sg.InputText(key='-PROD_NAME1-', do_not_clear=False)],
    [sg.Text('2-е доп название продукта(optional): ', font='Verdano'),
     sg.InputText(key='-PROD_NAME2-', do_not_clear=False)],
    [sg.Text('1-е название категории: ', font='Verdano'), sg.InputText(key='-GLOBAL_NAME1-', do_not_clear=False)],
    [sg.Text('2-е название категории: ', font='Verdano'), sg.InputText(key='-GLOBAL_NAME2-', do_not_clear=False)],
    [sg.Output(size=(80, 10))],
    [sg.Submit(s=20, button_color='green'), sg.Exit(s=15, button_color="tomato")]
]
window = sg.Window('PdfEditor', layout)
company_info = get_company_info()
company_name = company_info[0].split(' ')

while True:  # The Event Loop
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break

    file_path = values['-FILE-']
    filename = values['-FILE-'].split('/')[-1]

    meta_data, descr_type = get_meta(values=values, company_info=company_info)

    # Add company contacts
    add_contacts(file_path=file_path, descr_type=descr_type, values=values)

    reader = PdfReader(os.path.join(file_path))
    writer = PdfWriter()

    ready_writer = add_meta(reader=reader, writer=writer, author=company_info[1], meta=meta_data)

    with open(os.path.join(READY_PATH, filename), "wb") as file:
        ready_writer.write(file)
    print(f'Файл {filename} Успешно изменен')
window.close()
