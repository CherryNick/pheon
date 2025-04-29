from app import init_app
from app_config import Config
from extensions.logger import logger

try:
    config = Config()
except Exception as e:
    logger.error("Failed to load config")
    logger.exception(e)
    raise SystemExit(1) from e


app = init_app(config)
