import os
from datetime import date
import numpy as np


def create_lists_and_new_file_for_parser(multiproc):
    current_date = date.today()
    new_file = f'01_data/{current_date}.txt'
    list_statements = []
    filepaths = [os.path.join(dirpath, file) for dirpath, dirnames, filenames in os.walk('01_data') for file in
                 filenames]

    if not os.path.exists(new_file):
        previous_file = filepaths[-1]
        with open(previous_file, 'r', encoding='utf8') as ff_read, open(new_file, 'w', encoding='utf8') as ff_write:
            for line in ff_read:
                if _check_line(line_for_check=line, file_name=ff_write):
                    statement = line.split(" ", 1)[0]
                    list_statements.append(statement)
        list_statements = _chunked_list(lists=list_statements, multiproc=multiproc)
        return list_statements, new_file
    else:
        previous_file = filepaths[-2]
        raise ValueError(f'\nФайл {new_file} существует. Удалите перед запуском\n')


def _chunked_list(lists, multiproc):
    our_array = np.array(lists)
    chunked_arrays = np.array_split(our_array, multiproc)
    lists = [list(array) for array in chunked_arrays]
    return lists


def _check_line(line_for_check, file_name):
    final_statuses = [
        'Молбата Ви е одобрена от Съвета по гражданството. Следва да се освободите от досегашното си гражданство',
        'Указ. Получен',
        'Указ. Отправлено',
        'Указ. Запись',
        'е прекратена със заповед',
        'Преписката Ви е разгледана от Съвета по гражданството и е взето решение да бъде прекратена',
        'Отказ на Вицепрезидента на Република България',
        'Съветът по гражданство не е уважил молбата'
    ]

    for final_status in final_statuses:
        if final_status in line_for_check:
            file_name.write(line_for_check)
            # print(f'Не проверяется. Добавлена строка - {line_for_check.strip()}', flush=True)
            return False
    else:
        return True

# try:
#     lists_statement, new_file = create_lists_and_new_file_for_parser(multiprocessing=3)
#     for list_statement in lists_statement:
#         print(list_statement)
#         print(len(list_statement))
# except Exception as exc:
#     print(exc)
