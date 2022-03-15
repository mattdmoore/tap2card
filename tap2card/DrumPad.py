import mido
import numpy as np
from statistics import mode
from psychopy.clock import Clock


class DrumPad:
    def __init__(self, device=''):
        # Device
        self.port = []
        self.open_port(device)
        self.clock = Clock()

        # States
        self.listening = False
        self.new_tap = False
        self.tap_num = 0

        # Data
        self.taps = []
        self.velocities = []
        self.history = None
        self.error_history = None

    def open_port(self, device):
        inputs = mido.get_input_names()
        devices = [match for match in inputs if device in match]
        devices = list(dict.fromkeys(devices))

        if len(devices) == 0:
            raise ValueError('No device found matching name: {}'.format(device))

        if len(devices) == 1:
            idx = 0

        else:
            prompt = 'Multiple devices found:\n' + \
                     ''.join(['{}: {}\n'.format(i, device) for i, device in enumerate(devices)])
            print(prompt, '\n')

            while True:
                try:
                    idx = int(input('Select a device:'))
                    if 0 <= idx <= len(devices) + 1:
                        break

                except ValueError:
                    print('Please enter a number')

        self.port = mido.open_input(devices[idx], callback=self.tap)

    def tap(self, msg):
        if self.listening and msg.type == 'note_on':
            t = self.clock.getTime()
            if msg.velocity == 0:  # ignore note off messages
                return
            if self.taps and t - self.taps[-1] < .1:  # ignore sub-100ms taps (stick bounce)
                return
            self.taps.append(t)
            self.velocities.append(msg.velocity)
            self.new_tap = True

    def transcribe_rhythm(self, target_rhythm, min_n=6, memory=3):
        if not self.listening:
            self.listen()

        n = m = len(target_rhythm)
        if self.history is None:
            self.history = np.zeros((memory, m))
            self.error_history = np.zeros(m)

        if n < min_n:
            n *= (min_n * 2 - 2) // n  # multiply into suitable range

        if self.new_tap and len(self.taps) > n:
            self.new_tap = False
            intervals = np.diff(np.array(self.taps[-(n + 1):]) * 1e3)  # convert last n taps to milliseconds

            search_min = intervals.min(initial=None) / 1.5  # reduce harmonic issues by using lower bound > min / 2
            search_max = intervals.mean()  # sensible upper bound
            ioi, strength = self.find_ioi(n, (search_min, search_max))
            if ioi is not None:
                rhythm = np.round(intervals / ioi)  # use extracted IOI to scale intervals to nearest metrical unit

                closest = match_rhythms(rhythm, target_rhythm, m)

                error = np.roll(rhythm - intervals / ioi, closest[0])
                self.error_history = (self.error_history + error) / 2
                self.history[self.tap_num % memory] = np.roll(rhythm[-m:], closest[0])
                self.tap_num += 1

                print('Target rhythm:\t\t\t\t', target_rhythm)
                print('Consensus rhythm estimate:\t', [int(mode(self.history[:, i])) for i in range(m)])
                print('IOI: {0:.1f}ms\tConfidence: {1:.1f}%'.format(ioi, strength * 100))

                print('History:')
                print(self.history, '\n')

    def find_ioi(self, n, initial_range=(100, 3000), search_resolution=20, stopping_threshold=1.05):

        # Binary logarithmic search with circularised IOIs
        taps = 2 * np.pi * np.array(self.taps[-n:]) * 1e3  # scale IOIs to millisecond radians
        critical_value = [5.297, 5.556, 5.743, 5.885, 5.996, 6.085, 6.158, 6.219, 6.271][n - 6]

        ioi, strength = None, None
        search_range = np.log10(initial_range)  # initial search range in milliseconds
        while 10 ** (search_range[1] - search_range[0]) > stopping_threshold:  # loop until search bounds are within 5%
            iois = np.logspace(*search_range, search_resolution)  # log-spaced IOIs in search range
            rho = np.zeros(iois.size)
            for i, val in enumerate(iois):
                scaled = taps / val  # scale taps using each IOI
                rho[i] = resultant_vector(scaled)  # calculate mean resultant vector length

            idx, strength = rho.argmax(), rho.max(initial=None)  # get index and length of max resultant vector
            m = int(search_resolution / 2 - 1)  # midpoint of search range
            search_range = np.log10((iois[:m+1:m] if idx <= m else iois[m+1::m]))  # cut search space in half
            # print(10 ** search_range)
            if n * rho[idx] ** 2 > critical_value:
                ioi = iois[idx]

        return ioi, strength

    def get_data(self):
        self.stop()
        return [self.taps, self.velocities]

    def listen(self, delay=0):
        self.reset(delay)
        self.listening = True

    def stop(self):
        self.listening = False

    def reset(self, delay=0):
        self.clock.reset(delay)

        self.listening = False
        self.new_tap = False

        self.taps = []
        self.velocities = []

    def print_summary(self, beat, phase, taps, metre):
        print('Beat: {0} \tPhase: {1}'.format(beat,
                                              phase))
        print('Found in {0:.1f} cycles | {1} taps'.format(taps[-1] / (2 * metre * np.pi),
                                                          len(self.taps)))


def match_rhythms(rhythm, target, m):
    closest = (None, 1e3)
    for r in range(m):
        distance = sum([abs(a - b) for a, b in zip(target, np.roll(rhythm[-m:], r))])
        closest = (r, distance) if distance < closest[1] else closest
    return closest


def resultant_vector(rads):
    x = sum(np.cos(rads)) ** 2
    y = sum(np.sin(rads)) ** 2
    return np.sqrt(x + y) / len(rads)


def circular_mean(rads):
    x = sum(np.cos(rads))
    y = sum(np.sin(rads))
    return np.arctan2(y, x)
