from typing import TypedDict

import uvicorn
from fastapi import FastAPI

from src.routers import login, salary


class HTTPUnauthorizedError(TypedDict):
    detail: str


app = FastAPI(responses={401: {"model": HTTPUnauthorizedError}})

app.include_router(salary.router)
app.include_router(login.router)


if __name__ == "__main__":
    from src.settings import AppSettings

    settings = AppSettings()
    uvicorn.run(
        "src.main:app", host=settings.app_host, port=settings.app_port, reload=settings.debug
    )
