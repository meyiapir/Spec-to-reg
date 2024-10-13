import uvicorn
from fastapi import FastAPI

from API import logins, check_specs
from core.config import settings

app = FastAPI()

app.include_router(logins.router)
app.include_router(check_specs.router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.URL, port=8000, log_config=None)
