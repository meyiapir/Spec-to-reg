import uvicorn
from fastapi import FastAPI
from sqlalchemy.testing.plugin.plugin_base import logging

from certify.API import logins, check_specs
from certify.core.config import settings

app = FastAPI()

app.include_router(logins.router)
app.include_router(check_specs.router)

if __name__ == "__main__":
    print("Running server")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)
