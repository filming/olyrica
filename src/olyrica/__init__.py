from dotenv import load_dotenv
import requests

import os
import logging
from logging.handlers import TimedRotatingFileHandler
import zipfile
from os.path import basename
import random
import json
import time

from ..xify import Xify


class Olyrica:
    """A class to create a Twitter bot that tweets Olivia Rodrigo's song lyrics."""

    def __init__(self) -> None:
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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

    def get_valid_lyric(self) -> str:
        """Get a lyric from storage and analyze it using AI."""

        lyric = ""
        is_valid_lyric = False

        while not is_valid_lyric:
            self.logger.info("Attempting to retrieve and validate a lyric.")

            lyric = self.get_random_lyric()

            is_valid_lyric = self.analyze_lyric(lyric)

        return lyric

    def get_random_lyric(self) -> str:
        """Get a random lyric from storage."""

        # Get a random album
        LYRICS_DIR_PATH = os.path.join("storage", "lyrics")
        random_album = random.choice(
            ["SOUR", "GUTS"]
        )  # We're going to hard-code the album choices for this project

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

    def analyze_lyric(self, lyric) -> bool:
        """Determine the validity of a lyric using OpenAI."""

        # Create custom prompt
        prompt = f"""You will be given a song lyric that will require you to analyze its emotional depth, relatability and thought-provoking nature. This is to determine its potential impact on my Twitter audience. My Twitter audience in this case are fans of a specific popstar. Respond with 'Positive' if the lyric demonstrates introspection, emotional resonance, or thought-provoking elements, making it relatable and engaging. Otherwise, respond with 'Negative' if the lyric lacks depth or fails to resonate emotionally or intellectually. If the lyric contains vivid metaphors, powerful imagery, or captures universal experiences, consider it as 'Positive'. Here is the lyric: {lyric}"""

        sample_valid_lyrics = [
            "You used me as an alibi",
            "Just so I could call you mine",
            "And do you tell her she's the most beautiful girl you've ever seen?",
            "She probably gives you butterflies",
            "Quit my job, start a new life",
            "Show her off like she's a new trophy",
            "You got me fucked up in the head, boy",
            "But even after all this, you're still everything to me",
            "Yeah, I'm so tough when I'm alone and I make you feel so guilty",
            "And I'd leave you, but the roller coaster's all I've ever had",
            "Crying on the floor of my bathroom",
            "Maybe I'm too emotional",
        ]
        sample_invalid_lyrics = [
            "The things you did",
            "Doe-eyed as you buried me",
            "I wonder if you're around",
            "Your favorite crime",
            "She's so pretty",
            "I'm selfish, I know",
            "Really",
            "I don't understand",
            "I've spent the night",
            "Do you get déjà vu? (Oh-oh)",
        ]

        prompt = f"""
        You will be given a song lyric that will require you to analyze its potential impact on my Twitter audience, who are fans of a specific popstar. 

        Please rate the lyric on the following scales:

        * Emotional Resonance: 
            * 1 (Very low) - The lyric evokes little to no emotional response.
            * 3 (Neutral) - The lyric evokes a mild emotional response or is emotionally neutral.
            * 5 (Very high) - The lyric evokes a strong emotional response. 

        * Relatability:
            * 1 (Very low) - The lyric describes a very niche or uncommon experience.
            * 3 (Neutral) - The lyric describes an experience that some, but not all, people might relate to.
            * 5 (Very high) - The lyric describes a universal experience or emotion that most people can connect with.

        * Thought-provoking nature:
            * 1 (Very low) - The lyric is straightforward and doesn't invite deeper thought or interpretation
            * 3 (Neutral) - The lyric might prompt some reflection, but doesn't necessarily challenge existing perspectives
            * 5 (Very high) - The lyric challenges conventional thinking, sparks debate or encourages deeper analysis

        Keep in mind that pop music lyrics often use figurative language, metaphors, and hyperbole to express emotions and experiences. Relatability can stem from both positive and negative emotions, as well as observations about common social situations.

        Here are some examples of lyrics that I think are typically positive/valid: {sample_valid_lyrics}, and here are some examples of lyrics that I think are negative/invalid: {sample_invalid_lyrics}.

        Based on these critereas, summarize the lyric and respond with either 'Positive' or 'Negative'.

        Here is the lyric: {lyric}
        """
        # Send query to OpenAI
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.OPENAI_API_KEY}",
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
        }

        self.logger.info("Sending lyric to OpenAI to validate its status as a lyric.")

        successful_prompt = False
        resp_msg = ""

        while not successful_prompt:
            r = requests.post(
                "https://api.openai.com/v1/chat/completions",
                data=json.dumps(payload),
                headers=headers,
            )
            resp = json.loads(r.text)

            if r.status_code == 200:
                resp_msg = resp["choices"][0]["message"]["content"].lower()
                successful_prompt = True

            elif r.status_code == 429:
                wait_time = 21
                time.sleep(wait_time)

        # Parse the response
        if "positive" in resp_msg:
            self.logger.info(
                """The lyric " %s " has passed validation from OpenAI.""", lyric
            )

            return True

        else:
            self.logger.info(
                """The lyric " %s " has failed validation from OpenAI.""", lyric
            )

            return False
