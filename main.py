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
        sleep(0.5)
        parser.start()

    sleep(30)

    with open(new_file, 'a', encoding='utf8') as ff:
        while any([parser.is_alive() for parser in parsers]):
            # one_is_alive = any([parser.is_alive() for parser in parsers])
            # if one_is_alive:
            if not collector.empty():
                data = str(collector.get())
                ff.write(data)
                print(f'Строка {data.split(" ", 1)[0]} записана')
            # else:
            #     break

        print(f'В очереди - {collector.qsize()} ')

        if not collector.empty():
            data = str(collector.get())
            ff.write(data)
            print(f'Строка {data.split(" ", 1)[0]} записана')

    for parser in parsers:
        parser.join()

    sort_file(new_file)
    compare(file_result='compare_result.txt')


if __name__ == '__main__':
    run_parser(multiproc=12)

# 20.2 мин - 12 потоков
# 30.2 мин - 12 потоков
