from src.olyrica import Olyrica


def main():
    olyrica = Olyrica()

    lyrics = []

    for i in range(3):
        lyric = olyrica.get_random_lyric()
        lyrics.append(lyric)

    for lyric in lyrics:
        analysis = olyrica.analyze_lyric(lyric)
        print(f"Result: {analysis} | Lyric: {lyric}")


if __name__ == "__main__":
    main()
