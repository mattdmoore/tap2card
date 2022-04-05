from .Trial import Trial


class Practice:
    def __init__(self, rhythm):
        self.trial = Trial(rhythm, 0)

    def begin(self, window, drum_pad):
        self.trial.practice(window, drum_pad)
        self.trial.run(window, drum_pad)
