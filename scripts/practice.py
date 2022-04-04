from tap2card.Rhythm import Rhythm
from tap2card.Practice import Practice


def main(window, drum_pad):
    rhythm = Rhythm([1, 1, 2])
    practice = Practice(rhythm)
    practice.begin(window, drum_pad)
