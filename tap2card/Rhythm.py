from numpy import roll, bincount, cumsum, zeros


class Rhythm:
    def __init__(self, onsets):
        if isinstance(onsets, str):
            onsets = [int(x) for x in onsets]

        self.onsets = tuple(onsets)
        if max(onsets) > 1:
            self.__from_durations(onsets)

        self.metre = sum(self.onsets)

    def __repr__(self):
        return str(self.onsets)

    def __len__(self):
        return len(self.onsets)

    def __iter__(self):
        for onset in self.onsets:
            yield onset

    def __sub__(self, other):
        return (abs(x - y) for x, y in zip(self.onsets, other.onsets))

    def __eq__(self, other):
        if other is None:
            return False
        if len(self) != len(other):
            return False
        for r in range(len(other)):
            if sum(self - other.rotate(r)) == 0:
                return True
        return False

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
