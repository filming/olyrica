from src.olyrica import Olyrica


def main():
    olyrica = Olyrica()

    lyric = olyrica.get_valid_lyric()
    print(lyric)


if __name__ == "__main__":
    main()
