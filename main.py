import logging
import PySimpleGUI as sg
from services.pdf_services import add_contacts, add_meta, write_new_pdf_file
from services.service import get_company_info, get_meta, clear_temp_folder
from constants import TOOLTIP
from tqdm import tqdm
from functools import partialmethod
from loguru import logger

sg.theme('Dark')
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
    logger.add("logs/log.log", encoding='utf-8',
               format="{time:DD-MM-YYYY HH:mm:ss} | <level>{level: <8}</level> | {file} | {function} | {message}",
               retention="5 days", level='DEBUG')
    window = sg.Window('PdfEditor', layout)
    company_info = get_company_info()
    logger.info('.csv data received')
    while True:  # The Event Loop
        logger.debug('Session start')
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break
        file_path = values['-FILE-']
        filename = values['-FILE-'].split('/')[-1]
        logger.info(f'Receive file {file_path}')

        # Get meta data and descr type
        meta_data, descr_type = get_meta(values=values, company_info=company_info)
        logger.info('Receive ready meta_data and description type(descr_type)')

        # Add company contacts(before.pdf, after.pdf)
        add_contacts(file_path=file_path, descr_type=descr_type, values=values, filename=filename)
        logger.info('Company contacts successfully added')

        # add meta_data and create writer object
        ready_writer = add_meta(filename=filename, author=company_info[1], meta=meta_data)
        logger.info('Get ready writer object')

        write_new_pdf_file(filename=filename, writer=ready_writer)
        logger.info('Create new ready .pdf file')
        # Clear temp folder after creating ready pdf file
        clear_temp_folder()
        logger.info('Temp folder cleared')

        logger.info('New PDF file created Successfully')
        logger.debug('Session end')
    window.close()
    logger.debug('Session end(App exited)')


if __name__ == '__main__':
    main()
