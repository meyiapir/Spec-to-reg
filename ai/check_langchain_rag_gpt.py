import os

import requests

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
Use Case: "rain - light sensor malfunction"
Goal: To inform the driver about the malfunction of the rain - light sensor and ensure the driver can take appropriate actions in response to the malfunction.
Scope: SWP, Smartphone
Actor: driver, authorized user of Atom App
Preconditions:
    1. Car is on. 
    2. The driver is in the car. 
    3. The user is authorized in the Atom App on their smartphone. 
    4. Both the vehicle and the smartphone have access to a cellular network. 
    5. The auto rain-light sensor is enabled. 
Trigger:
    1. The rain sensor malfunctions. 
    2. The light sensor malfunctions. 
Main Scenario:
    1. The system detects a malfunction in either the rain sensor or the light sensor. 
    2. The system displays a failure alert on the out_2.SWP and out_5. Smartphone via the Atom App. 
    3. Automatic Wiper Function: 
        ◦ If the rain sensor malfunctions, the system disables the automatic wiper function. 
        ◦ The driver is prompted out_2.SWP to manually control the wipers in_10. 
        ◦ If a manual setting cannot be determined, the wipers turn off. 
        ◦ On out_2.SWP and out_5. Smartphone shows message. 
    4. Automatic Headlight Function (Auto Low Beam Headlamp): 
        ◦ If the light sensor malfunctions, the system disables the automatic headlight function. 
        ◦ The driver is prompted out_2.SWP to manually control the headlights in_2. 
        ◦ If a manual setting cannot be determined, the auto low beam headlamp turn off. 
        ◦ On out_2.SWP and out_5. Smartphone shows message. 

Priority: Normal

Type: Use Case CF
"""

# Загружаем файлы и отправляем запрос к API
files = [('files', (file_path.split('/')[-1], open(file_path, 'rb'))) for file_path in test_file_paths]
response = requests.post(url, data={'specifications': specifications}, files=files)

# Проверка ответа
if response.status_code == 200:
    print("Успешный ответ от API:")
    print(response.json())
else:
    print(f"Ошибка при выполнении запроса: {response.status_code}")
    print(response.text)
