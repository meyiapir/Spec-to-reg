import json
import os
import time

import requests
import markdown


# Пути к тестовым файлам
test_file_paths = [
    "./test_data/regl/AVAS_EN.pdf",
    "./test_data/regl/Braking_EN.pdf",
    "./test_data/regl/Wipe_and_wash_ENG.pdf",
]

# URL вашего локального FastAPI сервера
url = "http://127.0.0.1:8000/check-requirements/"

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
    print(json.dumps(json_response, indent=4, ensure_ascii=False))
else:
    print(f"Ошибка при выполнении запроса: {response.status_code}")
    print(response.text)

