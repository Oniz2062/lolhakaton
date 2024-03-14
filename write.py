import json
with open('data/test_taskend.json', mode='r', encoding='utf-8') as ish:
    js = json.load(ish)
    with open('data/my_test_end.json', mode='w', encoding='utf-8') as file:
        json.dump(js, file, indent=4, ensure_ascii=False)