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


def enter_id():
    while True:
        try:
            value = int(input('Please enter the participant ID number: '))
        except ValueError:
            print('Invalid input')
        else:
            return value


def main():
    participant_id = enter_id()
    drum_pad = tap2card.DrumPad('SPD')
    window = tap2card.Screen(fullscr=True, allowGUI=False, screen=1)
    # window = tap2card.Screen((2000, 1000))
    window.instructions()
    practice.main(window, drum_pad, participant_id)
    experiment.main(window, drum_pad, participant_id)


if __name__ == '__main__':
    if '__main__.py' not in listdir():  # if called as project folder
        chdir('tap2card')
    main()
