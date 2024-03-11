import json

def optimal_costs(data, prices_for_resources):
    return 0

with open("исх.json", encoding='utf-8', mode="r") as read_file:
    data = json.load(read_file)
all_prices_for_resources = []
personal=[]
resource_name = ""
price=""
for i in range(len(data["resources"]["rows"])):
    j=0
    while data["resources"]["rows"][i]["name"][j] != '(':
        resource_name += (data["resources"]["rows"][i]["name"][j])
        j += 1
    if data["resources"]["rows"][i]["name"][j] == '(':
        j += 1
    while data["resources"]["rows"][i]["name"][j]!='р':
        price+=(data["resources"]["rows"][i]["name"][j])
        j += 1
    all_prices_for_resources.append([resource_name, data["resources"]["rows"][i]["id"], int(price)])
    price = resource_name = ""
j=0
i=0
print("prices_for_resources: ", all_prices_for_resources)
now_costs=[]
now_efforts=[]
for i in range(len(data["assignments"]["rows"])):
    for j in range(len(all_prices_for_resources)):
        if all_prices_for_resources[j][1] == data["assignments"]["rows"][i]["resource"]:
            for x in range(len(data["tasks"]["rows"][0]["children"])):
                for y in range(len(data["tasks"]["rows"][0]["children"][x]["children"])):
                    if data["assignments"]["rows"][i]["event"]==data["tasks"]["rows"][0]["children"][x]["children"][y]["id"]:
                        now_costs.append([data["tasks"]["rows"][0]["children"][x]["name"]+"/", data["tasks"]["rows"][0]["children"][x]["children"][y]["name"], all_prices_for_resources[j][0], data["tasks"]["rows"][0]["children"][x]["children"][y]["effort"] * all_prices_for_resources[j][2]])
                        personal.append(all_prices_for_resources[j][0])
            break
for i in range(len(data["assignments"]["rows"])):
    for j in range(len(all_prices_for_resources)):
        if all_prices_for_resources[j][1] == data["assignments"]["rows"][i]["resource"]:
            for x in range(len(data["tasks"]["rows"][0]["children"])):
                for y in range(len(data["tasks"]["rows"][0]["children"][x]["children"])):
                    if data["assignments"]["rows"][i]["event"]==data["tasks"]["rows"][0]["children"][x]["children"][y]["id"]:
                        now_efforts.append([data["tasks"]["rows"][0]["children"][x]["name"], data["tasks"]["rows"][0]["children"][x]["children"][y]["name"], all_prices_for_resources[j][0], data["tasks"]["rows"][0]["children"][x]["children"][y]["effort"]])
                        personal.append(all_prices_for_resources[j][0])
            break
sum_now_costs=0
for i in range(len(now_costs)):
    sum_now_costs+=now_costs[i][3]
print("now_costs", now_costs)
print("now_efforts", now_efforts)
print("sum_now_costs", sum_now_costs)
print(set(personal))

all_costs=[]
j=0
"""
циклы прогоняют данные которые я вытащил из json и сунул в массивы данных. Эти циклы считают суммарную стоимость 
"""
for i in range(len(all_prices_for_resources)):
    while all_prices_for_resources[i][0][j]!=" ":
        resource_name+=all_prices_for_resources[i][0][j]
        j+=1
    j=0
    for x in range(len(now_costs)):
        if now_costs[x][2].find(resource_name)>=0:
            if now_costs[x][3]>=all_prices_for_resources[i][2]*now_efforts[x][3]:
                all_costs.append([now_costs[x][0], now_costs[x][1], all_prices_for_resources[i][0], all_prices_for_resources[i][1], all_prices_for_resources[i][2]*now_efforts[x][3]])
    resource_name=""
count_resource_name = 0
count_resource_names=[]
for i in range(len(all_prices_for_resources)):
    while all_prices_for_resources[i][0][j]!=" ":
        resource_name+=all_prices_for_resources[i][0][j]
        j+=1
    j=0
    for x in range(len(now_costs)):
        if now_costs[x][2].find(resource_name)>=0:
            count_resource_name += 1
    if count_resource_name != 0:
        count_resource_names.append([all_prices_for_resources[i][0], count_resource_name])
    resource_name = ""
    count_resource_name = 0
print("all_costs", all_costs)
print("count_resource_names", count_resource_names)
new_costs=[]
project_name=""
resource_name=""
for i in range(len(now_costs)):
    while now_costs[i][2][j]!=" ":
        resource_name+=now_costs[i][2][j]
        j+=1
    j=0
    for x in range(len(all_costs)):
        if now_costs[i][0]==all_costs[x][0] and now_costs[i][1]==all_costs[x][1] and all_costs[x][2].find(resource_name)>=0 and now_costs[i][3]>=all_costs[x][4]:
            new_costs.append([now_costs[i][0],all_costs[x][1],all_costs[x][2],all_costs[x][3],all_costs[x][4]])
            if len(new_costs) > 0:
                if new_costs[i][0] == all_costs[x][0] and new_costs[i][1] == all_costs[x][1] and new_costs[i][2] == all_costs[x][2]:
                    break
    resource_name=""
print(new_costs)
sum_new_costs=0
for i in range(len(new_costs)):
    sum_new_costs+=new_costs[i][4]
print("sum_new_costs", sum_new_costs)
