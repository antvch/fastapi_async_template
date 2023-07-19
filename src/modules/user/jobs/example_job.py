from time import sleep
from ..services.log import Log

async def example_job():
    """
    Пример фоновой задачи, которая выполняется по расписанию
    """
    Log.to_file("Example job just got executed")