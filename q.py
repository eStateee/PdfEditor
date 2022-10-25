import PySimpleGUI as sg
from typing import List, AnyStr
import os
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import csv

# CONSTANTS
COMMON_META = 'MAIN_PROD_NAME || COMPANY-NAME_ENG. DESCR_TYPE на PROD-TYPE SUB1_PROD_NAME. Описание на PROD2TYPE' \
              'SUB2_PROD_NAME. Продажа оборудования производства завод-изготовитель COMPANY-NAME_RUS, производитель ' \
              'COUNTRY. Дилер ГКНТ. Поставка Россия и СНГ. '

READY_PATH = os.path.join(os.path.abspath(os.curdir), 'res')
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
                    global_prod_name, global_prod_name2) -> AnyStr:
    _temp = COMMON_META.replace('MAIN_PROD_NAME', prod_name).replace('COMPANY-NAME_ENG', company_name_eng).replace(
        'DESCR_TYPE',
        descr_type).replace(
        'PROD-TYPE', global_prod_name).replace('SUB1_PROD_NAME', sub_name1).replace('PROD2TYPE',
                                                                                    global_prod_name2).replace(
        'SUB2_PROD_NAME', sub_name2__optional).replace('COMPANY-NAME_RUS', company_name_rus).replace('COUNTRY',
                                                                                                     company_country)
    return _temp


def add_contacts(filename) -> None:
    merger = PdfMerger()
    main = open(os.path.join(START_PATH, filename), 'rb')
    before = open(os.path.join(TEMPLATES_PATH, 'before.pdf'), 'rb')
    after = open(os.path.join(TEMPLATES_PATH, 'after.pdf'), 'rb')
    merger.append(main)
    merger.merge(position=0, fileobj=before, pages=(0, 1))
    merger.append(after)
    output = open(os.path.join(START_PATH, filename), "wb")
    merger.write(output)
    merger.close()
    output.close()


def get_description(descr_name) -> AnyStr:
    if descr_name in ('T', 'Т'):
        return 'технические характеристики'
    elif descr_name in ('О', 'о'):
        return 'техническое описание'
    elif descr_name in ('П', 'P'):
        return 'паспорт'
    else:
        return descr_name


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
    [sg.Text('Файл:'), sg.InputText(key='-FILE-', do_not_clear=False),
     sg.FileBrowse(file_types=(("Pdf Files", "*.pdf"),), s=13, button_color='green', button_text='Выбрать файл')],
    [sg.Text('')],
    [sg.Text('Т-Тех. характеристики | О-Техническое описание | П-Паспорт', font='Verdano', text_color='yellow')],
    [sg.Text('Тип описания: '), sg.InputText(key='-DESCR-', do_not_clear=False)],
    [sg.Text('Название продукта: '), sg.InputText(key='-PROD_NAME-', do_not_clear=False)],
    [sg.Text('1-е доп название продукта: '), sg.InputText(key='-PROD_NAME1-', do_not_clear=False)],
    [sg.Text('2-е доп название продукта(optional): '), sg.InputText(key='-PROD_NAME2-', do_not_clear=False)],
    [sg.Text('1-е общее название товара: '), sg.InputText(key='-GLOBAL_NAME1-', do_not_clear=False)],
    [sg.Text('2-е доп название товара: '), sg.InputText(key='-GLOBAL_NAME2-', do_not_clear=False)],
    [sg.Output(size=(80, 10))],
    [sg.Submit(s=20, button_color='green'), sg.Exit(s=15, button_color="tomato")]
]
window = sg.Window('PdfEditor', layout)
company_info = get_company_info()
company_name = company_info[0].split(' ')
while True:  # The Event Loop

    event, values = window.read()
    filename = values['-FILE-'].split('/')[-1]
    descr_type = get_description(descr_name=values['-DESCR-']).capitalize()
    prod_name = values['-PROD_NAME-']
    sub_name1 = values['-PROD_NAME1-']
    sub_name2 = ' ' + values['-PROD_NAME2-'].lower()
    global_prod_name = values['-GLOBAL_NAME1-'].lower()
    global_prod_name2 = values['-GLOBAL_NAME2-'].lower()

    meta_data = get_common_meta(company_name_eng=company_name[0], company_name_rus=company_name[1],
                                company_country=company_info[2], prod_name=prod_name, sub_name1=sub_name1,
                                sub_name2__optional=sub_name2, descr_type=descr_type, global_prod_name=global_prod_name,
                                global_prod_name2=global_prod_name2)

    # Add company contacts
    add_contacts(filename=filename)

    reader = PdfReader(os.path.join(START_PATH, filename))
    writer = PdfWriter()

    ready_writer = add_meta(reader=reader, writer=writer, author=company_info[1], meta=meta_data)

    with open(os.path.join(READY_PATH, filename), "wb") as file:
        ready_writer.write(file)
    print(f'Файл {filename} Успешно изменен')

    if event in (None, 'Exit', 'Cancel'):
        break
window.close()
