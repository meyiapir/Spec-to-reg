import os

import PyPDF2
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from certify.ai.prompts_lib import rus_prompt, eng_prompt
from certify.core.config import settings

# Установите ваш API-ключ OpenAI
os.environ['OPENAI_API_KEY'] = settings.OPENAI_API_KEY

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
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text
            if text:
                return text
            else:
                raise ValueError(f"Не удалось извлечь текст из PDF файла: {file_path}")
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {file_extension if file_extension else 'неизвестный формат'}")

# Функция для векторизации и сопоставления
def vectorize_documents(specifications):
    # Векторизация регламентов с помощью OpenAIEmbeddings
    embedding_model = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts([specifications], embedding=embedding_model)
    return vectorstore

# Основная функция проверки требований с использованием LangChain и GPT
def check_use_cases_against_specifications_gpt(file_paths, specifications, language):
    # Векторизация текста регламентов
    vectorstore = vectorize_documents(specifications)

    # Модель GPT для анализа
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

    # Выбор шаблона на основе языка
    # Выбор шаблона на основе языка
    if language == "ru":
        prompt_template = ChatPromptTemplate.from_template(rus_prompt)
    else:
        prompt_template = ChatPromptTemplate.from_template(eng_prompt)


    output_parser = StrOutputParser()
    responses = []

    for file_path in file_paths:
        use_case_text = extract_text_from_file(file_path)

        # Сопоставление требования с векторизованными регламентами
        docs = vectorstore.similarity_search(use_case_text)

        if docs:
            # Создаем запрос для GPT
            prompt = prompt_template.format(specifications_data=specifications)

            # GPT анализирует требования и регламенты
            response = model(prompt)
            parsed_response = output_parser.invoke(response)

            responses.append({"file": file_path, "response": parsed_response})
        else:
            responses.append({"file": file_path, "response": "Не имеет соответствующих регламентов."})

    return responses




