import json
import os
import time

import requests
import markdown


a = {'results': [{'file': 'C:\\Users\\meyap\\AppData\\Local\\Temp\\tmpr6l44ju5.pdf', 'response': '{\n  "specifications": [\n    {\n      "specifications": "Машинка для людей",\n      "validation": "Не соответствует регламенту",\n      "comments": "Термин #-Машинка для людей-# является некорректным и требует замены на точное техническое определение, например, \'автомобиль\' или \'транспортное средство\'."\n    },\n    {\n      "specifications": "ТИпо тесла",\n      "validation": "Не соответствует регламенту",\n      "comments": "Термин #-Типо тесла-# не является техническим и требует замены на более точное описание, например, \'электрический автомобиль\' или \'автомобиль, аналогичный Tesla\'."\n    }\n  ],\n  "summary": {\n    "issues": "Некорректные термины: #-Машинка для людей-#, #-Типо тесла-#",\n    "recommendations": [\n      "Заменить термин \'Машинка для людей\' на \'автомобиль\' или \'транспортное средство\'.",\n      "Заменить термин \'Типо тесла\' на \'электрический автомобиль\' или \'автомобиль, аналогичный Tesla\'."\n    ]\n  }\n}'}, {'file': 'C:\\Users\\meyap\\AppData\\Local\\Temp\\tmpfaozykns.pdf', 'response': '{\n  "specifications": [\n    {\n      "specifications": "Машинка для людей",\n      "validation": "Не соответствует регламенту",\n      "comments": "Термин #-Машинка-# является некорректным и требует замены на точный технический термин, например, \'автомобиль\' или \'транспортное средство\'."\n    },\n    {\n      "specifications": "ТИпо тесла",\n      "validation": "Не соответствует регламенту",\n      "comments": "Фраза #-Типо тесла-# не является техническим термином и требует замены на более точное описание, например, \'электрический автомобиль с аналогичными характеристиками\'."\n    }\n  ],\n  "summary": {\n    "issues": "Некорректные термины: #-Машинка-#, #-Типо тесла-#",\n    "recommendations": [\n      "Заменить термин \'Машинка\' на \'автомобиль\' или \'транспортное средство\'.",\n      "Заменить фразу \'Типо тесла\' на \'электрический автомобиль с аналогичными характеристиками\'."\n    ]\n  }\n}'}, {'file': 'C:\\Users\\meyap\\AppData\\Local\\Temp\\tmpt092rue1.pdf', 'response': '{\n  "specifications": [\n    {\n      "specifications": "Машинка для людей",\n      "validation": "Не соответствует регламенту",\n      "comments": "Термин #-Машинка для людей-# является некорректным и требует замены на точное техническое определение, например, \'автомобиль\' или \'транспортное средство\'."\n    },\n    {\n      "specifications": "ТИпо тесла",\n      "validation": "Не соответствует регламенту",\n      "comments": "Термин #-Типо тесла-# не является техническим и требует замены на более точное описание, например, \'электрический автомобиль аналогичного класса\'."\n    }\n  ],\n  "summary": {\n    "issues": "Некорректные термины: #-Машинка для людей-#, #-Типо тесла-#",\n    "recommendations": [\n      "Заменить термин \'Машинка для людей\' на \'автомобиль\' или \'транспортное средство\'.",\n      "Заменить термин \'Типо тесла\' на \'электрический автомобиль аналогичного класса\'."\n    ]\n  }\n}'}]}
for i in a['results']:
    print(json.loads(i['response'])['summary']['issues'])
exit(0)

# Пути к тестовым файлам
test_file_paths = [
    "./test_data/regl/AVAS_EN.pdf",
    "./test_data/regl/Braking_EN.pdf",
    "./test_data/regl/Wipe_and_wash_ENG.pdf",
]

# URL вашего локального FastAPI сервера
url = "http://127.0.0.1:8000/process/check-specifications/"

# Тестовые спецификации
specifications = """
I-23222
OC Subsection: [F-3681] New OC Subsection: 06 Driving / Wipers and Washers

Description: 
Машинка для людей
ТИпо тесла
"""

# Загружаем файлы и отправляем запрос к API
files = [('files', (file_path.split('/')[-1], open(file_path, 'rb'))) for file_path in test_file_paths]
data = {
    'specifications': specifications,
    'language': 'ru'
}
t1 = time.time()
response = requests.post(url, data=data, files=files)
print(f"Время выполнения: {time.time() - t1:.2f} сек.")

# Проверка ответа
if response.status_code == 200:
    # Получение JSON ответа
    json_response = response.json()

    # Красивый вывод с отступами
    print("Успешный ответ от API:")
    print(json_response)
else:
    print(f"Ошибка при выполнении запроса: {response.status_code}")
    print(response.text)

