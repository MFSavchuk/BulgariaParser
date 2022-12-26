def sort_file(file_name):
    with open(file_name, 'r', encoding='utf8') as file:
        lines = []
        lines2019 = []
        lines2020 = []
        lines2021 = []
        lines2022 = []

        for line in file:
            year = line.split("/", 2)[1][:4]
            if year == '2019':
                lines2019.append(line)
            elif year == '2020':
                lines2020.append(line)
            elif year == '2021':
                lines2021.append(line)
            elif year == '2022':
                lines2022.append(line)

    lines2019 = sorted(lines2019, key=lambda x: int(x.split("/", 2)[0]))
    lines2020 = sorted(lines2020, key=lambda x: int(x.split("/", 2)[0]))
    lines2021.sort(key=lambda x: int(x.split("/", 2)[0]))
    lines2022.sort(key=lambda x: int(x.split("/", 2)[0]))

    lines.extend(lines2019)
    lines.extend(lines2020)
    lines.extend(lines2021)
    lines.extend(lines2022)

    with open(file_name, 'w', encoding='utf8') as file:
        for line in lines:
            file.write(line)
