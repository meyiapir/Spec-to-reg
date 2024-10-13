import os
import tempfile

from fastapi import UploadFile, File, Form, APIRouter
from fastapi.responses import JSONResponse

from certify.ai.langchain_rag_gpt import check_use_cases_against_specifications_gpt

router = APIRouter(prefix="/process")

# Маршрут для загрузки файлов и текстовых спецификаций
@router.post("/check-specifications/")
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
