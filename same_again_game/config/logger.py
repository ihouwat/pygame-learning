import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s, %(lineno)d: %(message)s')
logging.getLogger("app_logger")
logger = logging.getLogger("app_logger")