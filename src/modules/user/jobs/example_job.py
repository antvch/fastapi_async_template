import logging

from modules.user.services.log import Log

# initialize logger
logging.basicConfig(
    format='%(levelname)s - %(asctime)s - %(message)s',
    level=logging.INFO
)
log = logging.getLogger(__name__)


async def example_job():
    """
    Example of background task with Scheduler
    """
    log.info('START EXAMPLE JOB...')
    Log.to_file("Example job just got executed")
