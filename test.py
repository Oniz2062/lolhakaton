import json
from datetime import datetime, timedelta


def dumps(dict):
    return json.dumps(dict, indent=4, ensure_ascii=False)


def params(json_dict):
    sum_duration = json_dict['tasks']['rows'][0]['duration']
    workers = set()
    price_project = 0
    for asig in assignments:
        price = 0
        workers.add(asig['resource'])
        for res in resources:
            if res['id'] == asig['resource']:
                i_left, i_right = 0, 0
                for i in range(len(res['name'])):
                    if res['name'][i] == '(':
                        i_left = i
                    elif res['name'][i] + res['name'][i + 1] + res['name'][i + 2] == 'руб':
                        i_right = i
                        break
                price = int(res['name'][i_left + 1:i_right])
                break
        price_project += asig['currentEffort'] / (1000 * 3600) * price
    resource_costs = len(set(workers))
    return sum_duration, resource_costs, price_project


def сhange_date(tasks, calendars, start_date, end_date):
    format = "%Y-%m-%dT%H:%M:%S"
    tasks[3]['startDate'], tasks[3]['endDate'] = start_date, end_date
    start_date = datetime.strptime(start_date, format)
    end_date = datetime.strptime(end_date, format)
    duration = end_date - start_date
    week = duration/7
    count_days_week = week.days - 1
    for day in calendars[0]['intervals']:
        if day['startDate'] != None:
            start_lunch = datetime.strptime(day['startDate'], format)
            end_lunch = datetime.strptime(day['endDate'], format)
            if start_date <= start_lunch <= end_lunch <= end_date:
                duration -= datetime.strptime(day['endDate'], format) - datetime.strptime(day['startDate'], format)
        else:
            str1 = day["recurrentStartDate"].split()
            str2 = day["recurrentEndDate"].split()
            for i in range(len(str1)):
                if str1[i] == 'at':
                    start_lunch = datetime.strptime(str1[i+1], '%H:%M')
                    end_lunch = datetime.strptime(str2[i+1], '%H:%M')
                    if start_lunch == end_lunch:
                        duration -= timedelta(days=1) * count_days_week
                    else:
                        duration -= (end_lunch - start_lunch) * count_days_week
    print(duration)


with open("data/ish.json", mode="r", encoding="utf-8") as ish:
    js = json.load(ish)
    project1 = js['tasks']['rows'][0]["children"][0]
    project2 = js['tasks']['rows'][0]["children"][1]
    project3 = js['tasks']['rows'][0]["children"][2]
    result = dict(js['tasks']['rows'][0])
    result.pop('children')
    tasks = [project1, project2, project3, result]
    dependencies = js['dependencies']['rows']
    calendars = js['calendars']['rows']
    resources = js['resources']['rows']
    assignments = js['assignments']['rows']
    timeRanges = js['timeRanges']['rows']
    keyResults = js['keyResults']['rows']
    accountingObject = js['accountingObject']





    convert = {'tester':'Тестирование', 'developer':'Разработка', 'analyst':'Аналитика'}

    ids_resources = {}
    for item in resources:
        ids_resources[item['id']] = convert[item['projectRoleId']]
    # print(ids_resources)
    project_res_effort = {}
    for i in range(len(tasks[:-1])):
        res_effort = {}
        for group in tasks[i]['children']:
            res_effort[group['name']] = group['id']
        project_res_effort[f'project_{i+1}'] = res_effort


    # Оптимизация по ресурсам
    # Рандомные люди но всего 3
    set_humans = {}
    for e in set(ids_resources.values()):
        for key, val in ids_resources.items():
            if val == e:
                set_humans[val] = key
                break
    # print(set_humans)
    dict_assignments = {}
    for proj in project_res_effort:
        for group, id in project_res_effort[proj].items():
            dict_assignments[id] = set_humans[group]


    # Переписывание новых назначений
    test_js = js

    for assig in test_js['assignments']['rows']:
        assig['resource'] = dict_assignments[assig['event']]

    with open('data/test.json', mode='w', encoding='utf-8') as test:
        json.dump(test_js, test, indent=4, ensure_ascii=False)

    сhange_date(tasks, calendars, '2024-02-05T09:00:00', "2024-05-27T18:00:00")









