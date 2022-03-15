import tap2card

if __name__ == '__main__':
    drum_pad = tap2card.DrumPad('SPD')
    while True:
        drum_pad.transcribe_rhythm([4, 3, 1, 2, 2, 4])
