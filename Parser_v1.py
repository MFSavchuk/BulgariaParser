from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import multiprocessing

from datetime import date


class Parser(multiprocessing.Process):

    def __init__(self, year, numbers, file_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.year = year
        self.numbers = numbers
        self.current_date = date.today()
        self.file_name = file_name

    def run(self):
        browser = webdriver.Chrome()
        browser.get('https://publicbg.mjs.bg/BgInfo/')

        for number in self.numbers:
            # browser.get('https://publicbg.mjs.bg/BgInfo/')
            # sleep(0.1)

            statement = f'{number}/{self.year}'
            input_element = browser.find_element(By.NAME, "regNum")
            input_element.send_keys(statement)
            input_element.send_keys(Keys.RETURN)
            # sleep(0.1)

            html = browser.page_source
            html = " ".join(html.splitlines())

            with open(f'{self.file_name} {self.current_date}.txt', 'a', encoding='utf8') as ff:

                if 'Резервиране на дата за получаване на удостоверение' in html:
                    ff.write(f'{statement} Указ. Запись\n')
                    # print(f'{statement} Указ. Запись')
                else:
                    _, end = html.split('<div class="validation-summary-errors text-danger"><ul><li>', 1)
                    result, _ = end.split('</li>', 1)
                    # result, _ = end.split('</li> </ul></div>')
                    if 'Вече сте получили удостоверение по тази преписка' in result:
                        ff.write(f'{statement} Указ. Получен\n')
                        # print(f'{statement} Указ. Получен')
                    elif 'Вашето удостоверение е изпратено в консулска служба' in result:
                        start, _ = result.split('. При получаване ')
                        embassy = start[52:]
                        ff.write(f'{statement} Указ. Отправлено в {embassy}\n')
                        # print(f'{statement} Указ. Отправлено в {embassy}')
                    else:
                        ff.write(f'{statement} {result}\n')

        browser.quit()


if __name__ == '__main__':

    parser1 = Parser(year=2019, numbers=range(15000, 30000), file_name='2019')  # 15000-30000
    # parser1.run()

    parser2 = Parser(year=2020, numbers=range(1, 11000), file_name='2020')  # 1-11000
    # parser2.run()

    parser3 = Parser(year=2021, numbers=range(1, 15000), file_name='2021-1')  # 1-15000
    # parser3.run()

    parser4 = Parser(year=2021, numbers=range(15001, 30000), file_name='2021-2')  # 15001-30000
    # parser4.run()

    parser5 = Parser(year=2022, numbers=range(1, 9250), file_name='2022')  # 1-9250
    # parser5.run()

    parser1.start()
    parser2.start()
    parser3.start()
    parser4.start()
    parser5.start()

    parser1.join()
    parser2.join()
    parser3.join()
    parser4.join()
    parser5.join()

# for ch in end:
#     count += 1
#     if ch == '<':
#         break
#     if count == 200:
#         result += '\n'
#         count = 0
#     result += ch


# import __future__ import print_function #Only for Python2
#
# with open('file1.txt') as f1, open('file2.txt') as f2, open('outfile.txt', 'w') as outfile:
#     for line1, line2 in zip(f1, f2):
#         if line1 == line2:
#             print(line1, end='', file=outfile)


# first_word = some_string.split(' ', 1)[0]
