from psychopy import event, core
from .RhythmFinder import RhythmFinder


class Trial:
    def __init__(self, rhythm, trial_num):
        self.rhythm = rhythm
        self.trial_num = trial_num
        self.clock = core.Clock()
        self.errors = {
            'ioi': 0,
            'metre': 0,
            'rhythm': 0
        }
        self.error_threshold = 3

    def practice(self, window, drum_pad):
        finder = RhythmFinder(self.rhythm)
        window.show_rhythm(self.trial_num, True)
        drum_pad.listen()

        while not event.getKeys():
            if drum_pad.has_intervals and drum_pad.new_tap:
                drum_pad.new_tap = False
                intervals = drum_pad.intervals[-len(self.rhythm.durations()) * 3:]
                history = ' '.join([str(x) if x is not None else '-' for x in intervals])

                rhythm = finder.find_rhythm(intervals)
                ioi, strength = drum_pad.find_ioi(n=10)
                window.show_rhythm(self.trial_num, True)

                # Check taps are even
                if ioi is None:
                    self.errors['ioi'] += 1
                    if self.errors['ioi'] > self.error_threshold:
                        window.uneven_taps(self.trial_num)
                else:
                    self.errors['ioi'] = 0

                # Check metre is correct
                if rhythm is not None and sum(rhythm.durations()) != sum(self.rhythm.durations()):
                    self.errors['metre'] += 1
                    if self.errors['metre'] > self.error_threshold:
                        window.incorrect_metre(self.trial_num)
                else:
                    self.errors['metre'] = 0

                # Check rhythm is correct
                if rhythm != self.rhythm:
                    self.errors['rhythm'] += 1
                    if self.errors['rhythm'] > self.error_threshold:
                        window.incorrect_rhythm(self.trial_num)
                else:
                    self.errors['rhythm'] = 0

                if ioi:
                    print('IOI:', str(round(ioi, 1)) + 'ms',
                          '(' + str(round(strength * 100)) + '%)',
                          'Rhythm:', rhythm.durations() if rhythm is not None else None,
                          'Correct' if rhythm == self.rhythm else 'Incorrect',
                          'History:', history)
                else:
                    print('IOI:', None,
                          '(' + str(round(strength * 100)) + '%)',
                          'Rhythm:', rhythm.durations() if rhythm is not None else None,
                          'Correct' if rhythm == self.rhythm else 'Incorrect',
                          'History:', history)

        window.stop(True)
        event.waitKeys()

        # For debugging
        # import curses
        # console = curses.initscr()
        # curses.cbreak()
        # curses.curs_set(0)
        # while not event.getKeys():
        #     if drum_pad.has_intervals and drum_pad.new_tap:
        #         drum_pad.new_tap = False
        #         intervals = drum_pad.intervals[-len(self.rhythm.durations()) * 3:]
        #
        #         rhythm = finder.find_rhythm(intervals)
        #         ioi, strength = drum_pad.find_ioi(n=10)
        #
        #         console.clear()
        #         console.addstr(0, 0, 'History: ' + ' '.join([str(x) if x is not None else '-' for x in intervals]))
        #         if ioi is None:
        #             console.addstr(1, 0, 'Taps are uneven')
        #         else:
        #             console.addstr(1, 0, 'IOI: {0:.1f} Confidence: {1:.2f}%'.format(
        #                 ioi, strength * 100))
        #
        #         if not rhythm:
        #             console.addstr(2, 0, 'Rhythm does not repeat')
        #         else:
        #             console.addstr(2, 0, 'Found: ' + ' '.join([str(x) for x in rhythm.durations()]) +
        #                            ' Match: {}'.format(rhythm == self.rhythm))
        #         console.refresh()
        # console.clear()
        # curses.endwin()

        drum_pad.reset()

    def run(self, window, drum_pad):
        finder = RhythmFinder(self.rhythm)
        window.show_rhythm(self.trial_num)
        drum_pad.listen()

        while not event.getKeys():
            if drum_pad.has_intervals and drum_pad.new_tap:
                drum_pad.new_tap = False
                intervals = drum_pad.intervals[-len(self.rhythm.durations()) * 3:]
                history = ' '.join([str(x) if x is not None else '-' for x in intervals])

                rhythm = finder.find_rhythm(intervals)
                ioi, strength = drum_pad.find_ioi(n=10)

                if ioi:
                    print('IOI:', str(round(ioi, 1)) + 'ms',
                          '(' + str(round(strength * 100)) + '%)',
                          'Rhythm:', rhythm.durations() if rhythm is not None else None,
                          'Correct' if rhythm == self.rhythm else 'Incorrect',
                          'History:', history)
                else:
                    print('IOI:', None,
                          '(' + str(round(strength * 100)) + '%)',
                          'Rhythm:', rhythm.durations() if rhythm is not None else None,
                          'Correct' if rhythm == self.rhythm else 'Incorrect',
                          'History:', history)
        window.stop()
        event.waitKeys()

    def trial_finished(self):
        pass
