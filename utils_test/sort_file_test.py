def sort_file(file_name):
    with open(file_name, 'r', encoding='utf8') as file:
        lines = []

        for line in file:
            lines.append(line)

    # lines.sort(key=lambda x: (int(x.split("/", 2)[1][:4]), int(x.split("/", 2)[0])))
    lines.sort(key=lambda x: int(x.split("/", 2)[0]))
    lines.sort(key=lambda x: int(x.split("/", 2)[1][:4]))
    # lines.sort(key=lambda x: int(x.split("/", 2)[0]))

    with open(file_name, 'w', encoding='utf8') as file:
        for line in lines:
            file.write(line)


sort_file('01_data/2022-12-26test.txt')
