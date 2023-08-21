from http import HTTPStatus

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from exceptions import NotFoundError
from modules.user.jobs.example_job import example_job
from routers import router
from settings import settings

# Init app
app = FastAPI()

# Add rotes
app.include_router(router)

# Setup Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_urls],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Scheduler
scheduler = AsyncIOScheduler()
SCHEDULER_INTERVAL_IN_MINUTES = 30
scheduler.add_job(example_job, 'interval', minutes=SCHEDULER_INTERVAL_IN_MINUTES)


@app.on_event('startup')
async def startup() -> None:
    """Срабатывает на старт FastAPI приложения."""
    # Start scheduler
    scheduler.start()


@app.on_event('shutdown')
async def shutdown() -> None:
    """Срабатывает на остановку FastAPI приложения."""
    # Stop scheduler
    scheduler.shutdown()


# Error handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
) -> JSONResponse:
    """
    Обработчик ответа при ошибках валидации запроса.

    :param request: HTTP запрос
    :type request: Request

    :param exc: Ошибка
    :type exc: RequestValidationError

    :returns: JSONResponse
    """
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'errors': exc.errors()}),
    )


@app.exception_handler(NotFoundError)
async def not_found_exception_handler(
        request: Request,
        exc: NotFoundError,
) -> JSONResponse:
    """
    Обработчик ответа при ошибках валидации запроса.

    :param request: HTTP запрос
    :type request: Request

    :param exc: Ошибка
    :type exc: NotFoundError

    :returns: JSONResponse
    """
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content=jsonable_encoder({'error': exc.message}),
    )
