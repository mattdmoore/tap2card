from .Trial import Trial


class Experiment:
    def __init__(self, rhythms):
        self.trials = [Trial(rhythm) for rhythm in rhythms]

    def begin(self, window, drum_pad):
        for trial in self.trials:
            trial.practice(window, drum_pad)
            trial.run(window, drum_pad)
