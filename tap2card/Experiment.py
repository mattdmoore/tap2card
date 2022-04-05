from .Trial import Trial


class Experiment:
    def __init__(self, rhythms):
        self.trials = [Trial(rhythm, i + 1) for i, rhythm in enumerate(rhythms)]

    def begin(self, window, drum_pad):
        for trial in self.trials:
            trial.practice(window, drum_pad)
            trial.run(window, drum_pad)
