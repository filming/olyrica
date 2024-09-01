# Olyrica

**A Twitter/X bot made in Python dedicated to tweeting out Olivia Rodrigo's song lyrics.**

## Description

Olyrica is a Python-based bot designed to autonomously post Olivia Rodrigo's song lyrics on Twitter. It starts by selecting a random lyric from her discography, validates their appeal using AI, and then tweets out the lyric via a Twitter API wrapper, [XIFY](https://github.com/filming/xify).

## Getting Started

### Dependencies

Below listed are the key dependencies:

* Python
* python-dotenv
* requests
* requests-oauthlib

### Installing

* Python can be downloaded from [here.](https://www.python.org/)
* Install all dependencies using `pip install -r requirements.txt` stored in main project directory.
* Add your Twitter/X and OpenAI API keys to an `.env` file.

### Executing program

Test examples on how to use this module are located inside of the [test](https://github.com/filming/olyrica/tree/main/tests) directory.

## Help

* All runtime data of Olyrica are stored in the log file located at `storage/logs/olyrica/current.log`.
* All runtime data of XIFY are stored in the log file located at `storage/logs/xify/current.log`.

## Authors

Contributors

* [Filming](https://github.com/filming)

## License

This project is licensed under the MIT License - see the LICENSE file for details
