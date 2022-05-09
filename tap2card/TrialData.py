import csv
from os.path import exists
from .Utilities import generate_filename


class TrialData:
    def __init__(self, participant_id, trial_num, result, practice):
        self.participant_id = participant_id
        self.trial_num = trial_num
        self.data = result
        self.practice = practice

    def write_csv(self):
        directory_structure = {
            0: 'data',
            1: 'participant_{:02d}.csv'.format(self.participant_id),
        }
        file = generate_filename(directory_structure)
        first_write = not exists(file)

        data = {
            'participant_id': self.participant_id,
            'trial_num': self.trial_num,
            'practice': self.practice,
            **self.data
        }

        with open(file, 'a') as f:
            w = csv.DictWriter(f, fieldnames=list(data.keys()))
            if first_write:
                w.writeheader()
            w.writerow(data)
