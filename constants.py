import os
COMMON_META = 'MAIN_PROD_NAME || COMPANY-NAME_ENG. DESCR_TYPE на PROD-TYPE SUB1_PROD_NAME. TECH-TYPE на PROD2TYPE' \
              'SUB2_PROD_NAME. Продажа оборудования производства завод-изготовитель COMPANY-NAME_RUS, производитель ' \
              'COUNTRY. Дилер ГКНТ. Поставка Россия и СНГ. '

READY_PATH = os.path.join(os.path.abspath(os.curdir), 'res')
TEMP_PATH = os.path.join(os.path.abspath(os.curdir), 'temp')
START_PATH = os.path.join(os.path.abspath(os.curdir), 'start')
TEMPLATES_PATH = os.path.join(os.path.abspath(os.curdir), 'templates')