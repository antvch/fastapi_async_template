from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from .routers import router
from .modules.user.exceptions.not_found import NotFoundException
from .modules.user.jobs.example_job import example_job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import os

app = FastAPI()

@app.on_event("startup")
async def startup() -> None:
    # Запуск задач по расписанию
    scheduler = AsyncIOScheduler()
    scheduler.add_job(example_job, 'interval', seconds=60)
    scheduler.start()

@app.on_event("shutdown")
async def shutdown() -> None:
    pass

"""
Обработчик ответа при ошибках валидации запроса
"""
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"errors": exc.errors()}),
    )
@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content=jsonable_encoder({"error": exc.message}),
    )

"""
Роуты
"""
app.include_router(router)

"""
Middleware
"""
origins = [
    os.environ["FRONTEND_URL"],
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)