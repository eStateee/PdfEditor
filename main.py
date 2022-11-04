import PySimpleGUI as sg
from typing import AnyStr
from PyPDF2 import PdfReader,  PdfMerger
import docx
### Local imports
from services import get_company_info, get_meta, add_meta, clear_temp_folder
from pdf_services import convert_pdf_to_docx, redact_docx_file

from constants import *

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


def change_before_pdf_file(values, descr_type) -> AnyStr:

    name = values['-PROD_NAME-']
    global_prod_name = values['-GLOBAL_NAME1-']
    _D = {
        'qwe': name,
        'asd': global_prod_name.upper(),
        'zxc': descr_type.upper(),
    }
    docx_path = convert_pdf_to_docx()  # path to docx file
    docx_document = docx.Document(docx_path)  # docx Entity
    try:
        _redacted_pdf_file_path = redact_docx_file(docx_document, _D)
        return _redacted_pdf_file_path
    except Exception:
        print('Oops... Some exception:(')


def add_contacts(file_path, descr_type, values,filename) -> None:
    merger = PdfMerger()
    original_pdf_file = open(os.path.join(file_path), 'rb')
    redacted_pdf_file_path = change_before_pdf_file(values=values, descr_type=descr_type)
    before = open(os.path.join(redacted_pdf_file_path), 'rb')
    after = open(os.path.join(TEMPLATES_PATH, 'after.pdf'), 'rb')
    merger.append(original_pdf_file)
    merger.merge(position=0, fileobj=before, pages=(0, 1))
    merger.append(after)
    output = open(os.path.join(READY_PATH,filename), "wb")
    merger.write(output)
    merger.close()
    output.close()


def main():
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
        # Add company contacts(before.pdf, after.pdf)
        add_contacts(file_path=file_path, descr_type=descr_type, values=values,filename=filename)

        # add meta_data and create writer object
        reader = PdfReader(os.path.join(READY_PATH, filename))
        ready_writer = add_meta(reader=reader, author=company_info[1], meta=meta_data)

        with open(os.path.join(READY_PATH, filename), "wb") as file:
            ready_writer.write(file)

        print(f'Файл {filename} Успешно изменен')
        clear_temp_folder()
    window.close()


if __name__ == '__main__':
    main()
