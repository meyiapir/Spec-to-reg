from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import openai
import tiktoken
import faiss

import os
import PyPDF2

# Установите ваш API-ключ OpenAI
os.environ['OPENAI_API_KEY'] = ''

# Функция для извлечения текста из текстовых файлов или PDF
def extract_text_from_file(file_path):
    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == ".txt":
        # Извлечение текста из текстового файла
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    elif file_extension.lower() == ".pdf":
        # Извлечение текста из PDF-файла
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            return text
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {file_extension}")

# Функция для векторизации и сопоставления
def vectorize_documents(specifications):
    # Векторизация регламентов с помощью OpenAIEmbeddings
    embedding_model = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts([specifications], embedding=embedding_model)
    return vectorstore

# Основная функция проверки требований с использованием LangChain и GPT
def check_use_cases_against_specifications_gpt(file_paths, specifications):
    # Векторизация текста регламентов
    vectorstore = vectorize_documents(specifications)

    # Модель GPT для анализа
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    prompt_template = ChatPromptTemplate.from_template(
        "Проанализируй следующие требования на соответствие регламентам: {requirement}. "
        "Для каждого требования сообщи, соблюдены ли регламенты, и добавь комментарий, если есть расхождения."
    )
    output_parser = StrOutputParser()

    for file_path in file_paths:
        use_case_text = extract_text_from_file(file_path)

        # Сопоставление требования с векторизованными регламентами
        docs = vectorstore.similarity_search(use_case_text)

        if docs:
            # Создаем запрос для GPT
            prompt = prompt_template.format(requirement=use_case_text)

            # GPT анализирует требования и регламенты
            response = model(prompt)
            parsed_response = output_parser.invoke(response)

            # Выводим результат
            print(f"Файл: {file_path}")
            print(f"Ответ GPT: {parsed_response}")
            print("-" * 40)
        else:
            print(f"Файл: {file_path} не имеет соответствующих регламентов.")
            print("-" * 40)

# Пример использования функции:
file_paths = ["./regl/AVAS_EN.pdf", "./regl/Braking_EN.pdf", "./regl/Wipe_and_wash_ENG.pdf"]  # Пути к файлам с регламентами
specifications = """
I-23222
OC Subsection: [F-3681] New OC Subsection: 06 Driving / Wipers and Washers

Description: 
Use Case: "rain - light sensor malfunction"
Goal: To inform the driver about the malfunction of the rain - light sensor and esnure the driver can take appropriate actions in response to the malfunction.
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
check_use_cases_against_specifications_gpt(file_paths, specifications)
