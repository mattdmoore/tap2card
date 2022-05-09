from tap2card.Rhythm import Rhythm
from tap2card.Experiment import Experiment


def main(window, drum_pad, participant_id):
    rhythms = [Rhythm([2, 2, 1, 1, 2]),
               Rhythm([4, 1, 1, 2, 1, 1, 1, 1, 4])]

    experiment = Experiment(rhythms, participant_id)
    experiment.begin(window, drum_pad)
