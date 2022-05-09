from .Trial import Trial


class Practice:
    def __init__(self, rhythm, participant_id):
        self.trial = Trial(rhythm, 0)
        self.participant_id = participant_id

    def begin(self, window, drum_pad):
        self.trial.practice(window, drum_pad, self.participant_id)
        self.trial.run(window, drum_pad, self.participant_id)
