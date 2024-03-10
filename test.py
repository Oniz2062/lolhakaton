import json


def dumps(dict):
    return json.dumps(dict, indent=4, ensure_ascii=False)


with open("data/opt_dlit.json", mode="r", encoding="utf-8") as ish:
    js = json.load(ish)
    project1 = js['tasks']['rows'][0]["children"][0]
    project2 = js['tasks']['rows'][0]["children"][1]
    project3 = js['tasks']['rows'][0]["children"][2]
    del js['tasks']['rows'][0]["children"]
    result = js['tasks']['rows'][0]
    tasks = [project1, project2, project3, result]
    dependencies = js['dependencies']['rows']
    calendars = js['calendars']['rows']
    resources = js['resources']['rows']
    assignments = js['assignments']['rows']
    timeRanges = js['timeRanges']['rows']
    keyResults = js['keyResults']['rows']
    accountingObject = js['accountingObject']

    sum_duration = tasks[3]['duration']

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
                    elif res['name'][i] + res['name'][i+1] + res['name'][i+2] == 'руб':
                        i_right = i
                        break
                price = int(res['name'][i_left + 1:i_right])
                break
        price_project += asig['currentEffort'] / (1000 * 3600) * price

    resource_costs = len(set(workers))

    data = (sum_duration, resource_costs, price_project)






