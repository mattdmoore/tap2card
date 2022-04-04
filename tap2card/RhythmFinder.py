from tap2card.Rhythm import Rhythm


class RhythmFinder:
    def __init__(self, target):
        self.target = Rhythm(target) if not isinstance(target, Rhythm) else target

    def find_rhythm(self, intervals):
        string = ''.join([str(x) if x is not None else '-' for x in intervals])

        trie = Trie()
        for i in range(len(string)):
            for j in range(i + 2, len(string)):
                trie.add(string[i:j + 1])

        candidates = [Rhythm(rhythm) for rhythm in trie.find_repeats() if '-' not in rhythm]
        for rhythm in candidates:
            if rhythm == self.target:
                return rhythm
        return max(candidates, key=len) if candidates else None


class Trie(dict):
    def __init__(self):
        super().__init__()

    def add(self, *args):
        for word in args:
            current = self
            for letter in word:
                current = current.setdefault(letter, Trie())
            current['_'] = '_'

    def list_words(self):
        my_list = []
        for k, v in self.items():
            if k != '_':
                for el in v.list_words():
                    my_list.append(k + el)
            else:
                my_list.append('')
        return my_list

    def find_repeats(self):
        result = []
        for word in self.list_words():
            node = self
            for letter in word:
                if letter in node.keys():
                    node = node[letter]

            if word in node.list_words():
                result.append(word)
        return result
