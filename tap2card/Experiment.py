from .Trial import Trial


class Experiment:
    def __init__(self, rhythms, participant_id):
        self.trials = [Trial(rhythm, i + 1) for i, rhythm in enumerate(rhythms)]
        self.participant_id = participant_id

    def begin(self, window, drum_pad):
        window.main_experiment()
        for trial in self.trials:
            trial.practice(window, drum_pad, self.participant_id)
            trial.run(window, drum_pad, self.participant_id)
        window.finished()
