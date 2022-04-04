from tap2card.Rhythm import Rhythm
from tap2card.Experiment import Experiment


def main(window, drum_pad):
    rhythms = [Rhythm([2, 2, 1, 1, 2]),
               Rhythm([4, 1, 1, 2, 1, 1, 1, 1, 4])]

    experiment = Experiment(rhythms)
    experiment.begin(window, drum_pad)
