from typing import List, AnyStr

from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import csv
import time

# CONSTANTS
COMMON_META = 'MAIN_PROD_NAME || COMPANY-NAME_ENG. DESCR_TYPE на PROD-TYPE SUB1_PROD_NAME. Описание на PROD2TYPE' \
              'SUB2_PROD_NAME. Продажа оборудования производства завод-изготовитель COMPANY-NAME_RUS, производитель ' \
              'COUNTRY. Дилер ГКНТ. Поставка Россия и СНГ. '

PASSPORT_META = 'MAIN_PROD_NAME || COMPANY-NAME_ENG. Паспорт на PROD-TYPE SUB1_PROD_NAME. Техническое описание на PROD2TYPE SUB2_PROD_NAME. Продажа оборудования ' \
                'производства завод-изготовитель COMPANY-NAME_RUS, производитель COUNTRY. Дилер ГКНТ. Поставка ' \
                'Россия и СНГ. '


def get_company_info() -> List:
    res = []
    with open('company_info.csv', encoding='utf-8') as file_obj:
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


def get_passport_meta(company_name_eng, company_name_rus, company_country, prod_name, sub_name1,
                      global_prod_name, global_prod_name2, sub_name2__optional) -> AnyStr:
    _temp = PASSPORT_META.replace('MAIN_PROD_NAME', prod_name).replace('COMPANY-NAME_ENG', company_name_eng).replace(
        'PROD-TYPE',
        global_prod_name).replace(
        'SUB1_PROD_NAME', sub_name1).replace('PROD2TYPE', global_prod_name2).replace('SUB2_PROD_NAME',
                                                                                     sub_name2__optional).replace(
        'COMPANY-NAME_RUS', company_name_rus).replace('COUNTRY',
                                                      company_country)
    return _temp


def add_contacts(filename) -> None:
    merger = PdfMerger()
    main = open(f'{filename}.pdf', 'rb')
    before = open('before.pdf', 'rb')
    after = open('after.pdf', 'rb')
    merger.append(main)
    merger.merge(position=0, fileobj=before, pages=(0, 1))
    merger.append(after)
    output = open(f"{filename}.pdf", "wb")
    merger.write(output)
    merger.close()
    output.close()


def get_description(descr_name) -> AnyStr:
    if descr_name in ('Т', 'т', 't', 'T'):
        return 'технические характеристики'
    elif descr_name in ('О', 'о'):
        return 'описание'
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


# USER INPUT
filename = input('Название файла: ')
meta_type = input('Тип метаданных (1-паспорт, Enter-обычный): ')
prod_name = input('Введи название товара: ')
sub_name1 = input('Введи 1 доп название: ')
global_prod_name = input('Введи общее название товара: ')
company_info = get_company_info()
company_name = company_info[0].split(' ')
global_prod_name2 = input('Введи 2-е общее название товара: ').lower()
sub_name2 = input('Введи 2 доп название(optional): ').lower()
sub_name2 = ' ' + sub_name2
if meta_type == '1':
    meta_data = get_passport_meta(company_name_eng=company_name[0], company_name_rus=company_name[1],
                                  company_country=company_info[2], prod_name=prod_name, sub_name1=sub_name1,
                                  global_prod_name=global_prod_name, global_prod_name2=global_prod_name2,
                                  sub_name2__optional=sub_name2)
else:
    descr_type = input('Введи тип описания(т-тех.характеристики | о-описание): ')
    descr_type = get_description(descr_name=descr_type).capitalize()

    meta_data = get_common_meta(company_name_eng=company_name[0], company_name_rus=company_name[1],
                                company_country=company_info[2], prod_name=prod_name, sub_name1=sub_name1,
                                sub_name2__optional=sub_name2, descr_type=descr_type, global_prod_name=global_prod_name,
                                global_prod_name2=global_prod_name2)

# Add company contacts
add_contacts(filename=filename)

reader = PdfReader(f'{filename}.pdf')
writer = PdfWriter()

ready_writer = add_meta(reader=reader, writer=writer, author=company_info[1], meta=meta_data)

with open(f"{filename}.pdf", "wb") as file:
    ready_writer.write(file)
print('Успешно')
time.sleep(2)
