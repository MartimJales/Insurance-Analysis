import csv
import sys

def separateAges(file_name, clean_file):
    arr =[]
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        arr2= next(reader)
        arr2.append('sex_age')
        arr.append(arr2)
        for row in reader:
            s = ''
            age = int(row[1])
            if (age <= 8):
                row[1] = "Kids"
            elif (age <= 18):
                row[1] = 'Adolescents '
            elif (age <= 65):
                row[1] = 'Adults'
            elif (age <= 100):
                row[1] = 'Elderly'
            s = row[0] + '-' + row[1]
            row.append(s)
            arr.append(row)

    with open(clean_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(arr)

def totals(file_name, total):
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)
        header = next(reader)
        for row in reader:
            for classe in header:
                if row[classe] not in total.keys():
                    total[row[classe]] = 0
                total[row[classe]] += 1

def intersection(file_name, dicts):
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file, fieldnames=['sex', 'age', 'body', 'local', 'month', 'sex_age'])
        header = reader.__next__()
        header.pop('sex')
        header.pop('age')
        header.pop('sex_age')
        for class1 in header:
            for class2 in ['sex', 'age']:
                str = class1 + '-' + class2
                dicts[str] = {}
        for row in reader:
            for class1 in header:
                for class2 in ['sex', 'age']:
                    str = class1 + '-' + class2
                    if row[class1] not in dicts[str]:
                        dicts[str][row[class1]] = {}
                    if row[class2] not in dicts[str][row[class1]]:
                        dicts[str][row[class1]][row[class2]] = 1
                    else:
                        dicts[str][row[class1]][row[class2]] += 1

def create_odds_tables(dicts, total, ref_arr):
    for big in dicts.keys():
        for small in dicts[big].keys():
            with open('tabelas/'+big + '-' + small + '.csv', 'w') as file:
                file.write('%s,%s,diference,OR\n' % (big, small))
                found = False
                for reference in ref_arr:
                    if reference in dicts[big][small].keys():
                        found = True
                        ref_count = dicts[big][small][reference]
                        ref_diff = total[reference] - ref_count
                        for key in dicts[big][small].keys():
                            key_count = dicts[big][small][key]
                            key_diff = total[key] - key_count
                            if key != reference:
                                odds_ratio = calculate_odds(ref_count, ref_diff, key_count, key_diff)
                                file.write('%s,%s, %s, %.2f\n' %
                                       (key, key_count, key_diff, odds_ratio))
                            else:
                                file.write('%s,%s, %s, REF\n' % (key, key_count, key_diff))
                if not found:
                    for key in dicts[big][small].keys():
                        file.write('%s,0, 0\n' % key)

def backup(dicts, total):
    for big in dicts.keys():
        for small in dicts[big].keys():
            with open('tabelas odds/'+big + '-' + small + '.csv', 'w') as file:
                file.write('%s,%s,diference\n' % (big, small))
                for key in dicts[big][small].keys():
                    file.write('%s,%s, %s\n' % (key, dicts[big][small][key], total[key] - dicts[big][small][key]))

def calculate_odds(ref_count, ref_diff, key_count, key_diff):
   return float((key_count * ref_diff)/(ref_count * key_diff))

def main(argv):
    dicts = {}
    total = {}

    '''separateAges(argv[1], argv[2])'''
    totals('table.csv', total)
    intersection('table.csv', dicts)
    reference =["Adults","boy"]
    create_odds_tables(dicts, total, reference)

    for elme in dicts.items():
        print(elme)

if __name__ == '__main__':
    main(sys.argv)
