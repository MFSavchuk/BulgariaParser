from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import multiprocessing

from utils.compare import compare
from utils.create_lists_and_new_file_for_parser import create_lists_and_new_file_for_parser
from utils.sort_file import sort_file


class Parser(multiprocessing.Process):

    def __init__(self, statements, new_file, collector=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collector = collector  # очередь
        self.statements = statements
        self.new_file = new_file

    def run(self):
        browser = webdriver.Chrome()
        for statement in self.statements:

            browser.get('https://publicbg.mjs.bg/BgInfo/')
            input_element = browser.find_element(By.NAME, "regNum")
            input_element.send_keys(statement)
            input_element.send_keys(Keys.RETURN)
            sleep(0.1)

            html = browser.page_source
            html = " ".join(html.splitlines())

            if 'Резервиране на дата за получаване на удостоверение' in html:
                self.new_file.write(f'{statements} Указ. Запись\n')
            else:
                _, end = html.split('<div class="validation-summary-errors text-danger"><ul><li>', 1)
                result, _ = end.split('</li>', 1)
                if 'Вече сте получили удостоверение по тази преписка' in result:
                    self.new_file.write(f'{statements} Указ. Получен\n')
                elif 'Вашето удостоверение е изпратено в консулска служба' in result:
                    start, _ = result.split('. При получаване ')
                    embassy = start[52:]
                    self.new_file.write(f'{statements} Указ. Отправлено в {embassy}\n')
                else:
                    self.new_file.write(f'{statement} {result}\n')

        browser.quit()


if __name__ == '__main__':
    lists, new_file = create_lists_and_new_file_for_parser(multiproc=4)

    with open(new_file, 'a', encoding='utf8') as ff:
        for statements in lists:
            parser = Parser(statements=statements, new_file=ff)
            parser.run()
    sort_file(new_file)
    compare(file_result='compare_result.txt')

    # collector = multiprocessing.Queue()
    # parsers = [Parser(statements=statements, new_file=ff) for statements in lists]
    # for parser in parsers:
    #     parser.start()
    # for parser in parsers:
    #     parser.join()
