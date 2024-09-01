import time

from src.olyrica import Olyrica


def main():
    olyrica = Olyrica()

    hours, minutes, seconds = 0, 30, 0
    TWEET_DELAY = (hours * 3600) + (minutes * 60) + seconds

    olyrica.logger.info(
        "Delay between each tweet set to: %s hour(s), %s minute(s) and %s second(s).",
        hours,
        seconds,
        minutes,
    )

    while True:
        try:
            lyric = olyrica.get_valid_lyric()

            olyrica.xify.create_tweet(lyric)

            time.sleep(TWEET_DELAY)

        except Exception as e:
            olyrica.logger.critical(f"Previous attempt to run program failed. {e}")
            break


if __name__ == "__main__":
    main()
