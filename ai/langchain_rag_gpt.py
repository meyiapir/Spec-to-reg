import os
from typing import List
import PyPDF2
import docx
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
import uvicorn

app = FastAPI()

# Конфигурация для различных параметров
class Config:
    # Set OpenAI API Key and other parameters from environment variables, allowing easy configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key_here')
    MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-4o-mini')
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.0))

# Установите API ключ OpenAI
os.environ['OPENAI_API_KEY'] = Config.OPENAI_API_KEY

# Функция для извлечения текста из файла
class TextExtractor:
    @staticmethod
    async def extract_text_from_file(upload_file: UploadFile) -> str:
        # Determine the file extension and extract text accordingly
        print(f"Extracting text from file: {upload_file.filename}")
        _, file_extension = os.path.splitext(upload_file.filename)

        if file_extension.lower() == ".txt":
            return await TextExtractor._extract_from_txt(upload_file)
        elif file_extension.lower() == ".pdf":
            return await TextExtractor._extract_from_pdf(upload_file)
        elif file_extension.lower() == ".docx":
            return await TextExtractor._extract_from_docx(upload_file)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    @staticmethod
    async def _extract_from_txt(upload_file: UploadFile) -> str:
        try:
            # Read text from a TXT file
            print(f"Reading TXT file: {upload_file.filename}")
            contents = await upload_file.read()
            return contents.decode('utf-8')
        except FileNotFoundError:
            # Handle case where file is not found
            print(f"FileNotFoundError for file: {upload_file.filename}")
            raise FileNotFoundError(f"The file {upload_file.filename} was not found.")
        except PermissionError:
            # Handle permission error during file access
            print(f"PermissionError for file: {upload_file.filename}")
            raise PermissionError(f"Permission denied for file {upload_file.filename}.")

    @staticmethod
    async def _extract_from_pdf(upload_file: UploadFile) -> str:
        try:
            # Read text from a PDF file
            print(f"Reading PDF file: {upload_file.filename}")
            contents = await upload_file.read()
            # Write contents to a temporary file for reading with PyPDF2
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_file.write(contents)
                temp_file_path = temp_file.name
            # Use PyPDF2 to extract text from each page of the PDF
            with open(temp_file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ''.join(page.extract_text() for page in reader.pages if page.extract_text())
            return text
        except FileNotFoundError:
            # Handle case where file is not found
            print(f"FileNotFoundError for file: {upload_file.filename}")
            raise FileNotFoundError(f"The file {upload_file.filename} was not found.")
        except PermissionError:
            # Handle permission error during file access
            print(f"PermissionError for file: {upload_file.filename}")
            raise PermissionError(f"Permission denied for file {upload_file.filename}.")

    @staticmethod
    async def _extract_from_docx(upload_file: UploadFile) -> str:
        try:
            # Read text from a DOCX file
            print(f"Reading DOCX file: {upload_file.filename}")
            contents = await upload_file.read()
            # Write contents to a temporary file for reading with the python-docx library
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_file:
                temp_file.write(contents)
                temp_file_path = temp_file.name
            # Use python-docx to extract text from the document
            doc = docx.Document(temp_file_path)
            text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except FileNotFoundError:
            # Handle case where file is not found
            print(f"FileNotFoundError for file: {upload_file.filename}")
            raise FileNotFoundError(f"The file {upload_file.filename} was not found.")
        except PermissionError:
            # Handle permission error during file access
            print(f"PermissionError for file: {upload_file.filename}")
            raise PermissionError(f"Permission denied for file {upload_file.filename}.")

# Класс для векторизации документов
class DocumentVectorizer:
    def __init__(self, model_name: str = Config.MODEL_NAME):
        # Initialize vectorizer with an embedding model
        print(f"Initializing DocumentVectorizer with model: {model_name}")
        self.embedding_model = OpenAIEmbeddings()
        self.vectorstore = None

    def vectorize(self, texts: List[str], batch_size: int = 10):
        # Split the documents into batches for efficient processing
        print(f"Vectorizing documents in batches of size: {batch_size}")
        vector_batches = [texts[i:i + batch_size] for i in range(0, len(texts), batch_size)]
        all_vectors = []
        for batch in vector_batches:
            print(f"Vectorizing batch of size: {len(batch)}")
            # Vectorize each batch of documents using the embedding model
            batch_vectors = FAISS.from_texts(batch, embedding=self.embedding_model)
            all_vectors.append(batch_vectors)
        # Combine all vectorstores into one unified vectorstore
        print("Merging all vectorstores into one")
        self.vectorstore = FAISS.merge(all_vectors)
        return self.vectorstore

# Класс для проверки требований с использованием LangChain и GPT
class UseCaseChecker:
    def __init__(self, model_name: str = Config.MODEL_NAME, temperature: float = Config.TEMPERATURE):
        # Initialize the use case checker with the chosen language model and temperature
        print(f"Initializing UseCaseChecker with model: {model_name}, temperature: {temperature}")
        self.model = ChatOpenAI(model=model_name, temperature=temperature)
        # Create a prompt template for analyzing requirements
        self.prompt_template = ChatPromptTemplate.from_template(
            """
            Проанализируй следующие требования на соответствие регламентам: {requirement}.
            Для каждого требования сопоставь его с регламентом и укажи, соблюдены ли регламенты. Если модель найдет слово или термин, который вызывает затруднение или который она интерпретирует как неясный, выдели его с двух сторон символами #- (например, #-Слово#-).
            Добавь комментарий, если есть расхождения между требованиями и регламентом, и также выделяй проблемные термины в этих комментариях.
            """
        )
        self.output_parser = StrOutputParser()

    async def check_requirements(self, specification_text: str, use_case_texts: List[str]):
        print("Starting requirements check")
        # Vectorize the specification text along with use case texts
        vectorizer = DocumentVectorizer()
        vectorstore = vectorizer.vectorize([specification_text] + use_case_texts)

        response_parts = []
        for use_case_text in use_case_texts:
            print(f"Performing similarity search for use case: {use_case_text[:50]}...")
            # Search for similar documents in the vectorstore
            docs = vectorstore.similarity_search(use_case_text)

            if docs:
                print("Matching documents found, generating response")
                # Create prompt and use the model to generate a response
                prompt = self.prompt_template.format(requirement=use_case_text)
                try:
                    response = self.model(prompt)
                    parsed_response = self.output_parser.invoke(response)
                except Exception as e:
                    # Handle errors during response generation
                    print(f"Error processing response for use case: {use_case_text[:50]}... - {str(e)}")
                    parsed_response = f"Error processing the response: {str(e)}"

                response_parts.append(f"Use Case: {use_case_text}\nResponse: {parsed_response}\n{'-' * 40}\n")
            else:
                print("No matching documents found for use case")
                response_parts.append(f"Use Case: {use_case_text}\nNo matching regulations found.\n{'-' * 40}\n")

        combined_response = ''.join(response_parts)
        print("Requirements check completed")
        return combined_response

@app.post("/check-requirements/")
async def check_requirements(specification: str, use_case_files: List[UploadFile] = File(...)):
    try:
        print("Received request to check requirements")
        # Extract text from each uploaded use case file
        use_case_texts = [await TextExtractor.extract_text_from_file(file) for file in use_case_files]
        # Initialize the use case checker and perform the requirements check
        checker = UseCaseChecker()
        result = await checker.check_requirements(specification, use_case_texts)
        print("Returning result of requirements check")
        return {"result": result}
    except ValueError as e:
        # Handle value errors
        print(f"ValueError: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        # Handle file not found errors
        print(f"FileNotFoundError: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        # Handle permission errors
        print(f"PermissionError: {str(e)}")
        raise HTTPException(status_code=403, detail=str(e))

if __name__ == "__main__":
    print("Starting FastAPI server")
    uvicorn.run(app, host="0.0.0.0", port=8000)
