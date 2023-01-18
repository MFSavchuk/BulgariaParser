import os
from collections import defaultdict
from pprint import pprint

results_test = {
    'Финальная проверка -> Положительно': 0,
    'Финальная проверка -> Доп. документы': 0,
    'Финальная проверка -> Дополнительная проверка': 0,
    'Финальная проверка -> Отказ': 0,
    'Положительно -> Указ': 0,
    'Положительно -> Отказ Вицепрезидента': 0,
    'Образувана преписка -> Финальная проверка': 0,
    'Образувана преписка -> Доп. документы': 0,

}


def compare(file_result):
    statuses = {
        'Молбата Ви е одобрена от Съвета по гражданството. Следва да се освободите от досегашното си гражданство': 0,
        'Указ': 0,
        # 'Указ. Получен': 0,
        # 'Указ. Отправлено': 0,
        # 'Указ. Запись': 0,
        'е прекратена със заповед': 0,
        'Преписката Ви е разгледана от Съвета по гражданството и е взето решение да бъде прекратена': 0,
        'Отказ на Вицепрезидента на Република България': 0,
        'Съветът по гражданство не е уважил молбата': 0,
        'Молбата ви е разгледана от Съвета по гражданство с положително становище': 0,
        'Преписката е разгледана от Съвета по гражданството. Извадена е за допълнителна проверка': 0,
        'Преписката е нередовна. Необходимо е представяне на допълнителни документи': 0,
        'По преписката Ви предстои да бъде извършен финален експертен преглед преди да бъде разгледана от Съвета по гражданство': 0,
        'Образувана преписка': 0,
    }

    filepaths = [os.path.join(dirpath, file) for dirpath, dirnames, filenames in os.walk('01_data') for file in
                 filenames]
    statements = defaultdict(lambda: [])

    with open(filepaths[-2], 'r', encoding='utf8') as f1, open(filepaths[-1], 'r', encoding='utf8') as f2:

        my_statement = '11074/2021'
        my_count_final = 0
        my_count_additional_documents = 0
        my_count_positive = 0
        was_my_statements = False

        for line1, line2 in zip(f1, f2):

            statement = line2.split(' ', 1)[0]
            line1 = line1.strip()
            line2 = line2.strip()

            if not was_my_statements:
                if my_statement in statement:
                    was_my_statements = True
                elif 'По преписката Ви предстои да бъде извършен финален експертен преглед преди да бъде разгледана от Съвета по гражданство' in line2:
                    my_count_final += 1
                elif 'Преписката е нередовна. Необходимо е представяне на допълнителни документи' in line2:
                    my_count_additional_documents += 1
                elif 'Молбата ви е разгледана от Съвета по гражданство с положително становище' in line2:
                    my_count_positive += 1

            if line1 != line2:
                if 'Указ' in line2 or 'Молбата Ви е одобрена от Съвета по гражданството' in line2:
                    statements['1.Указ'].append(statement)
                elif 'Молбата ви е разгледана от Съвета по гражданство с положително становище' in line2:
                    statements['2.Положительно'].append(statement)
                elif 'Преписката е разгледана от Съвета по гражданството. Извадена е за допълнителна проверка' in line2:
                    statements['3.Доп. проверка'].append(statement)
                elif 'Преписката е нередовна. Необходимо е представяне на допълнителни документи' in line2:
                    statements['4.Доп. документы'].append(statement)
                elif 'По преписката Ви предстои да бъде извършен финален експертен преглед преди да бъде разгледана от Съвета по гражданство' in line2:
                    statements['5.Финальная проверка'].append(statement)
                elif 'Образувана преписка' in line2:
                    statements['6.Образувана преписка'].append(statement)
                elif 'е прекратена със заповед' in line2:
                    statements['7.Прекращено приказом'].append(statement)
                elif 'Преписката Ви е разгледана от Съвета по гражданството и е взето решение да бъде прекратена' in line2 or 'Съветът по гражданство не е уважил молбата' in line2:
                    statements['8.Совет по гражданству прекратил/не удовлетворил ходатайство'].append(statement)
                elif 'Отказ на Вицепрезидента на Република България' in line2:
                    statements['9.Отказ Вицепрезидента'].append(statement)
                else:
                    print(line2)
        tuple_statements = sorted(statements.items(), key=lambda x: x[0])

    with open(filepaths[-1], 'r', encoding='utf8') as f1:
        for line in f1:
            for status, value in statuses.items():
                if status in line:
                    statuses[status] += 1
    pprint(statuses)

    file_old = filepaths[-2].split('\\', 1)[1]
    file_new = filepaths[-1].split('\\', 1)[1]

    all_count_final = statuses[
        "По преписката Ви предстои да бъде извършен финален експертен преглед преди да бъде разгледана от Съвета по гражданство"]
    all_count_additional_documents = statuses[
        "Преписката е нередовна. Необходимо е представяне на допълнителни документи"]
    all_count_positive = statuses[
        "Молбата ви е разгледана от Съвета по гражданство с положително становище"]

    after_my_count_final = all_count_final - my_count_final
    after_my__count_additional_documents = all_count_additional_documents - my_count_additional_documents
    after_my_count_positive = all_count_positive - my_count_positive

    with open(f'02_result\\{file_result}', 'a', encoding='utf8') as ff:
        ff.write('---------------------------------------------------------------------------------------------------------------------------------------\n')
        print('---------------------------------------------------------------------------------------------------------------------------------------')
        ff.write(f'Преписки подадени по консулски път. Сравнение {file_new[:-4]} с {file_old[:-4]}\n')
        print(f'Преписки подадени по консулски път. Сравнение {file_new[:-4]} с {file_old[:-4]}')
        ff.write('\n')
        print('---------------------------------------------------------------------------------------------------------------------------------------')

        for key, values in tuple_statements:
            count = 0
            for _ in values:
                count += 1
            ff.write(f'{key} ({count} человек) - {values}\n')
            print(f'{key} ({count} человек) - {values}')

        ff.write('\n')
        print('---------------------------------------------------------------------------------------------------------------------------------------')

        ff.write(
            f'"Положительно": до - {my_count_positive}, после - {after_my_count_positive}, всего - {all_count_positive}\n')
        print(
            f'"Положительно": до - {my_count_positive}, после - {after_my_count_positive}, всего - {all_count_positive}')

        ff.write(
            f'"Финальная проверка": до -  {my_count_final}, после - {after_my_count_final}, всего - {all_count_final}\n')
        print(
            f'"Финальная проверка": до - {my_count_final}, после - {after_my_count_final}, всего - {all_count_final}')

        ff.write(
            f'"Переписка нерегулярная. Необходимо представить дополнительные документы": до - {my_count_additional_documents}, после - {after_my__count_additional_documents}, всего - {all_count_additional_documents}\n')
        print(
            f'"Переписка нерегулярная. Необходимо представить дополнительные документы": до - {my_count_additional_documents}, после - {after_my__count_additional_documents}, всего - {all_count_additional_documents}')

        print('---------------------------------------------------------------------------------------------------------------------------------------')


# compare(file_result='compare_result.txt')
# compare(file_result='compare_result_test.txt')
