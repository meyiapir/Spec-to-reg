import os

import requests
import json

# Define the API endpoint and the port number that FastAPI is running on
API_URL = "http://localhost:8000/check-requirements/"

# Define the specification text for testing
specification_text = """
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

# Define paths to the test use case files
test_files = [
    ("use_case_1.txt", "This is a test use case file 1 content."),
    ("use_case_2.txt", "This is a test use case file 2 content."),
]

# Create temporary files for the use case files
temp_files = []
for filename, content in test_files:
    with open(filename, 'w') as f:
        f.write(content)
        temp_files.append(filename)

# Prepare the files to be uploaded
files = [("use_case_files", (open(temp_file, 'rb'))) for temp_file in temp_files]

# Define the data payload for the POST request
data = {
    "specification": specification_text,
}

# Send the POST request to the FastAPI server and capture the response
response = requests.post(API_URL, data=data, files=files)

# Check the response status code
if response.status_code == 200:
    print("Response received successfully:")
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))
else:
    print(f"Failed to receive response. Status code: {response.status_code}")
    print(response.text)

# Clean up temporary files
for temp_file in temp_files:
    try:
        os.remove(temp_file)
    except OSError as e:
        print(f"Error: {temp_file} : {e.strerror}")
