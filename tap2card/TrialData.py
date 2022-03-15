from pickle import dump, HIGHEST_PROTOCOL
import csv

from .Utilities import generate_filename


class TrialData:
    def __init__(self, participant_id, trial_info, data, result):
        self.participant_id = participant_id
        self.trial_info = {
            'block': trial_info[0],
            'block_name': trial_info[1],
            'trial': trial_info[2],
            'rhythm': trial_info[3]
        }

        self.data = {'taps': data[0],
                     'velocities': data[1]}

        self.result = {
            'ioi': result[0],
            'rho': result[1]  # mean resultant vector length
        }

    def cache(self):
        directory_structure = {
            0: 'data',
            1: 'cache',
            2: 'participant_{}'.format(self.participant_id),
            3: 'block_{}'.format(self.trial_info['block']),
            4: 'trial-{}.pickle'.format(self.trial_info['trial'])
        }
        file = generate_filename(directory_structure)
        try:
            with open(file, "wb") as f:
                dump(self, f, protocol=HIGHEST_PROTOCOL)
        except Exception as ex:
            print("Error during pickling object:", ex)

    def write_csv(self, file):
        data = {
            'participant_id': self.participant_id,
            **self.trial_info,
            **self.data,
            **self.result
        }
        csv.DictWriter(file, fieldnames=list(data.keys())).writerow(data)
