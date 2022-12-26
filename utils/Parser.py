import multiprocessing

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class Parser(multiprocessing.Process):

    def __init__(self, statements, collector, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collector = collector  # очередь
        self.statements = statements

    def run(self):
        browser = webdriver.Chrome()
        browser.get('https://publicbg.mjs.bg/BgInfo/')
        for statement in self.statements:

            # browser.get('https://publicbg.mjs.bg/BgInfo/')
            input_element = browser.find_element(By.NAME, "regNum")
            input_element.send_keys(statement)
            input_element.send_keys(Keys.RETURN)
            # sleep(0.1)

            html = browser.page_source
            html = " ".join(html.splitlines())

            if 'Резервиране на дата за получаване на удостоверение' in html:
                self.collector.put(f'{statement} Указ. Запись\n')
                print(f'Обработан номер - {statement}')
                browser.get('https://publicbg.mjs.bg/BgInfo/')
            else:
                _, end = html.split('<div class="validation-summary-errors text-danger"><ul><li>', 1)
                result, _ = end.split('</li>', 1)
                if 'Вече сте получили удостоверение по тази преписка' in result:
                    self.collector.put(f'{statement} Указ. Получен\n')
                elif 'Вашето удостоверение е изпратено в консулска служба' in result:
                    start, _ = result.split('. При получаване ')
                    embassy = start[52:]
                    self.collector.put(f'{statement} Указ. Отправлено в {embassy}\n')
                else:
                    self.collector.put(f'{statement} {result}\n')
                print(f'Обработан номер - {statement}')

        browser.quit()
