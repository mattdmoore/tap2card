import tap2card
from scripts import practice, experiment


def main():
    drum_pad = tap2card.DrumPad('SPD')
    window = tap2card.Screen((400, 400))

    practice.main(window, drum_pad)
    experiment.main(window, drum_pad)


if __name__ == '__main__':
    main()
