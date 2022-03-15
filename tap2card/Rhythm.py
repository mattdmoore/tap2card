from numpy import roll, bincount, cumsum, zeros


class Rhythm:
    def __init__(self, onsets):
        self.onsets = tuple(onsets)
        if max(onsets) > 1:
            self.__from_durations(onsets)

        self.metre = sum(self.onsets)

    def __repr__(self):
        return str(self.onsets)

    def __len__(self):
        return len(self.onsets)

    def __from_durations(self, durations):
        idx = cumsum(durations) - durations
        onsets = zeros(sum(durations), dtype=int)
        onsets[idx] = 1
        self.onsets = tuple(onsets)

    def rotate(self, r):
        return Rhythm(roll(self.onsets, -r))

    def durations(self):
        durations = bincount(cumsum(self.onsets))
        durations[-1] += durations[0]
        return tuple(durations[1:])
