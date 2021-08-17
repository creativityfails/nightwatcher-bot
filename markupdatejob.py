import requests
import json
import os.path


def get_na_marks_file():
    try:
        markjson = requests.get('https://gunmarks.poliroid.ru/api/com/vehicles/65,85,95', timeout=5)
    except Exception as e:
        print(e)
        print('Failed to get marks for na')
        return

    data = markjson.json()
    with open('namarks.txt', 'w') as outfile:
        json.dump(data, outfile)


def get_eu_marks_file():
    try:
        markjson = requests.get('https://gunmarks.poliroid.ru/api/eu/vehicles/65,85,95', timeout=5)
    except Exception as e:
        print(e)
        print('Failed to get marks for eu')
        return

    data = markjson.json()
    with open('eumarks.txt', 'w') as outfile:
        json.dump(data, outfile)


def get_ru_marks_file():
    try:
        markjson = requests.get('https://gunmarks.poliroid.ru/api/ru/vehicles/65,85,95', timeout=5)
    except Exception as e:
        print(e)
        print('Failed to get marks for ru')
        return

    data = markjson.json()
    with open('rumarks.txt', 'w') as outfile:
        json.dump(data, outfile)


def update_region_marks_file(region):
    regions = ['na', 'eu', 'ru']
    if region not in regions:
        return
    if region == 'na':
        url = 'https://gunmarks.poliroid.ru/api/com/vehicles/65,85,95'
    else:
        url = 'https://gunmarks.poliroid.ru/api/' + region + '/vehicles/65,85,95'
    try:
        markjson = requests.get(url, timeout=5)
    except Exception as e:
        print(e)
        print(f'Failed to get marks for {region}')
        return

    data = markjson.json()

    regionFile = region + 'marks.txt'
    with open(regionFile) as markfile:
        olddata = json.load(markfile)

    for newvalue in data['data']:
        if not newvalue['marks']['95'] or not newvalue['marks']['85'] or not newvalue['marks']['65']:
            for item in olddata['data']:
                if item['id'] == newvalue['id']:
                    oldDataValues = item['marks']
            if not newvalue['marks']['95']:
                newvalue['marks']['95'] = oldDataValues['95']
            if not newvalue['marks']['85']:
                newvalue['marks']['85'] = oldDataValues['85']
            if not newvalue['marks']['65']:
                newvalue['marks']['65'] = oldDataValues['65']

    with open(regionFile, 'w') as outfile:
        json.dump(data, outfile)


def update_marks_file():
    if os.path.isfile('namarks.txt'):
        update_region_marks_file('na')
    else:
        get_na_marks_file()
    if os.path.isfile('eumarks.txt'):
        update_region_marks_file('eu')
    else:
        get_eu_marks_file()
    if os.path.isfile('rumarks.txt'):
        update_region_marks_file('ru')
    else:
        get_ru_marks_file()


def get_marks_heap(d=None):
    if d is None:
        d = {'na': {}, 'eu': {}, 'ru': {}}
    try:
        markjson = requests.get('https://gunmarks.poliroid.ru/api/com/vehicles/65,85,95', timeout=5)
        data = markjson.json()
        for tank in data['data']:
            d['na'][tank['id']] = f' 1 mark: {tank["marks"]["65"]}. 2 marks: {tank["marks"]["85"]}. 3 marks: {tank["marks"]["95"]}'
    except Exception as e:
        print(e)
        print('Failed to get marks for na')

    try:
        markjson = requests.get('https://gunmarks.poliroid.ru/api/eu/vehicles/65,85,95', timeout=5)
        data = markjson.json()
        for tank in data['data']:
            d['eu'][tank['id']] = f' 1 mark: {tank["marks"]["65"]}. 2 marks: {tank["marks"]["85"]}. 3 marks: {tank["marks"]["95"]}'
    except Exception as e:
        print(e)
        print('Failed to get marks for eu')

    try:
        markjson = requests.get('https://gunmarks.poliroid.ru/api/ru/vehicles/65,85,95', timeout=5)
        data = markjson.json()
        for tank in data['data']:
            d['ru'][tank['id']] = f' 1 mark: {tank["marks"]["65"]}. 2 marks: {tank["marks"]["85"]}. 3 marks: {tank["marks"]["95"]}'
    except Exception as e:
        print(e)
        print('Failed to get marks for ru')

    return d


if __name__ == '__main__':
    print(get_marks_heap())
