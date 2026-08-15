import logging
import sys
def setup_logger():
    logger = logging.getLogger("enterprise-kb")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter('%(asctime)s [%(levelname)s)] %(message)s')
    )
    logger.addHandler(handler)

    return logger

logger = setup_logger()
if not logger.handlers:
    logger.addHandler(handler)


