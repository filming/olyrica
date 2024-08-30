import os
import logging
from logging.handlers import TimedRotatingFileHandler
import zipfile
from os.path import basename
import random

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

    def get_valid_lyric(self):
        """Get a lyric from storage and analyze it using AI."""

        lyric = ""
        is_valid_lyric = False

        self.logger.info("Attempting to retrieve and validate a lyric.")

        while not is_valid_lyric:
            lyric = self.get_random_lyric()

            is_valid_lyric = (
                True  # we'll do some checking later to properly validate this
            )

        return lyric

    def get_random_lyric(self):
        """Get a random lyric from storage."""

        # Get a random album
        LYRICS_DIR_PATH = os.path.join("storage", "lyrics")
        random_album = random.choice(os.listdir(LYRICS_DIR_PATH))
        album_dir_path = os.path.join(LYRICS_DIR_PATH, random_album)

        # Get a random song from the album
        random_song = random.choice(os.listdir(album_dir_path))
        song_file_path = os.path.join(album_dir_path, random_song)

        # Get a random lyric from the song
        song_title = None
        song_lyrics = set()

        with open(song_file_path, encoding="utf-8") as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    if not song_title:
                        song_title = line
                    else:
                        song_lyrics.add(line)

        song_lyrics = list(song_lyrics)
        random_song_lyric = random.choice(song_lyrics)

        self.logger.info(
            """Chosen lyric: " %s ". Chosen song: " %s ". Chosen album: " %s ".""",
            random_song_lyric,
            song_title,
            random_album,
        )

        return random_song_lyric
