import uvicorn
from fastapi import FastAPI

from core.config import settings
from API import logins

app = FastAPI()

app.include_router(logins.router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.URL, port=8000, log_config=None)
