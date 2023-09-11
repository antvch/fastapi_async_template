import logging

from modules.user.services.log import LogsService

# initialize logger
logging.basicConfig(
    format='%(levelname)s - %(asctime)s - %(message)s',  # noqa: WPS323
    level=logging.INFO,
)
log = logging.getLogger(__name__)


async def example_job():
    """Пример функции, работающей в фоне."""
    log.info('START EXAMPLE JOB...')
    LogsService.to_file('Example job just got executed')
