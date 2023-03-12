import csv


def write_table_int(file_path, rows):
    with open(file_path, 'w', newline='', encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def write_table(file_path, dicty):
    items = list()
    items.append(("Date", "Weight"))
    tmp = dict()
    for key in sorted(dicty.keys()):
        val = dicty[key]
        ts = val["t"].split('T')[0]
        ws = val["w"]
        tmp[ts] = ws
    for key in sorted(tmp.keys()):
        items.append((key, tmp[key]))
    write_table_int(file_path, items)
