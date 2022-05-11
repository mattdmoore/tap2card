from psychopy import core
from .RhythmFinder import RhythmFinder
from .TrialData import TrialData


class Trial:
    def __init__(self, rhythm, trial_num):
        # Trial variables
        self.rhythm = rhythm
        self.trial_num = trial_num

        # Timeout variables
        self.practice_duration = 180
        self.trial_duration = 60
        self.clock = core.Clock()

        # Success condition variables
        self.correct_taps = 0
        self.n_repetitions = 5

        # Error detection variables
        self.errors = {
            'ioi': 0,
            'metre': 0,
            'rhythm': 0
        }
        self.error_threshold = 4

    def practice(self, window, drum_pad, participant_id):
        feedback_cooldown = 0
        finder = RhythmFinder(self.rhythm)
        iois, rhos = [], []
        window.show_rhythm(self.trial_num, True)
        drum_pad.listen()

        # Wait for first tap before starting timer
        while not drum_pad.new_tap:
            continue
        t0 = self.clock.getTime()

        while (self.clock.getTime() - t0) < self.practice_duration:
            if drum_pad.has_intervals and drum_pad.new_tap:
                drum_pad.new_tap = False
                intervals = drum_pad.intervals[-len(self.rhythm.durations()) * 3:]
                history = ' '.join([str(x) if x is not None else '-' for x in intervals])

                rhythm = finder.find_rhythm(intervals)
                ioi, rho = drum_pad.find_ioi(n=10)
                iois.append(ioi)
                rhos.append(rho)

                if intervals[-1] is not None and intervals[-1] > 9:
                    self.errors = {
                        'ioi': 0,
                        'metre': 0,
                        'rhythm': 0
                    }
                    window.show_rhythm(self.trial_num, True)
                    feedback_cooldown = 10

                if feedback_cooldown == 0:
                    # Check rhythm is correct
                    if rhythm is not None and rhythm == self.rhythm:
                        window.correct_rhythm(self.trial_num)
                        self.correct_taps += 1

                        if self.correct_taps > len(self.rhythm.durations()) * self.n_repetitions:
                            self.correct_taps = 0
                            break

                    else:
                        # Check taps are even
                        if ioi is None or rhythm is None:
                            self.errors['ioi'] += 1
                            if self.errors['ioi'] > self.error_threshold:
                                window.uneven_taps(self.trial_num)
                        else:
                            # Reset ioi error count
                            self.errors['ioi'] = 0

                            # Check metre is correct
                            if sum(rhythm.durations()) != sum(self.rhythm.durations()):
                                self.errors['metre'] += 1
                                if self.errors['metre'] > self.error_threshold:
                                    window.incorrect_metre(self.trial_num)
                            else:
                                # Reset metre error count
                                self.errors['metre'] = 0

                                # Check rhythm is correct
                                if rhythm != self.rhythm:
                                    self.errors['rhythm'] += 1
                                    if self.errors['rhythm'] > self.error_threshold:
                                        window.incorrect_rhythm(self.trial_num,
                                                                True if len(rhythm.durations()) > len(
                                                                    self.rhythm.durations())
                                                                else False)
                                else:
                                    self.errors['rhythm'] = 0
                else:
                    feedback_cooldown -= 1

                if ioi:
                    print('IOI:', str(round(ioi, 1)) + 'ms',
                          '(' + str(round(rho * 100)) + '%)',
                          'Rhythm:', rhythm.durations() if rhythm is not None else None,
                          'Correct' if rhythm == self.rhythm else 'Incorrect',
                          'History:', history)
                else:
                    print('IOI:', None,
                          '(' + str(round(rho * 100)) + '%)',
                          'Rhythm:', rhythm.durations() if rhythm is not None else None,
                          'Correct' if rhythm == self.rhythm else 'Incorrect',
                          'History:', history)

        result = {'taps': drum_pad.taps * 1000,
                  'velocities': drum_pad.velocities,
                  'intervals': drum_pad.intervals[1:],
                  'ioi': 1 / (iois / 1000),
                  'rho': rhos}

        data = TrialData(participant_id, self.trial_num, result, True)
        data.write_csv()

        window.stop(self.trial_num, True)
        drum_pad.stop()

    def run(self, window, drum_pad, participant_id):
        finder = RhythmFinder(self.rhythm)
        iois, rhos = [], []
        window.show_rhythm(self.trial_num)
        drum_pad.listen()

        # Wait for first tap before starting timer
        while not drum_pad.new_tap:
            continue
        t0 = self.clock.getTime()

        while (self.clock.getTime() - t0) < self.trial_duration:
            if drum_pad.has_intervals and drum_pad.new_tap:
                drum_pad.new_tap = False
                intervals = drum_pad.intervals[-len(self.rhythm.durations()) * 3:]
                history = ' '.join([str(x) if x is not None else '-' for x in intervals])

                rhythm = finder.find_rhythm(intervals)
                ioi, rho = drum_pad.find_ioi(n=10)
                iois.append(ioi)
                rhos.append(rho)

                if rhythm is not None and rhythm == self.rhythm:
                    self.correct_taps += 1

                    if self.correct_taps > len(self.rhythm.durations()) * self.n_repetitions:
                        self.correct_taps = 0
                        break

                if ioi:
                    print('IOI:', str(round(ioi, 1)) + 'ms',
                          '(' + str(round(rho * 100)) + '%)',
                          'Rhythm:', rhythm.durations() if rhythm is not None else None,
                          'Correct' if rhythm == self.rhythm else 'Incorrect',
                          'History:', history)
                else:
                    print('IOI:', None,
                          '(' + str(round(rho * 100)) + '%)',
                          'Rhythm:', rhythm.durations() if rhythm is not None else None,
                          'Correct' if rhythm == self.rhythm else 'Incorrect',
                          'History:', history)

        result = {'taps': drum_pad.taps * 1000,
                  'velocities': drum_pad.velocities,
                  'intervals': drum_pad.intervals[1:],
                  'ioi': 1 / (iois / 1000),
                  'rho': rhos}

        data = TrialData(participant_id, self.trial_num, result, False)
        data.write_csv()

        window.stop(self.trial_num)
        drum_pad.stop()
