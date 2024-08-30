import os
import logging
from logging.handlers import TimedRotatingFileHandler
import zipfile
from os.path import basename

from ..xify import Xify


class Olyrica:
    """A class to create a Twitter bot that tweets Olivia Rodrigo's song lyrics."""

    def __init__(self):
        self.logger = self.setup_logger()
        self.logger.info("An instance of Olyrica has been initialized.")

        self.logger.info("Attempting to create an instance of XIFY.")
        self.xify = Xify()
        self.xify.create_xas()

    def setup_logger(self) -> logging.Logger:
        """Create a TimedRotatingFileHandler that rotates at midnight and formats filenames dynamically."""

        # Make sure storage location for logger exists before creating logging obj
        LOG_DIR_PATH = os.path.join("storage", "logs", "olyrica")
        LOG_PATH = os.path.join(LOG_DIR_PATH, "current.log")
        os.makedirs(LOG_DIR_PATH, exist_ok=True)

        # Configure formatter
        formatter = logging.Formatter(
            "[ %(asctime)s ] [ %(levelname)-8s] [ %(filename)-24s ] [ %(funcName)-24s ] :: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Configure handler
        def rotator(source, dest):
            # Rotated log file is zipped and the original log file will be deleted
            zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED).write(
                source, os.path.basename(source)
            )
            os.remove(source)

        handler = TimedRotatingFileHandler(
            LOG_PATH,
            when="midnight",
            backupCount=365,
        )
        """
		default name for a log file that is being rotated (handler.namer lambda callable receives this):
		"current.log.2024-07-19"

		custom name for log file that is being rotated (lambda callable of handler.namer sets this):
		"2024-07-18.zip"
		"""
        handler.namer = lambda name: (
            os.path.join(LOG_DIR_PATH, f"{os.path.splitext(name)[1][1:]}.zip")
            if name.count(".") > 1
            else name
        )
        handler.rotator = rotator
        handler.setFormatter(formatter)

        # Configure logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        return logger
