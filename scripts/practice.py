from tap2card.Rhythm import Rhythm
from tap2card.Practice import Practice


def main(window, drum_pad, participant_id):
    rhythm = Rhythm([1, 1, 2])
    practice = Practice(rhythm, participant_id)
    practice.begin(window, drum_pad)
