import json
from datetime import datetime, timedelta
import calendar


def dumps(dict):
    return json.dumps(dict, indent=4, ensure_ascii=False)


def get_duration_from_string(string):
    return int(''.join(''.join(string.split('PT')).split('H0M0S')))


def get_price_resource_from_string(string):
    i_left, i_right = 0, 0
    for i in range(len(string)):
        if string[i] == '(':
            i_left = i
        elif string[i] + string[i + 1] + string[i + 2] == 'руб':
            i_right = i
            break
    return int(string[i_left + 1:i_right])


def get_resource_by_uid(json_dict, UID):
    for e in json_dict['Project']['Resources']['Resource']:
        if e['UID'] == UID:
            return e


def get_task_by_uid(json_dict, UID):
    for e in json_dict['Project']['Tasks']['Task']:
        if e['UID'] == UID:
            return e

def params(json_dict):

    sum_duration = get_duration_from_string(json_dict['Project']['Tasks']['Task'][0]['Duration'])
    assignments = json_dict['Project']['Assignments']['Assignment']
    hum_work = set()
    price_project = 0
    for asig in assignments:
        hum_work.add(asig['ResourceUID'])
        resource = get_resource_by_uid(json_dict, asig['ResourceUID'])
        price_resource = get_price_resource_from_string(resource['Name'])
        task = get_task_by_uid(json_dict, asig['TaskUID'])
        duration_in_task = get_duration_from_string(task['Duration'])
        price_project += price_resource * duration_in_task
    print(price_project)
    # resource_costs = len(set(workers))
    # return sum_duration, resource_costs, price_project

with open('new_data/test.json', mode="r", encoding="utf-8") as ish:
    js = json.load(ish)

    params(js)
