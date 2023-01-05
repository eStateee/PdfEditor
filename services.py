from typing import List, AnyStr
import csv
from constants import COMMON_META, TEMPLATES_PATH, TEMP_PATH
import os
from loguru import logger


@logger.catch(message='An error in receiving data from .csv file')
def get_company_info() -> List:
    res = []
    with open(os.path.join(TEMPLATES_PATH, 'company_info.csv'), encoding='utf-8') as file_obj:
        reader_obj = csv.reader(file_obj)

        for row in reader_obj:
            res.append(' '.join(row))

    return res


company_info = get_company_info()
company_name = company_info[0].split('^^')

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


@logger.catch(message='An error occurred in get_meta ')
def get_meta(values, company_info) -> (AnyStr, AnyStr):
    _types = {
        'Т': ('Технические характеристики', 'Описание', 'тех. характеристики'),
        'О': ('Описание', 'Характеристики', 'Описание'),
        'П': ('Паспорт', 'Описание', 'Паспорт'),
        'СИ': ('Описание типа средства измерений', 'Характеристики', 'Описание типа средства измерений'),
        'РП': ('Руководство по эксплуатации', 'Описание', 'Руководство по эксплуатации'),
        'ИП': ('Инструкция по эксплуатации', 'Описание', 'Инструкция по эксплуатации'),
    }

    descr_type = values['-DESCR-'].upper()
    prod_name = values['-PROD_NAME-'].strip()
    sub_name1 = values['-PROD_NAME1-'].strip()
    sub_name2 = ' ' + values['-PROD_NAME2-'].strip()
    global_prod_name = values['-GLOBAL_NAME1-'].lower().strip()
    global_prod_name2 = values['-GLOBAL_NAME2-'].lower().strip()
    if descr_type in _types.keys():
        tech = _types[descr_type]
    else:
        tech = (descr_type, 'Описание')
    _meta = get_common_meta(company_name_eng=company_name[0], company_name_rus=company_name[1],
                            company_country=company_info[2], prod_name=prod_name, sub_name1=sub_name1,
                            sub_name2__optional=sub_name2, descr_type=tech[0], global_prod_name=global_prod_name,
                            global_prod_name2=global_prod_name2, tech=tech[1])
    try:
        return _meta, tech[2]
    except Exception:
        return _meta, tech[0]


@logger.catch(message='An error in cleaning temp folder')
def clear_temp_folder():
    for i in os.listdir(TEMP_PATH):
        p = os.path.join(TEMP_PATH, i)
        os.remove(p)
