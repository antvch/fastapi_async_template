from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from modules.user.exceptions.not_found import NotFoundException
from modules.user.jobs.example_job import example_job
from routers import router
from settings import env_vars

# Init app
app = FastAPI()

# Add rotes
app.include_router(router)

# Setup Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[env_vars.frontend_urls],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Scheduler
scheduler = AsyncIOScheduler()
scheduler.add_job(example_job, 'interval', minutes=30)


@app.on_event("startup")
async def startup() -> None:
    # Start scheduler
    scheduler.start()


@app.on_event("shutdown")
async def shutdown() -> None:
    # Stop scheduler
    scheduler.shutdown()


# Error handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Обработчик ответа при ошибках валидации запроса
    """
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"errors": exc.errors()}),
    )


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    """
    Обработчик ответа при ошибках валидации запроса
    """
    return JSONResponse(
        status_code=404,
        content=jsonable_encoder({"error": exc.message}),
    )
