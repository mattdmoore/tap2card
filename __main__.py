import tap2card
from os import chdir, listdir
from scripts import practice, experiment

# Data format:
# P_num, Trial num, Unit rate (Hz), Timestamps (ms), Resultant vector

# TODO:
#   - Setup basic experiment flow
#       - Practice + 2 trials
#       - Pre-recording practice with feedback
#   - Adapt data saving to paradigm
#       - Automatic attempt segmentation(?)
#   - Placeholder instruction pages
#   - Implement feedback types:
#       - Uneven durations (resultant vector check)
#       - Misinterpreted rhythm (matched durations check)
#       - Misinterpreted metre (unmatched durations check)
#       - Double tap(?) (should be blocked by pad lockout)
#       - Improper loop (final duration check)
#       - Early stopping (long pause check)
#   - Self-rating(?)


def main():
    drum_pad = tap2card.DrumPad('SPD')
    window = tap2card.Screen((2000, 1000))

    window.instructions()
    practice.main(window, drum_pad)
    experiment.main(window, drum_pad)


if __name__ == '__main__':
    if '__main__.py' not in listdir():  # if called as project folder
        chdir('tap2card')
    main()
