import requests
import json
import os.path


def getnamarks():
    try:
        markjson = requests.get('https://gunmarks.poliroid.ru/api/com/vehicles/65,85,95', timeout=5)
    except Exception as e:
        print(e)
        print('Failed to get battle log for na')
        return

    data = markjson.json()
    with open('namarks.txt', 'w') as outfile:
        json.dump(data, outfile)


def geteumarks():
    try:
        markjson = requests.get('https://gunmarks.poliroid.ru/api/eu/vehicles/65,85,95', timeout=5)
    except Exception as e:
        print(e)
        print('Failed to get battle log for eu')
        return

    data = markjson.json()
    with open('eumarks.txt', 'w') as outfile:
        json.dump(data, outfile)


def getrumarks():
    try:
        markjson = requests.get('https://gunmarks.poliroid.ru/api/ru/vehicles/65,85,95', timeout=5)
    except Exception as e:
        print(e)
        print('Failed to get battle log for ru')
        return

    data = markjson.json()
    with open('rumarks.txt', 'w') as outfile:
        json.dump(data, outfile)


def updateregionmarks(region):
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
        print('Failed to get battle log')
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


if os.path.isfile('namarks.txt'):
    updateregionmarks('na')
else:
    getnamarks()
if os.path.isfile('eumarks.txt'):
    updateregionmarks('eu')
else:
    geteumarks()
if os.path.isfile('rumarks.txt'):
    updateregionmarks('ru')
else:
    getrumarks()
