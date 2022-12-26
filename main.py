import multiprocessing
from time import sleep

from utils.time_track import time_track
from utils.create_lists_and_new_file_for_parser import create_lists_and_new_file_for_parser
from utils.Parser import Parser
from utils.sort_file import sort_file
from utils.compare import compare


@time_track
def run_parser(multiproc):
    lists, new_file = create_lists_and_new_file_for_parser(multiproc=multiproc)
    collector = multiprocessing.Queue()
    parsers = [Parser(statements=statements, collector=collector) for statements in lists]
    for parser in parsers:
        parser.start()

    sleep(30)

    with open(new_file, 'a', encoding='utf8') as ff:
        while True:
            one_is_alive = any([parser.is_alive() for parser in parsers])
            # print([parser.is_alive() for parser in parsers])
            if one_is_alive:
                if not collector.empty():
                    data = str(collector.get())
                    ff.write(data)
                    print(f'Строка {data.split(" ", 1)[0]} записана')
                    # print(f'Длина очереди - {collector.qsize()} ')
                    # sleep(0.4)
            else:
                break

        print('Этап 1 пройден')
        print(f'Длина очереди - {collector.qsize()} ')

        if not collector.empty():
            data = str(collector.get())
            ff.write(data)
            print(f'Строка {data.split(" ", 1)[0]} записана')

        print('Этап 2 пройден')

    for parser in parsers:
        parser.join()

    print('Этап 3 пройден')

    sort_file(new_file)
    compare(file_result='compare_result.txt')


if __name__ == '__main__':
    run_parser(multiproc=8)
