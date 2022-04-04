from psychopy import event
import curses
from tap2card.RhythmFinder import RhythmFinder


class Trial:
    def __init__(self, rhythm):
        self.rhythm = rhythm

    def practice(self, window, drum_pad):
        finder = RhythmFinder(self.rhythm)

        console = curses.initscr()
        curses.cbreak()
        curses.curs_set(0)

        window.rhythm_visualiser(self.rhythm)
        drum_pad.listen()
        while not event.getKeys():
            if drum_pad.has_intervals and drum_pad.new_tap:
                drum_pad.new_tap = False
                intervals = drum_pad.intervals[-len(self.rhythm.durations()) * 3:]

                rhythm = finder.find_rhythm(intervals)
                ioi, strength = drum_pad.find_ioi(n=10)

                console.clear()
                console.addstr(0, 0, 'History: ' + ' '.join([str(x) if x is not None else '-' for x in intervals]))
                if ioi is None:
                    console.addstr(1, 0, 'Taps are uneven')
                else:
                    console.addstr(1, 0, 'IOI: {0:.1f} Confidence: {1:.2f}%'.format(
                        ioi, strength * 100))

                if not rhythm:
                    console.addstr(2, 0, 'Rhythm does not repeat')
                else:
                    console.addstr(2, 0, 'Found: ' + ' '.join([str(x) for x in rhythm.durations()]) +
                                   ' Match: {}'.format(rhythm == self.rhythm))
                console.refresh()

        # Clean up
        console.clear()
        curses.endwin()
        drum_pad.reset()

    def run(self, window, drum_pad):
        pass
