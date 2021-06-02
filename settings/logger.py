import sys

import logging
from logging import Formatter
from logging.handlers import BufferingHandler

logger = logging.getLogger(__name__)
LOGFORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

bufferHandler = BufferingHandler(1000)
bufferHandler.setFormatter(Formatter(LOGFORMAT))


def setup_logging_pre() -> None:
    """
    [Logging setup.]
    """
    logging.basicConfig(
        level=logging.INFO,
        format=LOGFORMAT,
        handlers=[logging.StreamHandler(sys.stderr), bufferHandler])
