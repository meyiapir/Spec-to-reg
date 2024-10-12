from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import PyPDF2
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
import tempfile

app = FastAPI()

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
    if language == "ru":
        prompt_template = ChatPromptTemplate.from_template(
            """
            Ты система для сверки спецификации с регламентами. Отвечай максимально точно без лишних отступлений. Проанализируй следующие требования на соответствие регламентам: {requirement}.
            Для каждого требования сопоставь его с регламентом и укажи, соблюдены ли регламенты. Если модель найдет слово или термин, который вызывает затруднение или который она интерпретирует как неясный, выдели его с двух сторон символами #- (например, #-Слово#-).
            Добавь комментарий, если есть расхождения между требованиями и регламентом, и также выделяй проблемные термины в этих комментариях.
            """
        )
    else:
        prompt_template = ChatPromptTemplate.from_template(
            """
            Analyze the following requirements for compliance with the regulations: {requirement}. 
            For each requirement, match it with the regulation and indicate whether the regulations are met. If the model finds a word or term that is unclear or difficult to interpret, highlight it with #- symbols on both sides (e.g., #-Word#-).
            Add a comment if there are discrepancies between the requirements and the regulations, and also highlight problematic terms in these comments.
            """
        )

    output_parser = StrOutputParser()
    responses = []

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

            responses.append({"file": file_path, "response": parsed_response})
        else:
            responses.append({"file": file_path, "response": "Не имеет соответствующих регламентов."})

    return responses

# Маршрут для загрузки файлов и текстовых спецификаций
@app.post("/check-requirements/")
async def check_requirements(specifications: str = Form(...), language: str = Form("en"), files: list[UploadFile] = File(...)):
    file_paths = []
    try:
        # Сохранение загруженных файлов во временные файлы
        for file in files:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf' if file.filename.endswith('.pdf') else '.txt')
            temp_file.write(await file.read())
            temp_file.close()
            file_paths.append(temp_file.name)

        # Проверка требований на соответствие регламентам
        results = check_use_cases_against_specifications_gpt(file_paths, specifications, language)

        return JSONResponse(content={"results": results})

    finally:
        # Удаление временных файлов
        for path in file_paths:
            if os.path.exists(path):
                os.remove(path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
