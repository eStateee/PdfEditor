import logging
import PySimpleGUI as sg
from pdf_services import add_contacts, add_meta, write_new_pdf_file
from services import get_company_info, get_meta, clear_temp_folder
from constants import TOOLTIP
from tqdm import tqdm
from functools import partialmethod

layout = [
    [sg.Text('Файл:', font='Verdano'), sg.InputText(key='-FILE-', do_not_clear=False, font=20),
     sg.FileBrowse(file_types=(("Pdf Files", "*.pdf"),), s=13, button_color='green', button_text='Выбрать файл',
                   auto_size_button=True)],
    [sg.Text('')],

    [sg.Text('Тип описания: ', font='Verdano'),
     sg.InputText(key='-DESCR-', do_not_clear=False, s=30, font=20, tooltip=TOOLTIP)],
    [sg.Text('Название продукта: ', font='Verdano'),
     sg.InputText(key='-PROD_NAME-', do_not_clear=False, s=76, font=20)],
    [sg.Text('1-е доп название продукта:', font='Verdano'),
     sg.InputText(key='-PROD_NAME1-', do_not_clear=False, s=70, font=20)],
    [sg.Text('2-е доп название продукта(optional): ', font='Verdano'),
     sg.InputText(key='-PROD_NAME2-', do_not_clear=False, s=62, font=20)],
    [sg.Text('1-е название категории: ', font='Verdano'), sg.InputText(key='-GLOBAL_NAME1-', s=30, font=20)],
    [sg.Text('2-е название категории: ', font='Verdano'), sg.InputText(key='-GLOBAL_NAME2-', s=30, font=20)],
    [sg.Output(size=(100, 12), font=50)],
    [sg.Submit(s=20, button_color='green'), sg.Exit(s=15, button_color="tomato")]
]


def main():
    logging.disable(logging.CRITICAL)
    tqdm.__init__ = partialmethod(tqdm.__init__, disable=True)
    window = sg.Window('PdfEditor', layout)
    company_info = get_company_info()
    while True:  # The Event Loop
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break
        file_path = values['-FILE-']
        filename = values['-FILE-'].split('/')[-1]
        meta_data, descr_type = get_meta(values=values, company_info=company_info)
        # Add company contacts(before.pdf, after.pdf)
        add_contacts(file_path=file_path, descr_type=descr_type, values=values, filename=filename)

        # add meta_data and create writer object
        ready_writer = add_meta(filename=filename, author=company_info[1], meta=meta_data)
        write_new_pdf_file(filename=filename, writer=ready_writer)

        clear_temp_folder()
    window.close()


if __name__ == '__main__':
    main()
