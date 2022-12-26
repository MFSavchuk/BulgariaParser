import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import multiprocessing

from datetime import date


class Parser(multiprocessing.Process):

    def __init__(self, statement, file_name, browser, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.statement = statement
        self.file = file_name
        self.browser = browser

    def run(self):
        self.browser.get('https://publicbg.mjs.bg/BgInfo/')
        input_element = browser.find_element(By.NAME, "regNum")
        input_element.send_keys(self.statement)
        input_element.send_keys(Keys.RETURN)
        # sleep(0.1)

        html = self.browser.page_source
        html = " ".join(html.splitlines())

        if 'Резервиране на дата за получаване на удостоверение' in html:
            self.file.write(f'{self.statement} Указ. Запись\n')
            # print(f'{self.statement} Указ. Запись')
        else:
            _, end = html.split('<div class="validation-summary-errors text-danger"><ul><li>', 1)
            result, _ = end.split('</li>', 1)
            if 'Вече сте получили удостоверение по тази преписка' in result:
                self.file.write(f'{self.statement} Указ. Получен\n')
                # print(f'{self.statement} Указ. Получен')
            elif 'Вашето удостоверение е изпратено в консулска служба' in result:
                start, _ = result.split('. При получаване ')
                embassy = start[52:]
                self.file.write(f'{self.statement} Указ. Отправлено в {embassy}\n')
                # print(f'{self.statement} Указ. Отправлено в {embassy}')
            else:
                self.file.write(f'{self.statement} {result}\n')


def check_line(line_for_check, file_name):
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
            print(f'Не проверяется - "{line_for_check.strip()}"', flush=True)
            return False
    else:
        return True


if __name__ == '__main__':
    current_date = date.today()
    new_file = f'01_data/{current_date}.txt'

    filepaths = [os.path.join(dirpath, file) for dirpath, dirnames, filenames in os.walk('../01_data') for file in
                 filenames]

    with open(filepaths[-1], 'r', encoding='utf8') as ff1, open(new_file, 'a+', encoding='utf8') as ff2:
        browser = webdriver.Chrome()
        for line in ff1:
            if check_line(line_for_check=line, file_name=ff2):
                statement = line.split(' ', 1)[0]
                parser = Parser(statement=statement, file_name=ff2, browser=browser)
                parser.run()

        browser.quit()

# parser1 = Parser(year=2019, numbers=range(15000, 30000), file_name='2019')  # 15000-30000
# # parser1.run()
#
# parser2 = Parser(year=2020, numbers=range(1, 11000), file_name='2020')  # 1-11000
# # parser2.run()
#
# parser3 = Parser(year=2021, numbers=range(1, 15000), file_name='2021-1')  # 1-15000
# # parser3.run()
#
# parser4 = Parser(year=2021, numbers=range(15001, 30000), file_name='2021-2')  # 15001-30000
# # parser4.run()
#
# parser5 = Parser(year=2022, numbers=range(1, 9250), file_name='2022')  # 1-9250
# # parser5.run()
#
# parser1.start()
# parser2.start()
# parser3.start()
# parser4.start()
# parser5.start()
#
# parser1.join()
# parser2.join()
# parser3.join()
# parser4.join()
# parser5.join()


