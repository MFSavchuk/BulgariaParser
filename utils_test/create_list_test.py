import os

filepaths = [os.path.join(dirpath, file) for dirpath, dirnames, filenames in os.walk('../01_data') for file in filenames]

last_number = '110750/2021'
counter = 0

try:
    for filepath in filepaths:
        with open(filepath, 'r', encoding='utf8') as ff1, open('../01_data/2022-12-22.txt', 'a+', encoding='utf8') as ff2:
            for line in ff1:
                if 'финален експертен' in line:
                    counter += 1
                if last_number in line:
                    raise ValueError
                number = str(line.split(' ', 1)[0])
                print(number)
                if number in ff2:
                    continue
                if 'Няма такава преписка заведена по консулски път' in line:
                    continue
                else:
                    ff2.write(line)
except ValueError:
    print(f'Список создан до {last_number}, перед ним {counter} человек')
