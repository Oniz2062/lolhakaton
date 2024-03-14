import json
from datetime import datetime, timedelta
import calendar



# Считает количество пон, вт, ср, чт, пт, cб, вск во временном интервале
def days_weekly_month(start_date, end_date):
    format = "%Y-%m-%dT%H:%M:%S"
    start_date = datetime.strptime(start_date, format)
    end_date = datetime.strptime(end_date, format)
    convert = {0: 'MONDAY', 1: 'TUESDAY', 2: 'WEDNESDAY', 3: 'THURSDAY', 4: 'FRIDAY', 5: 'SATURDAY', 6: 'SUNDAY'}
    days_week = {}
    while start_date < end_date:
        key = convert[start_date.weekday()]
        if key not in days_week:
            days_week[key] = []
        days_week[key].append(full_day(datetime.strftime(start_date, format)))
        start_date += timedelta(days=1)
    return days_week


def special_weekends(start_date, end_date, calendars):
    format = "%Y-%m-%dT%H:%M:%S"
    start_date = datetime.strptime(start_date, format)
    end_date = datetime.strptime(end_date, format)
    list_special_weekends = []
    for cal in calendars['rows']:
        for day in cal['intervals']:
            if day['startDate'] is not None and day['endDate'] is not None:
                current_start_date = datetime.strptime(day['startDate'], format)
                current_end_date = datetime.strptime(day['endDate'], format)
                if day['workException'] == 'WEEKEND' and start_date <= current_start_date <= current_end_date <= end_date:
                    list_special_weekends.append((day['startDate'], day['endDate']))
    return list_special_weekends


def calendar_working_false(start_date, end_date, calendars):
    list_weekends = []
    dict_days = days_weekly_month(start_date, end_date)
    for day_weekly in dict_days:
        for cal in calendars['rows']:
            for day in cal['intervals']:
                if day['recurrentStartDate'] is not None and day['recurrentEndDate'] is not None:
                    list_tuples_day_time_start = read_recurrent_date(day['recurrentStartDate'])
                    list_tuples_day_time_end = read_recurrent_date(day['recurrentEndDate'])
                    for i in range(len(list_tuples_day_time_start)):
                        if day['isWorking'] is False and day["recurrentWeekday"] == day_weekly \
                                and list_tuples_day_time_start[i][0] != list_tuples_day_time_end[i][0]\
                                and list_tuples_day_time_start[i][1] == list_tuples_day_time_end[i][1]:
                            list_weekends.extend(dict_days[day_weekly])
    return list_weekends


def weekends_in_project(project, calendars):
    working_false = calendar_working_false(project['startDate'], project['endDate'], calendars)
    spec_week = special_weekends(project['startDate'], project['endDate'], calendars)
    working_false.extend(spec_week)
    return working_false



def dumps(dict):
    return json.dumps(dict, indent=4, ensure_ascii=False)


def get_price_resource_from_string(string):
    i_left, i_right = 0, 0
    for i in range(len(string)):
        if string[i] == '(':
            i_left = i
        elif string[i] + string[i + 1] + string[i + 2] == 'руб':
            i_right = i
            break
    return int(string[i_left + 1:i_right])


def get_resource_by_id(resources, id):
    for res in resources['rows']:
        if res['id'] == id:
            return res


def get_task_by_id(json_dict, task_id):
    for d in recursive_flatten_iterator(json_dict):
        if d['id'] == task_id:
            return d
    raise 'Задания такого id нет в списке'


def recursive_flatten_iterator(d):
    if isinstance(d, dict):
        yield d
        if d['expanded'] is True:
            yield from recursive_flatten_iterator(d['children'])
    if isinstance(d, list):
        for d in d:
            yield from recursive_flatten_iterator(d)


def is_weekend_in_calendar(day_str, calendars):
    format = "%Y-%m-%dT%H:%M:%S"
    day_search = datetime.strptime(day_str, format)
    for calendar in calendars['rows']:
        for day_calendar in calendar['intervals']:
            if day_calendar['startDate'] is not None:
                start_date = datetime.strptime(day_calendar['startDate'], format)
                end_date = datetime.strptime(day_calendar['endDate'], format)
                if day_calendar['workException'] == 'WEEKEND' and start_date <= day_search <= end_date:
                    return True
    return False


def full_day(str_start):
    format = "%Y-%m-%dT%H:%M:%S"
    str_start = datetime.strptime(str_start, format)
    str_end = str_start + timedelta(days=1)
    drop_start_date = datetime.strftime(str_start.date(), format)
    drop_end_date = datetime.strftime(str_end.date(), format)
    return drop_start_date, drop_end_date


def why_weekends_in_project(dict_project, calendars):
    for calendar in calendars['rows']:
        format = "%Y-%m-%dT%H:%M:%S"
        start_date = datetime.strptime(dict_project['startDate'], format)
        end_date = datetime.strptime(dict_project['endDate'], format)
        # count_weekends = 0
        weekends = []
        while start_date < end_date:
            if is_weekend_in_calendar(datetime.strftime(start_date, format), calendar['intervals']):
                weekends.append(full_day(datetime.strftime(start_date, format)))
            start_date += timedelta(days=1)
    return weekends


def date_is_week(str_date, list_weekends):
    for week in list_weekends:
        if week[0] <= str_date <= week[1]:
            return True
    return False


def correction_date_str(str_date, project, calendars):
    format = "%Y-%m-%dT%H:%M:%S"
    list_weekends = weekends_in_project(project, calendars)
    while date_is_week(str_date, list_weekends):
        str_date = datetime.strftime(datetime.strptime(str_date, format) + timedelta(days=1), format)
    return str_date


def displacement_task_with_childrens(left_border, task, calendars):
    for task in recursive_flatten_iterator(task):
        left_border = displacement_date_project_in_left(left_border, task, calendars)

def is_working_time(date, calendars):
    convert = {0: 'MONDAY', 1: 'TUESDAY', 2: 'WEDNESDAY', 3: 'THURSDAY', 4: 'FRIDAY', 5: 'SATURDAY', 6: 'SUNDAY'}
    format = "%Y-%m-%dT%H:%M:%S"
    date = datetime.strptime(date, format)
    format = '%H:%M'
    date = datetime.strptime(datetime.strftime(date, format), format)
    for calendar in calendars['rows']:
        for day in calendar['intervals']:
            if day['recurrentStartDate'] is not None and day['isWorking'] is False \
                    and day['recurrentWeekday'] == convert[date.weekday()]:
                rec_start_date = read_recurrent_date(day['recurrentStartDate'])
                rec_end_date = read_recurrent_date(day['recurrentEndDate'])
                for i in range(len(rec_start_date)):
                    start_date = (datetime.strptime(rec_start_date[i][1], format))
                    end_date = (datetime.strptime(rec_end_date[i][1], format))
                    if start_date > end_date:
                        end_date += timedelta(days=1)
                    if start_date <= date < end_date:
                        return False
    return True


def shift_data_on_work_time(start_date, end_date, calendars):
    format = "%Y-%m-%dT%H:%M:%S"
    convert = {0: 'MONDAY', 1: 'TUESDAY', 2: 'WEDNESDAY', 3: 'THURSDAY', 4: 'FRIDAY', 5: 'SATURDAY', 6: 'SUNDAY'}
    start_date = datetime.strptime(start_date, format)
    end_date = datetime.strptime(end_date, format)
    format = '%Y-%m-%d'
    start_date = datetime.strptime(datetime.strftime(start_date, format), format)
    end_date = datetime.strptime(datetime.strftime(end_date, format), format)
    format = '%H:%M'
    for calendar in calendars['rows']:
        for day in calendar['intervals']:
            if day['recurrentStartDate'] is not None and day['isWorking'] is True \
                    and day['recurrentWeekday'] == convert[start_date.weekday()]:
                rec_start_date = read_recurrent_date(day['recurrentStartDate'])
                rec_end_date = read_recurrent_date(day['recurrentEndDate'])
                start_day = start_date.date()
                start_time = datetime.strptime(rec_start_date[0][1], format).time()
                end_day = end_date.date()
                end_time = datetime.strptime(rec_end_date[-1][1], format).time()
                start_date = datetime(start_day.year, start_day.month, start_day.day, start_time.hour, start_time.minute, start_time.second)
                end_date = datetime(end_day.year, end_day.month, end_day.day, end_time.hour, end_time.minute, end_time.second)
                format = "%Y-%m-%dT%H:%M:%S"
                return datetime.strftime(start_date, format), datetime.strftime(end_date, format)

def displacement_date_project_in_left(left_border, task, calendars):
    format = "%Y-%m-%dT%H:%M:%S"

    convert_effort = {'d': 24, 'h': 1}
    convert_duration = {'d': 8, 'h': 1}

    left_border = datetime.strptime(left_border, format)

    start_date = datetime.strptime(task['startDate'], format)
    end_date = datetime.strptime(task['endDate'], format)


    start_weekends_in_project = weekends_in_project(task, calendars)

    # duration = task['duration'] * convert_duration[task['durationUnit']] / 8
    # effort = task['effort'] * convert_effort[task['effortUnit']]

    # Смещение
    delta = abs(start_date - left_border)
    start_date = left_border
    end_date -= delta

    # Замена дат в проекте
    task['startDate'] = correction_date_str(datetime.strftime(start_date, format), task, calendars)  # коррекция вправо до первого буднего
    task['startDate'] = shift_data_on_work_time(task['startDate'], task['endDate'], calendars)[0]

    end_weekends_in_project = weekends_in_project(task, calendars)

    weekends = len(end_weekends_in_project) - len(start_weekends_in_project)

    if task['expanded'] is True:  # достаточно вычесть из проекта в целом, а у сыновей только корректировать даты
        end_date = end_date - timedelta(days=weekends)

    task['endDate'] = correction_date_str(datetime.strftime(end_date, format), task, calendars)

    task['endDate'] = shift_data_on_work_time(task['startDate'], task['endDate'], calendars)[1]

    if task['expanded'] is True:
        new_left_border = task['startDate']
    else:
        new_left_border = task['endDate']

    return new_left_border
    # print(dumps(task))

# def displacement_date_project_in_left_and_correct_children_recurs(left_border, task, calendars):
#     for t in displacement_date_project_in_left(left_border, task, calendars):
#         print(dumps(t))

# def displacement_date_project_in_left_and_correct_children_recurs(left_border, project, calendars):
#     if isinstance(project, dict):
#         left_border = displacement_date_project_in_left(left_border, project, calendars)
#         yield left_border
#         if project['expanded'] is True:
#             yield from displacement_date_project_in_left_and_correct_children_recurs(left_border, project['children'], calendars)
#     if isinstance(project, list):
#         for child in project:
#             yield from displacement_date_project_in_left_and_correct_children_recurs(left_border, child, calendars)


# def displacement_date_project_in_left_and_correct_children(left_border, project, calendars):
#     for x in displacement_date_project_in_left_and_correct_children_recurs(left_border, project, calendars):
#         print(x)


def max_duration_in_project(dict_json):
    max_durations = 0
    for row in dict_json['tasks']['rows']:
        for proj in row['children']:
            max_durations = max(proj['duration'], max_durations)
    return max_durations


def get_project_max_duration(dict_json):
    for row in dict_json['tasks']['rows']:
        for proj in row['children']:
            if proj['duration'] == max_duration_in_project(dict_json):
                return proj


def optimization(dict_json):
    format = "%Y-%m-%dT%H:%M:%S"
    calendars = dict_json['calendars']
    count_tasks = len(dict_json['tasks']['rows'][0]['children'])
    step_border = int(dict_json['tasks']['rows'][0]['duration'] / count_tasks)
    for task in dict_json['tasks']['rows'][0]['children']:
        left_border = dict_json['tasks']['rows'][0]['startDate']
        displacement_task_with_childrens(left_border, task, calendars)
        left_border = datetime.strptime(left_border, format)
        left_border += timedelta(days=step_border)



# def linkage_project(project, calendars):
def get_assign_by_id_task(id_task, assignments):
    for assign in assignments['rows']:
        if assign['event'] == id_task:
            return assign
    raise 'На это задание никто не назначен'


# def get_assign_by_id_resource(id_resource, assignments):
#     for assign in assignments['rows']:
#         if assign['resource'] == id_resource:
#             return assign
#     raise 'На это задание никто не назначен'


def who_resource_in_task(task, assignments):
    task_id = task['id']
    resource_id = get_assign_by_id_task(task_id, assignments)['resource']
    return get_resource_by_id(resource_id)


def get_all_prices_resources_by_role(resources, project_role_id):
    prices = []
    for res in resources['rows']:
        current_project_role = res.get('projectRoleId', None)
        if current_project_role == project_role_id:
            prices.append(get_price_resource_from_string(res['name']))
    return prices


# def get_inexpensive_resource_by_role(task, resources, project_role_id):
#     all_price = get_all_prices_resources_by_role(resources, project_role_id))
#     for res in resources['rows']:
#         while len( != 1:
#             for i in range(sorted(get_all_prices_resources_by_role(resources, project_role_id), reverse=True))
#         return


def get_role_resource_by_str_task(name_task):
    convert = {'Аналитика': 'analyst', 'Разработка': 'developer', 'Тестирование': 'tester'}
    for task in convert:
        if task in name_task:
            return convert[task]
    return 'not in project'


# def resource_is_spare(id_resource, start_date_task, end_date_task, assignments):
#     for assign in assignments['rows']:
#         if assign['resource'] == id_resource:
#             assign['endDate']


# def appoint_resource_on_task(task, resources, assignments):
#     project_role_id = get_role_resource_by_str_task(task['name'])
#     inexpensive_resource = get_inexpensive_resource_by_role(resources, task, project_role_id)
#     for assign in assignments['rows']:
#         if assign['event'] == task['id']:
#             assign['resource'] = inexpensive_resource['id']


def params(json_dict):
    convert = {'day': 24, 'hour': 1}  # months - ?
    info_all_project = json_dict['tasks']['rows'][0]
    sum_duration = str(info_all_project['duration']) + info_all_project['durationUnit']
    assignments = json_dict['assignments']['rows']
    hum_work = set()
    price_project = 0
    for asig in assignments:
        hum_work.add(asig['resource'])
        resource = get_resource_by_id(json_dict['resources'], asig['resource'])
        price_resource = get_price_resource_from_string(resource['name'])
        task = get_task_by_id(json_dict, asig['event'])
        effort_in_task_hour = task['effort']*convert[task['effortUnit']]
        price_project += price_resource * effort_in_task_hour
    return sum_duration, len(hum_work), price_project


def read_recurrent_date(str_date):
    str_date = str_date.split()
    day_time = []
    for i in range(len(str_date) - 1):
        if str_date[i] == 'on':
            tup = (str_date[i+1], str_date[i+3])
            day_time.append(tup)
    return day_time


def all_keys(input_dict):
    if isinstance(input_dict, dict):
        keys = [* input_dict.keys(), ]
        for key, val in input_dict.items():
            keys.extend(all_keys(val))
        return keys
    else:
        return []


with open("data/my_test_end.json", mode="r", encoding="utf-8") as ish:
    js = json.load(ish)
    # optimization(js)
    # project = js['tasks']['rows'][0]['children'][2]
    # calendars = js['calendars']
    optimization(js)
    with open("data/my_test_end.json", mode="w", encoding="utf-8") as file:
        json.dump(js, file, indent=4, ensure_ascii=False)






